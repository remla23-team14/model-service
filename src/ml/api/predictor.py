import pickle
import joblib
from sklearn.naive_bayes import GaussianNB


class Predictor:

    def __init__(self, cf_file_name: str, classifier_filename: str, test_file_name: str):
        self._cv = pickle.load(open(cf_file_name, "rb"))
        self._classifier: GaussianNB = joblib.load(classifier_filename)
        with open(test_file_name, 'r') as file:
            self._training_score = float(file.read())

    def is_review_positive(self, review: str) -> bool:
        """Checks if a review is positive or negative.

        Args:
            review (str): The review to be tested if positive or negative.
                        e.g. We are so glad we found this place.

        Returns:
            bool. `true` if the review is positive, `false` otherwise.
        """
        processed_input = self._cv.transform([review]).toarray()[0]
        prediction = self._classifier.predict([processed_input])[0]
        (self._classifier.predict([processed_input]))
        return bool(prediction)

    def get_training_score(self) -> float:
        return self._training_score
