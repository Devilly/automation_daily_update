FROM python:3-bullseye

COPY main.py main.py
COPY .env .env
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

CMD ["python", "main.py"]