FROM python:3.11-slim


ADD ./requirements.txt /app/requirements.txt
WORKDIR /app

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt


ADD ./src/ /app/

EXPOSE 8080

CMD ["python", "run.py"]