FROM python:3.8-slim-buster

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
#RUN echo "10.206.26.2 database.microgen.gudanggaramtbk.com database-core.microgen.gudanggaramtbk.com database-query.microgen.gudanggaramtbk.com database-stream.microgen.gudanggaramtbk.com database-upload.microgen.gudanggaramtbk.co" | tee -a /etc/hosts

EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Add SSL certificate and key files
COPY cert.pem /app
COPY key.pem /app

#ENV FLASK_RUN_HOST=0.0.0.0

#CMD ["python3", "-m", "flask", "run"]

# Run the Flask application
CMD ["flask", "run", "--cert=cert.pem", "--key=key.pem"]
