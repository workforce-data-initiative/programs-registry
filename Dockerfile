
FROM python:alpine
WORKDIR /app
ADD requirements.txt .
RUN pip install -r requirements.txt
ADD . .
EXPOSE 5000
ENV FLASK_APP=app.py
CMD [ "python -m flask run" ]
