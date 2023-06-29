import dvc.api
import os
import dotenv

from ml.api.predictor import Predictor


class DVSPredictor(Predictor):

    def __init__(self):
        """A prediction object made based on online DVC's models."""
        dotenv.load_dotenv()
        print("Starting download of DVC files...")
        with self._download_dvc_file(os.getenv('DVC_PREPROCESSOR_PATH')) as preprocessor, \
                self._download_dvc_file(os.getenv('DVC_MODEL_PATH')) as model, \
                self._download_dvc_file(os.getenv('DVC_CORPUS_PATH')) as corpus, \
                self._download_dvc_file(os.getenv('DVC_METRICS_PATH'), mode="r") as metrics:
            print("Finished downloading DVC files.")
            super().__init__(preprocessor, model, corpus, metrics)

    @staticmethod
    def _download_dvc_file(file: str, mode="rb"):
        """Downloads and opens a file tracked github project.

        Args:
            file (str)
            mode (str, optional): Specifies the mode in which the file is opened. Defaults to "r" (read).
                Mirrors the namesake parameter in builtin `open()`_. Only reading `mode` is supported.

        Returns:
            _OpenContextManager: A context manager that generatse a corresponding
                `file object`_.
                The exact type of file object depends on the mode used.
                For more details, please refer to Python's `open()`_ built-in,
                which is used under the hood.

        Raises:
            AttributeError: If this method is not used as a context manager.
            ValueError: If non-read `mode` is used.
        """
        return dvc.api.open(
            file,
            repo=os.getenv('DVC_REPO'),
            rev=os.getenv('DVC_REV'),
            mode=mode
        )

