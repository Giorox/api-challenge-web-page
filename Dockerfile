FROM python:3.10
COPY requirements.txt .
RUN pip install -r requirements.txt
WORKDIR /api-challenge-web-page
CMD [ "python", "app.py"]
