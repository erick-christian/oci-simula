import os
import glob
import sys
import subprocess
import shutil

# Auto-instalar paramiko si no está disponible
try:
    import paramiko
except ImportError:
    print("[*] Instalando dependencia requerida (paramiko)...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "paramiko"])
    import paramiko

def cargar_env(ruta):
    env_vars = {}
    if not os.path.exists(ruta):
        print(f"[!] Error: No se encontró el archivo {ruta}")
        sys.exit(1)
        
    with open(ruta, 'r') as f:
        for linea in f:
            linea = linea.strip()
            if '=' in linea and not linea.startswith('#'):
                key, val = linea.split('=', 1)
                env_vars[key.strip()] = val.strip()
    return env_vars

def main():
    print("=====================================================")
    print(" ADVERTENCIA: DESPLIEGUE EN LIMPIO (FRESH DEPLOY)")
    print(" Esto destruirá la base de datos de producción")
    print(" y todos los archivos del código anterior.")
    print("=====================================================\n")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    env_file = os.path.join(base_dir, 'deploy.env')
    env_vars = cargar_env(env_file)
    
    HOST = env_vars.get('HOST')
    USER = env_vars.get('USER')
    PASSWORD = env_vars.get('PASSWORD')
    REMOTE_DIR = '/var/www'
    
    if not all([HOST, USER, PASSWORD]):
        print("[!] Faltan credenciales en deploy.env")
        sys.exit(1)

    archivos_tar = glob.glob(os.path.join(base_dir, 'deploy_oci-app_*.tar.gz'))
    
    if not archivos_tar:
        print(f"[!] No se encontró ningún archivo .tar.gz en {base_dir}")
        sys.exit(1)
        
    latest_tar = max(archivos_tar, key=os.path.getctime)
    filename = os.path.basename(latest_tar)
    ruta_remota_tar = f"/root/{filename}"
    
    filename_done = filename.replace('deploy_', '', 1) + '.done'
    ruta_remota_done = f"/root/{filename_done}"

    print(f"[*] Paquete a desplegar: {filename}")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(hostname=HOST, username=USER, password=PASSWORD, timeout=10)
        print("[*] Conexión SSH establecida con éxito.")
        
        print("[*] Iniciando transferencia SFTP al servidor...")
        sftp = ssh.open_sftp()
        
        def sftp_progreso(transferido, total):
            porcentaje = (transferido / total) * 100
            sys.stdout.write(f"\r    Progreso: {transferido}/{total} bytes ({porcentaje:.1f}%)")
            sys.stdout.flush()
            
        sftp.put(latest_tar, ruta_remota_tar, callback=sftp_progreso)
        print("\n[*] Transferencia completada exitosamente.")
        sftp.close()
        
        print("\n[*] Ejecutando los comandos de DESTRUCCIÓN Y RECONSTRUCCIÓN remota...")
        comandos_deploy = [
            # 1. Bajar contenedores y ELIMINAR VOLÚMENES (Base de datos)
            f"cd {REMOTE_DIR}/oci-app && docker compose down -v",
            # 2. Eliminar por completo el código existente para evitar basuras
            f"rm -rf {REMOTE_DIR}/oci-app/*",
            # 3. Descomprimir el código nuevo y puro
            f"tar -xzvf {ruta_remota_tar} -C {REMOTE_DIR}",
            # 4. Limpieza agresiva de Docker (imágenes que no se usen)
            f"docker system prune -af",
            # 5. Reconstruir todo desde cero
            f"cd {REMOTE_DIR}/oci-app && docker compose up -d --build",
            # 6. Esperar a que la Base de Datos acepte conexiones (Postgres)
            f"sleep 10",
            # 7. Inicializar el usuario Admin predeterminado (admin@oci.com / oci2026)
            f"docker exec oci-app-backend-1 python init_db.py",
            # 8. Importar todo el banco de preguntas desde preguntas.json
            f"docker exec oci-app-backend-1 python importar.py",
            # 9. Renombrar paquete a .done
            f"mv {ruta_remota_tar} {ruta_remota_done}",
            # 10. Estatus final
            f"cd {REMOTE_DIR}/oci-app && docker compose ps"
        ]
        
        for comando in comandos_deploy:
            print(f"\n>>> {comando}")
            stdin, stdout, stderr = ssh.exec_command(comando)
            canal = stdout.channel
            while not canal.exit_status_ready():
                if canal.recv_ready():
                    print(canal.recv(1024).decode('utf-8', errors='ignore'), end="")
                if canal.recv_stderr_ready():
                    print(canal.recv_stderr(1024).decode('utf-8', errors='ignore'), end="")
                    
            print(stdout.read().decode('utf-8', errors='ignore'), end="")
            print(stderr.read().decode('utf-8', errors='ignore'), end="")
            
            exit_status = canal.recv_exit_status()
            if exit_status != 0:
                print(f"[!] El comando falló con código de salida: {exit_status}")
                
        print("\n[✔] DESPLIEGUE EN LIMPIO FINALIZADO EXITOSAMENTE.")
        
        try:
            done_dir = os.path.join(base_dir, "done")
            os.makedirs(done_dir, exist_ok=True)
            destino_local = os.path.join(done_dir, filename)
            shutil.move(latest_tar, destino_local)
            print(f"[*] Archivo local movido a: {destino_local}")
        except Exception as e:
            pass

    except paramiko.AuthenticationException:
        print("\n[!] Error: Falló la autenticación.")
    except Exception as e:
        print(f"\n[!] Error crítico: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    main()
