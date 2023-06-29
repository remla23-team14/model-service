class Prediction:

    def __init__(self, predicted_sentiment: bool, confidence_score: float, new_sentiment: bool = None):
        """A predicton object to return a given predicted statement with its sentiment and confidence score.

        Args:
            predicted_sentiment (bool): Whether the sentiment is positive.
            confidence_score (float): A value between 0.5 and 1 how confident the given prediction is.
            new_sentiment (bool, optional): If the sentiment was corrected.
        """
        self._original_prediction = predicted_sentiment
        self._prediction = predicted_sentiment if new_sentiment is None else new_sentiment
        self._confidence_score_predicted_value = confidence_score

    @property
    def prediction(self) -> bool:
        return self._prediction

    @prediction.setter
    def prediction(self, new_prediction: bool):
        self._prediction = new_prediction

    @property
    def is_correct(self) -> bool:
        return self._original_prediction == self._prediction

    @property
    def confidence_score(self) -> float:
        return self._confidence_score_predicted_value
