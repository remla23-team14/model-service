# Downloading the trained models
If you don't want to pull the newest model through DVC everytime you can manually build them.
However, if you want to only download a specific file of DVC or you want to be able to run 
the app without internet access you can download them beforehand with help of DVC.

### DVC in your python enviroment
First make sure you have DVC and all other dependencies in the `requirements.txt` installed in your python virtual
environment. This can be done with:

```shell
pip install -r requirements.txt
```

### Pulling the files
```shell
cd <path_to_model-service_root>

# For the preprocessor:
dvc get -o model-training/c1_BoW_Sentiment_Model.joblib git@github.com:remla23-team14/model-training.git data/processed/c1_BoW_Sentiment_Model.joblib

# For the model:
dvc get -o model-training/c2_Classifier_Sentiment_Model git@github.com:remla23-team14/model-training.git models/c2_Classifier_Sentiment_Model

# For the corpus:
dvc get -o model-training/pre_processed_dataset.joblib git@github.com:remla23-team14/model-training.git data/processed/pre_processed_dataset.joblib

# For the metrics:
dvc get -o model-training/model_metrics.json git@github.com:remla23-team14/model-training.git data/output/model_metrics.json

```

