import pickle
import joblib


class Predictor:

    def __init__(self, cf_file_name: str, classifier_filename: str):
        self._cv = pickle.load(open(cf_file_name, "rb"))
        self._classifier = joblib.load(classifier_filename)

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
        return bool(prediction)
