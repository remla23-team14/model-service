# Dockerfile
# Starts a flask webservice to expose the ML model
FROM python:3.7-slim
WORKDIR /root
COPY requirements.txt /root/
RUN pip install -r requirements.txt

COPY app.py /root/
COPY ml/ /root/ml

# TODO Change this to retrieve the model from somewhere else.
COPY c1_BoW_Sentiment_Model.pkl /root/
COPY c2_Classifier_Sentiment_Model /root/

ENTRYPOINT ["python"]
CMD ["app.py"]