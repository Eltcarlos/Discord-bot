FROM python:3.9

# Instala ffmpeg
RUN apt update && \
    apt install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

COPY . /app

WORKDIR /app

# Instala las dependencias si tienes un archivo requirements.txt
RUN pip install -r requirements.txt

# Activa el entorno virtual
RUN python -m venv venv
RUN /bin/bash -c "source venv/bin/activate"

# Ejecuta el archivo main.py
CMD ["python", "main.py"]
