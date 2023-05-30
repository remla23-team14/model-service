import json
import typing

import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import GaussianNB
from ml.api.prediction import Prediction


class Predictor:

    def __init__(self, preprocessor, model, corpus, metrics_file):
        """A predictor object to predict the sentiment of reviews.

        Args:
            preprocessor (str, pathlib.Path, or file object):
                The file object or path of the file from which to load the preprocessor as CountVectorizer.
            model (str, pathlib.Path, or file object):
                The file object or path of the file from which to load the classifier as GaussianNB.
            metrics_file (file object): Of an JSON file containing the info for accuracy.train as a float.
        """
        self._preprocessor: CountVectorizer = joblib.load(preprocessor)
        self._preprocessor.fit_transform(joblib.load(corpus))  # Not sure why this is needed.
        self._classifier: GaussianNB = joblib.load(model)
        self._training_score = float(json.load(metrics_file)["accuracy"]["train"])
        self._previous_predictions: dict[str, Prediction] = {}
        self._last_prediction: typing.Optional[Prediction] = None
        print("Done initializing prediction model")

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
            processed_input = self._preprocessor.transform([review]).toarray()[0]
            sentiment = bool(self._classifier.predict([processed_input])[0])
            confidence_score = float((self._classifier.predict_proba([processed_input])[0]).max())
            prediction = Prediction(sentiment, confidence_score, given_sentiment)
            self._last_prediction = prediction
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
        if not self._previous_predictions: return 0.0
        return [p.is_correct for p in self._previous_predictions.values()].count(True) / len(self._previous_predictions)

    @property
    def last_confidence_score(self) -> float:
        if self._last_prediction is None: return 0.0
        return self._last_prediction.confidence_score
