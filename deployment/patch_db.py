import paramiko, sys

def main():
    with open('/var/www/oci-app/deployment/deploy.env', 'r') as f:
        env_vars = dict(line.strip().split('=', 1) for line in f if '=' in line and not line.startswith('#'))
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=env_vars['HOST'], username=env_vars['USER'], password=env_vars['PASSWORD'], timeout=10)
    
    print("[*] Conectado exitosamente. Aplicando parche SQL al contenedor db...")
    sql_command = "ALTER TABLE configuracion ADD COLUMN IF NOT EXISTS filtro_referencia VARCHAR;"
    cmd = f'docker exec oci-app-db-1 psql -U admin -d oci_db -c "{sql_command}"'
    
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print("Salida STDOUT:", stdout.read().decode())
    print("Salida STDERR:", stderr.read().decode())
    
    # Check what else might be missing to be sure based on recent local features
    # Let's just make sure as well that "Usuario" table and Reactivo.revisado_por exists.
    # The init.sql was updated locally but production db volumes persist across deployments.
    cmd_usuario = '''docker exec oci-app-db-1 psql -U admin -d oci_db -c "
        CREATE TABLE IF NOT EXISTS usuario (
            id SERIAL PRIMARY KEY,
            username VARCHAR UNIQUE NOT NULL,
            password_hash VARCHAR NOT NULL,
            rol VARCHAR NOT NULL
        );
        ALTER TABLE reactivo ADD COLUMN IF NOT EXISTS revisado_por VARCHAR;
        ALTER TABLE resuelto ADD COLUMN IF NOT EXISTS tiempo_extra_minutos INTEGER DEFAULT 0;
        ALTER TABLE reactivo ADD COLUMN IF NOT EXISTS referencia VARCHAR;
        ALTER TABLE reactivo ADD COLUMN IF NOT EXISTS pagina VARCHAR;
    "'''
    stdin, stdout, stderr = ssh.exec_command(cmd_usuario)
    print("\nAplicando schema extra (si faltaba persistencia):")
    print(stdout.read().decode())
    print(stderr.read().decode())
    
    ssh.close()

if __name__ == '__main__':
    main()
