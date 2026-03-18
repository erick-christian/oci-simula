# Guía de Actualización - OCI Simulador 2026

Este documento contiene las instrucciones necesarias para **actualizar** una instalación previa del Simulador de la Olimpiada del Conocimiento Infantil 2026 en un servidor remoto.

Si es la primera vez que instalas el sistema en este servidor, por favor consulta la guía `INSTRUCCIONES_DESPLIEGUE.md`.

---

## 🚀 Pasos para Instalar un Parche o Actualización

### 1. Transferencia del Nuevo Paquete
Carga el nuevo archivo `.tar.gz` (o `.tar`) con la actualización hacia tu servidor por SFTP, SCP o el método de tu preferencia. Ubícalo en la carpeta raíz del proyecto o en un lugar temporal.

### 2. Respaldar Base de Datos (Muy Recomendado)
Antes de sobreescribir los archivos, es una excelente práctica respaldar la base de datos actual para evitar pérdida de registros, resultados de alumnos o nuevas contraseñas:

```bash
cd /var/www/oci-app

# Crear el respaldo SQL de la base de datos de PostgreSQL en ejecución
docker compose exec database pg_dump -U postgres oci_db > respaldo_oci_$(date +"%Y%m%d_%H%M%S").sql
```

### 3. Detener los Servicios y Limpiar
Detén los contenedores actuales de Docker de manera segura para liberar los archivos antes de la extracción:

```bash
docker compose down
```

### 4. Extraer la Actualización
Extrae el contenido del nuevo empaquetado sobreescribiendo los archivos viejos de la aplicación. 
*(Nota: Esto no borrará tu base de datos, ya que Docker mantiene la información persistente en sus volúmenes virtuales)*:

```bash
# Extraer el contenido del empaquetado nuevo
tar -xzvf nombre-del-nuevo-archivo.tar.gz -C /var/www/

# Asegurar de que los permisos sigan siendo correctos
sudo chown -R $USER:$USER /var/www/oci-app
```

### 5. Recompilar y Levantar Contenedores
Dado que el código fuente de Python o el código del Frontend en Vue han cambiado, debes ordenarle a Docker que destruya las imágenes viejas y re-compile el nuevo código fuente antes de levantar el sistema nuevamente:

```bash
cd /var/www/oci-app

# El flag --build es crítico para que Docker detecte y compile los nuevos cambios
docker compose up -d --build
```

### 6. Verificar el Status

Una vez que termine la compilación (puede demorar un par de minutos dependiendo de la actualización de librerías del Frontend Node), verifica que todo corra correctamente:

```bash
docker compose ps
```

Si todo dice `Up`, y puedes acceder a la página web normalmente, ¡la actualización ha sido un éxito! Tu base de datos y toda su información seguirán intactos.
