# Dockerfile
# Starts a flask webservice to expose the ML model
FROM python:3.11
ENV PORT="8080"
WORKDIR /root
COPY requirements.txt /root/

COPY src/ /root/src

# When building locally make sure to have updated your submodules.
COPY model-training/c1_BoW_Sentiment_Model.pkl /root/model-training/c1_BoW_Sentiment_Model.pkl
COPY model-training/c2_Classifier_Sentiment_Model /root/model-training/c2_Classifier_Sentiment_Model
COPY model-training/test_acc.txt /root/model-training/test_acc.txt
COPY model-training/requirements.txt /root/model-training/requirements.txt

RUN pip install -r model-training/requirements.txt
RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["src/app.py"]
