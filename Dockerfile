# Dockerfile
# Starts a flask webservice to expose the ML model
FROM python:3.11
ENV PORT="8080"
WORKDIR /root
COPY requirements.txt /root/

COPY src/ /root/src

# When building locally make sure to pull git@github.com:remla23-team14/model-training.git to a folder 'model-training'.
COPY model-training/c1_BoW_Sentiment_Model.pkl /root/
COPY model-training/c2_Classifier_Sentiment_Model /root/
COPY model-training/test_acc.txt /root/
COPY model-training/requirements.txt /root/model-training/requirements.txt
RUN pip install -r model-training/requirements.txt
RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["src/app.py"]
