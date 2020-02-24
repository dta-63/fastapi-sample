FROM python:3.7
ADD . /app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8080
CMD ["python", "main.py"]