FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=run.py

EXPOSE 8080

# Run database migrations before starting the app
CMD ["sh", "-c", "flask db upgrade && gunicorn --bind 0.0.0.0:8080 run:app"]
