import paramiko, sys

def main():
    with open('/var/www/oci-app/deployment/deploy.env', 'r') as f:
        env_vars = dict(line.strip().split('=', 1) for line in f if '=' in line and not line.startswith('#'))
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=env_vars['HOST'], username=env_vars['USER'], password=env_vars['PASSWORD'], timeout=10)
    
    print("[*] Conectado exitosamente. Revisando logs de contenedores backend y frontend...\n")
    
    # Check backend logs for the 500 Internal Server error
    stdin, stdout, stderr = ssh.exec_command("docker logs --tail 30 oci-app-backend-1")
    print("=== BACKEND LOGS ===")
    print(stdout.read().decode())
    print(stderr.read().decode())
    
    # Check frontend websocket failure
    stdin, stdout, stderr = ssh.exec_command("docker logs --tail 20 oci-app-frontend-1")
    print("=== FRONTEND LOGS ===")
    print(stdout.read().decode())
    print(stderr.read().decode())
    
    ssh.close()

if __name__ == '__main__':
    main()
