# Contexto del Proyecto: OCI Simulador (Olimpiadas de Conocimiento Infantil)

Este archivo sirve como ancla de memoria estructural tanto para desarrolladores humanos como para asistentes de IA.

## 🎯 Propósito General
La aplicación es un simulador de exámenes interactivo diseñado para estudiantes. Permite realizar pruebas con diferentes áreas de conocimiento (Matemáticas, Español, etc.), reportar errores en las preguntas, ganar medallas basadas en el rendimiento, solicitar tiempo extra, y revisar detalladamente el progreso mediante gráficas. También cuenta con un Panel de Administración seguro para gestionar reactivos, aprobar/rechazar reportes de error y monitorear el rendimiento global.

## 🏗 Arquitectura del Sistema
- **Frontend:** Vue.js 3 (Composition API) + Vite.
  - PWA (Progressive Web App) configurada.
  - Gestión de estado ligero y enrutamiento con vue-router.
  - Renderizado de Matemáticas con KaTeX.
- **Backend:** Python (Flask) + SQLAlchemy (ORM).
  - API RESTful bajo `/api/...`.
  - CORS habilitado para comunicación cruzada (y proxy Nginx en Producción).
- **Base de Datos:** PostgreSQL 15.
- **Infraestructura & Despliegue:** 
  - Contenedores Docker orquestados con `docker-compose.yaml`.
  - Empaquetado en `.tar.gz` para envíos automáticos vía scripts SFTP (`deployment/do_deploy.py`).

## 🔑 Funcionalidades Clave Añadidas Recientemente
1. **Sistema de Medallas y Exclusión de Errores:** Exclusión de preguntas reportadas del puntaje final y recompensas visuales (Oro/Plata/Bronce).
2. **Dashboard de Rendimiento:** Un histórico gráfico para el Alumno y Administrador sobre puntajes máximos por materia y tiempos extras solicitados.
3. **Solicitar Más Tiempo / Guardar para Después:** Lógica para brindar 5 mins extra y permitir saltar preguntas para contestarlas al final.
4. **Login de Administradores:** Protección del panel administrativo mediante un esquema de usuarios (`admin@oci.com`) en la Base de Datos.
5. **PDF Reference Reader:** Lector embebido de libros de texto como referencia a las preguntas de examen.
6. **Visor Automático de Datos Extra & Relaciones:** Renderización dinámica de tablas y textos anidados complejos para problemas de lectura y relación de columnas.

## 🚀 Guías de Utilidad
- **Instalación Fresca:** Consultar `/deployment/first_deploy.md`.
- **Actualización Rápida:** Ejecutar `deployment/do_deploy.py` para sincronizar cambios locales al servidor remoto en caliente. (Documentado en `reload_deploy.md`).
- **Base de Datos:** Script de inicialización disponible en `db/init.sql`.
