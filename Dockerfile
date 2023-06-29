# Dockerfile
# Starts a flask webservice to expose the ML model
FROM python:3.11
ENV PORT="8080"
WORKDIR /root
COPY requirements.txt /root/

RUN pip install -r requirements.txt

COPY src/ /root/src
COPY development.env /root/.env

ENTRYPOINT ["python"]
CMD ["src/app.py"]
