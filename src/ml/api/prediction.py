class Prediction:

    def __init__(self, predicted_sentiment: bool, new_sentiment: bool = None):
        self._original_prediction = predicted_sentiment
        self._prediction = predicted_sentiment if new_sentiment is None else new_sentiment

    @property
    def prediction(self) -> bool:
        return self._prediction

    @prediction.setter
    def prediction(self, new_prediction: bool):
        self._prediction = new_prediction

    @property
    def is_correct(self) -> bool:
        return self._original_prediction == self._prediction
