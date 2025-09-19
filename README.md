# 📥 Descargador de Videos con Flask + yt-dlp

Este proyecto es una aplicación web en **Python (Flask)** que permite descargar videos desde YouTube (u otras plataformas soportadas por `yt-dlp`) directamente desde el navegador.  

Incluye:  
- Interfaz web con **modo oscuro**.  
- **Logo clicable** que redirige a la página principal.  
- Manejo de archivos duplicados (permite renombrar si ya existe).  
- **Barra de progreso en tiempo real** mientras se descarga.  
- Botón para **descargar el archivo** una vez completado.

---

## 🚀 Requisitos

- Python 3.8+
- pip
- Virtualenv (opcional, pero recomendado)

---

## 📦 Instalación

1. Clona o descarga este repositorio.  
   ```bash
   git clone https://github.com/DexterTavarez/descargador_web.git
   cd descargador_web
   ```

2. Crea y activa un entorno virtual:  
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

3. Instala las dependencias:  
   ```bash
   pip install flask yt-dlp
   ```

---

## ▶️ Uso

1. Inicia la aplicación:  
   ```bash
   python app.py
   ```

2. Abre tu navegador en:  
   ```
   http://127.0.0.1:5000
   ```

3. Ingresa la **URL del video** y presiona **Descargar**.  

---

## 📂 Estructura del proyecto

```
descargador_web/
│── app.py                # Código principal Flask
│── videos/               # Carpeta donde se guardan los videos
│── templates/            # HTMLs
│   ├── index.html        # Página principal
│   ├── confirm.html      # Confirmación si el archivo ya existe
│   ├── progress.html     # Barra de progreso
│── static/               # Archivos estáticos
│   ├── style.css         # Estilos (incluye modo oscuro)
│   ├── darkmode.js       # Script de modo oscuro
│   ├── logo.png          # Logo de la app
```

---

## 🌙 Modo oscuro

- Se activa con el botón **🌙 / ☀️** en la esquina superior derecha.  
- La preferencia de tema se guarda en el navegador (localStorage).  

---

## 📊 Barra de progreso

- Mientras el video se descarga, se muestra una **barra animada**.  
- Al llegar al **100%**, aparece un botón para descargar el archivo.  

---

## ⚠️ Nota

> ⚠️ Esta aplicación está pensada para **uso personal y educativo**.  
> No la uses para descargar contenido con copyright sin permiso.  
