import os
import glob
import sys
import subprocess
import shutil

# Auto-instalar paramiko si no está disponible en el entorno
try:
    import paramiko
except ImportError:
    print("[*] Instalando dependencia requerida (paramiko)...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "paramiko"])
    import paramiko

def cargar_env(ruta):
    """Carga variables desde un archivo .env a un diccionario."""
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
    # 1. Cargar credenciales
    base_dir = os.path.dirname(os.path.abspath(__file__))
    env_file = os.path.join(base_dir, 'deploy.env')
    env_vars = cargar_env(env_file)
    
    HOST = env_vars.get('HOST')
    USER = env_vars.get('USER')
    PASSWORD = env_vars.get('PASSWORD')
    REMOTE_DIR = '/var/www'
    
    if not all([HOST, USER, PASSWORD]):
        print("[!] Faltan credenciales (HOST, USER, o PASSWORD) en deploy.env")
        sys.exit(1)

    # 2. Localizar el paquete .tar.gz más reciente generado con el esquema de nombre oficial
    archivos_tar = glob.glob(os.path.join(base_dir, 'deploy_oci-app_*.tar.gz'))
    
    if not archivos_tar:
        print(f"[!] No se encontró ningún archivo .tar.gz de la app en {base_dir}")
        print("Por favor, empaqueta la app primero.")
        sys.exit(1)
        
    latest_tar = max(archivos_tar, key=os.path.getctime)
    filename = os.path.basename(latest_tar)
    ruta_remota_tar = f"/root/{filename}"
    
    # Crear el nombre seguro .done quitando el prefijo 'deploy_'
    filename_done = filename.replace('deploy_', '', 1) + '.done'
    ruta_remota_done = f"/root/{filename_done}"

    print(f"[*] Paquete seleccionado para despliegue: {filename}")
    print(f"[*] Iniciando conexión a {USER}@{HOST}...")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(hostname=HOST, username=USER, password=PASSWORD, timeout=10)
        print("[*] Conexión SSH establecida con éxito.")
        
        # 3. Transferencia SFTP
        print("[*] Iniciando transferencia SFTP al servidor...")
        sftp = ssh.open_sftp()
        
        def sftp_progreso(transferido, total):
            porcentaje = (transferido / total) * 100
            sys.stdout.write(f"\r    Progreso: {transferido}/{total} bytes ({porcentaje:.1f}%)")
            sys.stdout.flush()
            
        sftp.put(latest_tar, ruta_remota_tar, callback=sftp_progreso)
        print("\n[*] Transferencia completada exitosamente.")
        sftp.close()
        
        # 4. Comandos de despliegue remoto
        print("\n[*] Ejecutando los comandos de actualización en el servidor...")
        comandos_deploy = [
            # Descomprimir en /var/www
            f"tar -xzvf {ruta_remota_tar} -C {REMOTE_DIR}",
            # Bajar contenedores (usando el compose de prod)
            f"cd {REMOTE_DIR}/oci-app && docker compose -f docker-compose.prod.yaml down",
            # Limpieza (opcional, borramos dangling images para no saturar disco)
            f"docker image prune -f",
            # Recompilar y levantar
            f"cd {REMOTE_DIR}/oci-app && docker compose -f docker-compose.prod.yaml up -d --build",
            # Eliminar paquete del servidor tras éxito
            f"rm {ruta_remota_tar}",
            # Mostrar estatus final
            f"cd {REMOTE_DIR}/oci-app && docker compose -f docker-compose.prod.yaml ps"
        ]
        
        for comando in comandos_deploy:
            print(f"\n>>> {comando}")
            stdin, stdout, stderr = ssh.exec_command(comando)
            
            # Leer la salida en tiempo real (stdout y stderr)
            canal = stdout.channel
            while not canal.exit_status_ready():
                if canal.recv_ready():
                    print(canal.recv(1024).decode('utf-8', errors='ignore'), end="")
                if canal.recv_stderr_ready():
                    print(canal.recv_stderr(1024).decode('utf-8', errors='ignore'), end="")
                    
            # Vaciar buffers remanentes
            print(stdout.read().decode('utf-8', errors='ignore'), end="")
            print(stderr.read().decode('utf-8', errors='ignore'), end="")
            
            exit_status = canal.recv_exit_status()
            if exit_status != 0:
                print(f"[!] El comando falló con código de salida: {exit_status}")
                # Dependiendo de la severidad, podrías hacer sys.exit(1) aquí
                
        print("\n[✔] ACTUALIZACIÓN Y DESPLIEGUE FINALIZADO EXITOSAMENTE.")
        
        # Eliminar archivo local
        try:
            os.remove(latest_tar)
            print(f"[*] Archivo local eliminado: {latest_tar}")
        except Exception as rm_err:
            print(f"[!] No se pudo eliminar el archivo local: {rm_err}")
            
    except paramiko.AuthenticationException:
        print("\n[!] Error: Falló la autenticación. Revisa el USER y PASSWORD.")
    except Exception as e:
        print(f"\n[!] Ocurrió un error inesperado durante el despliegue: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    main()
