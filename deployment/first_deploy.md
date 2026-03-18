# Guía de Despliegue - OCI Simulador 2026

Este documento contiene las instrucciones necesarias para desplegar el Simulador de la Olimpiada del Conocimiento Infantil 2026 en un servidor remoto de producción tipo Linux (Ubuntu/Debian recomendado).

## Prerrequisitos del Servidor

El servidor de destino deberá contar con los siguientes programas instalados:

1. **Docker Engine**: Para contenerizar tanto el Frontend (Nginx/Vite) como el Backend (Python/Flask) y la Base de Datos.
2. **Docker Compose**: Para orquestar los tres contenedores y su red de comunicación.

Si no cuentas con ellos, instálalos ejecutando:

```bash
# Actualizar repositorios e instalar utilidades
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg lsb-release

# Añadir llave gpg oficial de Docker
sudo mkdir -m 0755 -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Configurar el repositorio
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalar Docker y Docker Compose
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Agregar tu usuario al grupo docker (opcional para no usar sudo constantemente)
sudo usermod -aG docker $USER
```

---

## 🚀 Pasos para Desplegar la Aplicación

### 1. Transferencia y Extracción
Carga el archivo `oci-app-YYYYMMDD_HHMMSS.tar.gz` hacia tu servidor por SFTP, SCP o el método de tu preferencia.

Descomprime el archivo transferido en el directorio donde vivirá tu aplicación (ej. `/var/www/` o `/opt/`):

```bash
# Crea el directorio principal
sudo mkdir -p /var/www/oci-app
sudo chown $USER:$USER /var/www/oci-app

# Extrae el contenido del empaquetado
tar -xzvf oci-app-*.tar.gz -C /var/www/
cd /var/www/oci-app
```

### 2. Levantamiento de Contenedores

La aplicación ha sido configurada en un ecosistema encapsulado `docker-compose.yaml` para su levantamiento con un sólo comando.

Ejecuta el siguiente comando dentro de `/var/www/oci-app` para compilar y levantar los servicios en modo administrador desprendido (background):

```bash
docker compose up -d --build
```

Esto levantará los siguientes módulos de red:
- **`database`**: Un contenedor oficial de PostgreSQL exponiendo el puerto 5432.
- **`backend`**: Una API Flask procesando la información de la base de datos en el puerto 5000.
- **`frontend`**: Una aplicación en Nginx/Vite sirviendo archivos estáticos optimizados en el **puerto 80**.

### 3. Verificar el Status

Verifica que no exista ningún contenedor caído o en estado de reinicio:

```bash
docker compose ps
```

Puedes ver los troncos de ejecución en vivo en caso de que ocurra algún error del lado del servidor del Maestro:

```bash
docker compose logs -f backend
```

---

## 🔗 Acceder al Simulador

Si tu servidor está expuesto al internet (o es red local), abre un navegador y dirígete directamente a la **IP Pública** o **Dominio** adjuntado a este servidor por el puerto `80`.

Ejemplo: `http://192.168.1.50/` o `http://tudominio.com/`

### Crear Sesión de Administrador
La primera vez que el contenedor `backend` se levanta, ejecutará automáticamente el script `init_db.py` e inyectará en la base de datos la cuenta predeterminada:
* **Correo**: `admin@oci.com`
* **Contraseña**: `oci2026`

Se recomienda encarecidamente cambiar esta contraseña dentro del panel una vez logeados o modificando la tabla desde algún cliente SQL.
