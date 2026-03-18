import paramiko, sys

def main():
    try:
        with open('/var/www/oci-app/deployment/deploy.env', 'r') as f:
            env_vars = dict(line.strip().split('=', 1) for line in f if '=' in line and not line.startswith('#'))
        
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=env_vars['HOST'], username=env_vars['USER'], password=env_vars['PASSWORD'], timeout=5)
        
        print("[*] SSH conected.")
        
        # Fast non-blocking command
        stdin, stdout, stderr = ssh.exec_command("docker ps -a | grep backend", timeout=5)
        print("DOCKER PS BACKEND:")
        print(stdout.read().decode())
        
        stdin, stdout, stderr = ssh.exec_command("docker logs --tail 20 oci-app-backend-1", timeout=5)
        print("BACKEND LOGS:")
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == '__main__':
    main()
