
FROM python:alpine
WORKDIR /app
ADD requirements.txt .
RUN pip install -r requirements.txt
ADD . .
EXPOSE 5000
CMD [ "python3", "app.py" ]
