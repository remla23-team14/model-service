from flasgger import Swagger
from flask import Flask, request
from ml.api.predictor import Predictor

app = Flask(__name__)
swagger = Swagger(app)
predictor = Predictor('c1_BoW_Sentiment_Model.pkl', 'c2_Classifier_Sentiment_Model')

@app.route('/', methods=['POST'])
def predict():
    """
    Make a hardcoded prediction
    ---
    consumes:
      - application/json
    parameters:
        - name: input_data
          in: body
          description: message to be classified.
          required: True
          schema:
            type: object
            required: sms
            properties:
                msg:
                    type: string
                    example: This is an example msg.
    responses:
      200:
        description: Some result
    """
    msg = request.get_json().get('msg')
    return {
        "message": "Message was: " + msg,
        "result": predictor.review_classification(msg)
    }

app.run(host="0.0.0.0", port=8080, debug=True)
