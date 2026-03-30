import paramiko
import sys

def main():
    env = {}
    with open('deployment/deploy.env') as f:
        for l in f:
            if '=' in l and not l.startswith('#'):
                k, v = l.strip().split('=', 1)
                env[k] = v
                
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    print("[*] Conectando a", env.get('HOST'))
    try:
        ssh.connect(hostname=env['HOST'], username=env['USER'], password=env['PASSWORD'], timeout=10)
    except Exception as e:
        print("Error de conexion:", e)
        sys.exit(1)

    cmds = [
        "export DEBIAN_FRONTEND=noninteractive && curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh",
        "mkdir -p /var/www/oci-app",
        "docker --version"
    ]
    
    for cmd in cmds:
        print(f">>> EJECUTANDO: {cmd}")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        
        canal = stdout.channel
        while not canal.exit_status_ready():
            if canal.recv_ready():
                sys.stdout.buffer.write(canal.recv(1024))
                sys.stdout.flush()
            if canal.recv_stderr_ready():
                sys.stderr.buffer.write(canal.recv_stderr(1024))
                sys.stderr.flush()
                
        sys.stdout.buffer.write(stdout.read())
        sys.stderr.buffer.write(stderr.read())
        
        status = canal.recv_exit_status()
        if status != 0:
            print(f"[!] Falla. Código: {status}")
            
    ssh.close()
    print("[*] Fin de Setup Remoto.")

if __name__ == '__main__':
    main()
