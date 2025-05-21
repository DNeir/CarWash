

# 🚗 CarWash 
## Sistema de Gestión de Lavado de Autos

**CarWash** es una aplicación web construida con Django para gestionar un negocio de lavado de autos. Permite registrar clientes, vehículos, empleados, servicios y agendar citas para realizar lavados.

---

## 🧾 Características

- Registro de clientes y sus vehículos
- Gestión de empleados
- Administración de servicios ofrecidos (lavado, encerado, etc.)
- Agendamiento de citas
- Relación entre vehículos, empleados y servicios
- Interfaz web básica con HTML + CSS

---

## 🏗️ Estructura del Proyecto

```plaintext
CarWash/
├── CarWash/            # Configuración principal del proyecto Django
├── DbWash/             # Aplicación principal con modelos y lógica
│   └── models.py       # Definición de la base de datos
├── templates/          # Archivos HTML para la interfaz
├── static/             # Archivos CSS e imágenes
├── db.sqlite3          # Base de datos local (SQLite)
├── manage.py           # Script principal para ejecutar comandos Django
``` 
## 💾 Requisitos
Python 3.8+
Django 4.x
Puedes instalar los requisitos con:

```plaintext
pip install -r requirements.txt
```
(Si no tienes el archivo requirements.txt, usa: pip install django)
(No olvides crear el entorno de python en caso de usar VSCode)

## 👨‍💻 ¿Qué puedes hacer?
Registros y utenticacion de usuarios y vehículos

Crear servicios personalizados

Programacion de citas para lavado de vehiculos

Consultar registros desde el panel de administración de Django

Panel de administración para gestionar servicios

Para entrar al panel de administración:
```plaintext
python manage.py createsuperuser
```

## 🚀 Cómo Ejecutar el Proyecto
Clona el repositorio:

```plaintext
git clone https://github.com/DNeir/CarWash.git
cd CarWash
```
La app ya cuenta con las migraciones necesarias
Inicia el servidor de desarrollo:

```plaintext
python manage.py runserver
```
Abre tu navegador en:

```plaintext
http://127.0.0.1:8000/
```
## 📄 Licencia
Este proyecto está bajo la licencia **MIT**.
