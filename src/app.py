import os

from flasgger import Swagger
from flask import Flask, request, json, Response

from ml.api.dvs_predictior import DVSPredictor
from ml.api.predictor import Predictor
from dotenv import load_dotenv

app = Flask(__name__)
swagger = Swagger(app)
training_loc = 'model-training/'
global predictor


def generate_predictor(use_dvc: bool = False) -> Predictor:
    """Makes a predictor object based on mounted files or the latest DVC file.

    This method uses local files if they can all be found it `training_loc` location under the correct name, otherwise
    it uses DVC.

    Args:
        use_dvc (bool, optional): If positive it doesn't even check if local files can be found and use DVC immediately.

    Returns:
        predictor. To be used to predict the sentiment of reviews.
    """
    if use_dvc: return DVSPredictor()
    preprocessor = training_loc + "c1_BoW_Sentiment_Model.joblib"
    found_preprocessor = os.path.isfile(preprocessor)
    model = training_loc + "c2_Classifier_Sentiment_Model"
    found_model = os.path.isfile(model)
    corpus = training_loc + "pre_processed_dataset.joblib"
    found_corpus = os.path.isfile(corpus)
    metrics = training_loc + "model_metrics.json"
    found_metrics = os.path.isfile(metrics)
    if found_preprocessor and found_model and found_corpus and found_metrics:
        print("Using own files...")
        with open(metrics, "r") as metrics_f:
            return Predictor(preprocessor, model, corpus, metrics_f)
    else:
        if found_preprocessor or found_model or found_corpus or found_metrics:
            print("Only some of the necessary files can be found...\n"
                  f"\t {'Found' if found_preprocessor else 'Missing'} preprocessor at '{preprocessor}'"
                  f"\t {'Found' if found_model else 'Missing'} model at '{preprocessor}'"
                  f"\t {'Found' if found_corpus else 'Missing'} corpus at '{preprocessor}'"
                  f"\t {'Found' if found_metrics else 'Missing'} metrics at '{preprocessor}'"
                  )
        return DVSPredictor()


@app.route('/predict', methods=['POST'])
def predict():
    """
    Make a prediction on the sentiment of a review based on a trained model.
    ---
    tags:
      - Sentiment
    consumes:
      - application/json
    parameters:
        - name: input_data
          in: body
          description: Review to be classified.
          required: True
          schema:
            type: object
            required: review
            properties:
                review:
                    type: string
                    example: We are glad we found this place.
    responses:
      200:
        description: Response with updated sentiment.
        content:
          application/json:
            schema:
              type: object
              properties:
                review:
                  type: string
                  example: We are glad we found this place.
                sentiment:
                  type: boolean
                  example: true
    """
    review = request.get_json().get('review')
    return {
        "review": review,
        "sentiment": json.dumps(predictor.is_review_positive(review))
    }


@app.route('/toggle-sentiment', methods=['POST'])
def toggle_sentiment():
    """
    A feedback endpoint to check if a previous prediction was incorrect.
    ---
    tags:
      - Sentiment
    consumes:
      - application/json
    parameters:
        - name: input_data
          in: body
          description: Sentiment of review to be updated.
          required: True
          schema:
            type: object
            required: review
            properties:
                review:
                    type: string
                    example: We are glad we found this place.
                sentiment:
                    type: boolean
                    example: 'true'
    responses:
      200:
        description: Response with updated sentiment.
        content:
          application/json:
            schema:
              type: object
              properties:
                review:
                  type: string
                  example: We are glad we found this place.
                sentiment:
                  type: boolean
                  example: true
    """
    review = request.get_json().get('review')
    sentiment = json.loads(request.get_json().get('sentiment'))
    sentiment = predictor.update_prev_prediction(review, sentiment)
    # TODO update accuracy,
    return {
        "review": review,
        "sentiment": json.dumps(sentiment)
    }


@app.route('/metrics', methods=['GET'])
def metrics():
    """
    Provides the metrics of the model-service in a Prometheus scrapable format.
    ---
    tags:
      - Metrics
    responses:
      200:
        description: Metrics data in Prometheus format.
        content:
          text/plain:
            schema:
              type: string
              example: |
                # HELP training_accuracy Provides the training accuracy of the prediction model.
                # TYPE training_accuracy gauge
                training_accuracy{} 0.9916666666666667
                # HELP deployment_accuracy Provides the actual accuracy of the prediction model.
                # TYPE deployment_accuracy gauge
                deployment_accuracy{} 0.0
                # HELP last_confidence_score Provides the confidence score of the most recently added review.
                # TYPE last_confidence_score gauge
                last_confidence_score{} 0.0
    """
    m = "# HELP training_accuracy Provides the training accuracy of the prediction model.\n"
    m += "# TYPE training_accuracy gauge\n"
    m += f"training_accuracy{{}} {predictor.training_score}\n"
    m += "# HELP deployment_accuracy Provides the actual accuracy of the prediction model.\n"
    m += "# TYPE deployment_accuracy gauge\n"
    m += f"deployment_accuracy{{}} {predictor.deployment_accuracy}\n"
    m += "# HELP last_confidence_score Provides the confidence score of the most recently added review.\n"
    m += "# TYPE last_confidence_score gauge\n"
    m += f"last_confidence_score{{}} {predictor.last_confidence_score}\n"
    return Response(m, mimetype="text/plain")


if __name__ == '__main__':
    load_dotenv()
    predictor = generate_predictor(os.getenv("USE_DVC", 'False').lower() in ('true', '1', 't'))
    app.run(host="0.0.0.0", port=os.getenv('PORT', 8080), debug=True)
