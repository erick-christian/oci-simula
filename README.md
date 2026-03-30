# 🎓 OCI 2026 - Simulador de Examen

Aplicación web interactiva diseñada para practicar exámenes de simulación para la **Olimpiada del Conocimiento Infantil (OCI)**. Ofrece una experiencia de usuario moderna y adaptada, retroalimentación inmediata, visor de referencias y un panel administrativo para seguimiento.

---

## ✨ Características Principales

### 🧑‍🎓 Panel del Estudiante
*   **Registro Intuitivo**: Carga de perfil mediante Nombre y Apellido con prevención de duplicados o pérdida de progreso.
*   **Modalidades de Examen**:
    *   **Entrenamiento**: Ideal para prácticas rápidas (ej. 30 preguntas).
    *   **Concentración**: Nivel intermedio (ej. 45 preguntas).
    *   **Maratón**: Simulación completa de alta demanda (ej. 100 preguntas).
*   **Selección Inteligente**: El sistema prioriza preguntas que el alumno **no ha visto**, rellenando con preguntas "vistas" solo si es necesario para cubrir la cuota.
*   **Gestión del Tiempo**: 
    *   Reloj de cuenta regresiva visualmente adaptado (alerta roja en zona crítica).
    *   Botón **`+5 Min`** para solicitar tiempo extra (registrado para métricas).
*   **Acciones durante el Examen**:
    *   **Saltar / Guardar para después**: Permite mover preguntas a una lista de pendientes para resolverlas al final.
    *   **Reportar Error**: Envía una alerta directa al supervisor si se detecta un fallo en el planteamiento.
*   **Visor de PDF Integrado**: Carga automática del libro/página de referencia de la SEP para consulta directa sin salir de la pregunta.
*   **Renderizado Matemático**: Soporte nativo para lectura de fórmulas complejas y ecuaciones con LaTeX (`KaTeX`).
*   **Resultados y Analíticas**:
    *   Pantallazo de calificación con medallas dinámicas (Oro, Plata, Bronce).
    *   Desglose porcentual por áreas temáticas.
    *   **Gráfica de Radar (Radar Chart)**: Histórico de rendimiento por cada área del conocimiento.
*   **Modo Oscuro (Dark Mode)**: Interfaz adaptativa que protege la vista durante prácticas nocturnas, accesible desde la pantalla de inicio.

### 🔐 Panel Administrativo
*   **Acceso Rápido**: Botón `Administrar` (🔒) estratégicamente ubicado en la esquina superior izquierda de la pantalla de registro.
*   **Acceso Protegido**: Formulario de Login para auditores y supervisores.
*   **Gestión de Configuración**:
    *   Ajuste de tiempos (minutos) y cantidad de preguntas por cada modalidad.
    *   Configuración del correo de supervisor que recibe los reportes y calificaciones.
    *   Filtros globales de generación (Generar solo preguntas con referencias validadas).
*   **Gestión de Reportes**: Listado de preguntas marcadas por alumnos. Los administradores pueden editar texto, adjuntar archivos/imágenes y marcar como "Revisado".
*   **Sistema de Notificaciones Automáticas**: El backend envía correos electrónicos HTML estructurados al supervisor cada que un alumno finaliza un simulador o cuando se reporta un reactivo dañado.
*   **Métricas Globales**: Tabla de puntuaciones históricas ordenadas por fecha y analíticas por alumno.

---

## 🚀 Tecnologías

*   **Frontend**: [Vue.js 3](https://vuejs.org/) (Composition API), [Vite](https://vitejs.dev/), [Tailwind CSS](https://tailwindcss.com/), [Chart.js](https://www.chartjs.org/) (Gráficas).
*   **Backend**: [Python 3](https://www.python.org/) con [Flask](https://flask.palletsprojects.com/) y [SQLAlchemy](https://www.sqlalchemy.org/).
*   **Base de Datos**: [PostgreSQL](https://www.postgresql.org/).
*   **PWA**: Soporte para instalación como aplicación nativa y Service Workers optimizados para cache y fallbacks.
*   **Infraestructura**: Docker y Docker Compose (Escenarios Dev y Producción).

---

## 📋 Requisitos Previos

Asegúrate de tener instalado en tu sistema:
*   [Docker](https://docs.docker.com/get-docker/)
*   [Docker Compose](https://docs.docker.com/compose/install/)

---

## 🛠️ Instalación y Ejecución 

### 🟢 Modo Desarrollo (Local)
1. Para levantar componentes en sucursales de desarrollo con hot-reload:
   ```bash
   docker compose up -d --build
   ```
2. Accesos:
   *   **Frontend**: `http://localhost:8077` (Mapeado a Vite en 5173)
   *   **Backend API**: `http://localhost:5000`

### 🔵 Modo Producción
Para desplegar sobre un servidor con Nginx integrado y empaquetado optimizado:
```bash
docker compose -f docker-compose.prod.yaml up -d --build
```

---

## 📥 Importación de Datos

Las preguntas del simulador están preparadas para cargarse a partir del archivo `preguntas.json`. **En este caso, se utilizó Inteligencia Artificial para destilar PDFs de cuestionarios reales y extraer/construir esta información.**

Una vez que los contenedores estén corriendo, usa el script helper para poblar la base de datos:
```bash
docker compose exec backend python importar.py
```

---

## 📂 Estructura Clave

*   **`/backend`**: API Flask. `app.py` contiene modelos y la lógica de negocio.
*   **`/frontend`**: Interfaz Vue 3. 
    *   `src/components/TarjetaReactivo.vue`: Lógica principal del examen e iframe visualizador.
*   **`/frontend/public/referencias`**: Almacén principal de PDFs de soporte para preguntas.
*   **`/deployment`**: Scripts de empaquetado y subida vía SSH/SFTP (`do_deploy.py`).

---

## ☁️ CUBEPATH (Infraestructura de Producción)

La aplicación se encuentra lista y liberada para funcionar en un **VPS tipo gp.micro**.
*   **Recursos**: 2 vCPU, 4 GB RAM, 80 GB SSD y 5 TB de transferencia.
*   **Demo Online**: [http://midudev.terian.com.mx](http://midudev.terian.com.mx)
