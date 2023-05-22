import os

from flasgger import Swagger
from flask import Flask, request, json, Response
from ml.api.predictor import Predictor
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
swagger = Swagger(app)
training_loc = 'model-training/'
predictor = Predictor(training_loc+'c1_BoW_Sentiment_Model.pkl', training_loc+'c2_Classifier_Sentiment_Model',
                      training_loc+'test_acc.txt')


@app.route('/predict', methods=['POST'])
def predict():
    """
    Make a prediction on the sentiment of a review based on a trained model.
    ---
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
        description: TODO
    """
    review = request.get_json().get('review')
    return {
        "msg": "The given review was: " + review,
        "sentiment": json.dumps(predictor.is_review_positive(review))
    }


@app.route('/toggle-sentiment', methods=['POST'])
def toggle_sentiment():
    """
    A feedback endpoint to check if a previous prediction was incorrect.
    ---
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
        description: TODO
    """
    review = request.get_json().get('review')
    sentiment = json.loads(request.get_json().get('sentiment'))
    sentiment = predictor.update_prev_prediction(review, sentiment)
    # TODO update accuracy,
    return {
        "msg": "The given review was: " + review,
        "sentiment": json.dumps(sentiment)
    }


@app.route('/metrics', methods=['GET'])
def metrics():
    m = "# HELP training_accuracy Provides the training accuracy of the prediction model.\n"
    m += "# TYPE training_accuracy gauge\n"
    m += f"training_accuracy{{}} {predictor.training_score}\n"
    m += f"deployment_accuracy{{}} {predictor.deployment_accuracy}\n"
    return Response(m, mimetype="text/plain")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=os.getenv('PORT', 8080), debug=True)
