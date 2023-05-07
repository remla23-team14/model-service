import pickle
import joblib


class Predictor:

    def __init__(self, cf_file_name: str, classifier_filename: str):
        self._cv = pickle.load(open(cf_file_name, "rb"))
        self._classifier = joblib.load(classifier_filename)
        self._prediction_map = {
            0: "negative",
            1: "positive"
        }

    def review_classification(self, review: str):
        """Checks if a review is positive or negative.

        Args:
            review (str): The review to be tested if positive or negative.
                        e.g. We are so glad we found this place.

        Returns:
            str. Feedback over the review.
        """
        processed_input = self._cv.transform([review]).toarray()[0]
        prediction = self._classifier.predict([processed_input])[0]
        return f"The model believes the review is {self._prediction_map[prediction]}."
