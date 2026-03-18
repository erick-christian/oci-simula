import paramiko, sys

def main():
    with open('/var/www/oci-app/deployment/deploy.env', 'r') as f:
        env_vars = dict(line.strip().split('=', 1) for line in f if '=' in line and not line.startswith('#'))
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=env_vars['HOST'], username=env_vars['USER'], password=env_vars['PASSWORD'], timeout=10)
    
    print("[*] Conectado exitosamente. Revisando estado de docker...")
    
    stdin, stdout, stderr = ssh.exec_command("cd /var/www/oci-app && docker compose ps")
    print(stdout.read().decode())
    
    # check backend logs more broadly
    stdin, stdout, stderr = ssh.exec_command("docker logs oci-app-backend-1 --tail 50")
    print("BACKEND LOGS:")
    print(stdout.read().decode())
    print(stderr.read().decode())
    
    ssh.close()

if __name__ == '__main__':
    main()
