from flasgger import Swagger
from flask import Flask, request, json, Response
from ml.api.predictor import Predictor

app = Flask(__name__)
swagger = Swagger(app)
predictor = Predictor('c1_BoW_Sentiment_Model.pkl', 'c2_Classifier_Sentiment_Model', 'test_acc.txt')


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
        "result": json.dumps(predictor.is_review_positive(msg))
    }


@app.route('/metrics', methods=['GET'])
def metrics():
    m = "# HELP training_accuracy Provides the training accuracy of the prediction model.\n"
    m += "# TYPE training_accuracy gauge\n"
    m += f"training_accuracy{{}} {predictor.get_training_score()}\n"
    return Response(m, mimetype="text/plain")


app.run(host="0.0.0.0", port=8080, debug=True)
