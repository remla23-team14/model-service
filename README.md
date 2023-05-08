# model-service
This service provides an API endpoint so that one can check 
if reviews are positive or negative.

## Service start-up
The best way to start the service is through the released docker images.
To run the latest version:
```sh
docker run --rm -it -p8080:8080 ghcr.io/remla23-team14/model-service:latest
```

### Start-up locally
One can also start of the service locally by following these steps:
1. Download python dependencies: `pip install -r requirements.txt`
2. Download the following ML models from [https://github.com/remla23-team14/model-training](), 
   and copy them to this repository:
    1. 'c1_BoW_Sentiment_Model.pkl'
    2. 'c2_Classifier_Sentiment_Model'
3. Run it by calling `python src/app.py`

## Service querying 
You can then query the service **after starting it** to see if a review is positive or negative by either:
* Going to [http://localhost:8080/apidocs]() and interacting with the swagger api.
* Using curl: `curl -X POST "http://localhost:8080/" -H  "accept: application/json" -H  
  "Content-Type: application/json" -d "{  \"msg\": \"Paste your review here.\"}"`
* Or performing POST on "http://localhost:8080/" with json body containing the msg.

## Set up the docker images yourself
If you wish to build the image yourself you first need to clone [https://github.com/remla23-team14/model-training]() 
to a new folder called 'model-training'.


    
