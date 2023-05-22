import pickle
import joblib
from sklearn.naive_bayes import GaussianNB
from src.ml.api.prediction import Prediction


class Predictor:

    def __init__(self, cf_file_name: str, classifier_filename: str, test_file_name: str):
        self._cv = pickle.load(open(cf_file_name, "rb"))
        self._classifier: GaussianNB = joblib.load(classifier_filename)
        with open(test_file_name, 'r') as file:
            self._training_score = float(file.read())
        self._previous_predictions: dict[str, Prediction] = {}

    def is_review_positive(self, review: str, given_sentiment: bool = None) -> bool:
        """Checks if a review is positive or negative.

        Args:
            review (str): The review to be tested if positive or negative.
                        e.g. We are so glad we found this place.
            given_sentiment(str): The actual sentiment. `None` if this value is not known before hand.

        Returns:
            bool. `true` if the review is positive, `false` otherwise.
        """
        if review in self._previous_predictions:
            return self._previous_predictions.get(review).prediction
        else:
            processed_input = self._cv.transform([review]).toarray()[0]
            sentiment = bool(self._classifier.predict([processed_input])[0])
            prediction = Prediction(sentiment, given_sentiment)
            self._previous_predictions.update({review: prediction})
        return prediction.prediction

    def update_prev_prediction(self, review: str, sentiment: bool) -> bool:
        """Checks if a review is positive or negative.

        Args:
            review (str): The review for which the sentiment should be updated.
            sentiment(str): The actual new sentiment.
        Returns:
            bool. The sentiment.
        """
        if review not in self._previous_predictions:
            return self.is_review_positive(review, sentiment)
        self._previous_predictions.get(review).prediction = sentiment
        return sentiment

    @property
    def training_score(self) -> float:
        return self._training_score

    @property
    def deployment_accuracy(self) -> float:
        return [p.is_correct for p in self._previous_predictions.values()].count(True) / len(self._previous_predictions)
