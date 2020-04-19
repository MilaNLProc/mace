from typing import Dict, List
import pandas as pd

from app.forms import MaceForms
from app.mace.config import FILLER, PRIORS_COL_NAME, CONTROLS_COL_NAME
from app.mace.config import (
    ALPHA, BETA, EM, MAX_ITERATIONS, RESTARTS, THRESHOLD
)


class MaceInputs(object):
    f"""
    Collects inputs to feed to MACE.

    Sets parameters and computes basic stats

    Parameters
    ----------
    inputfile : pandas.core.frame.DataFrame
        Name of the input file
    priors : Dict
        File name for prior likelihood of each label
    controls : List
        List of length inputfile.shape[0] with the true annotation
    alpha : float alpha > 0 defaults to {ALPHA}
        For VB, alpha parameter of the beta prior distribution
    beta : float beta > 0 defaults to {BETA}
        For VB, beta parameter of the beta prior distribution
    em : bool defalts to {EM}
        Flag to use EM training instead of VB
    iterations : int iterations > 0 defaults to {MAX_ITERATIONS/10}
        Number of training iterations
    restarts : int restarts > 0 defaults to {RESTARTS}
        Number of random restarts
    threshold : float threshold > 0 defaults to {THRESHOLD}
        Percentage of instances (ordered by entropy) to keep
    smoothing : float smoothing > 0 defaults to 0.01/num_labels
        Smoothing parameter
    """

    def __init__(self, form: MaceForms):
        self.inputfile = pd.read_excel(
            form.inputfile.data, dtype=str
        ).fillna(FILLER)
        self.priors = self.get_priors(form)
        self.controls = self.get_controls(form)
        self.alpha = self._naive_check(form.alpha, ALPHA)
        self.beta = self._naive_check(form.beta, BETA)
        self.em = EM
        self.iterations = self._naive_check(form.iterations, MAX_ITERATIONS/10)
        self.restarts = self._naive_check(form.restarts, RESTARTS)
        self.threshold = self._naive_check(form.threshold, THRESHOLD)
        self.smoothing = form.smoothing  # no check: default computed in Mace
        self.email = str(form.email)

    @staticmethod
    def _naive_check(in_, default):
        if in_ is not None:
            return in_
        return default

    def get_priors(self, form: MaceForms) -> Dict:

        if form.priorsfile.data is None:
            return {}

        priors = pd.read_excel(form.file.priors, dtype=str)
        annotations = priors.columns.to_list()
        annotations.remove(PRIORS_COL_NAME)

        # DataFrame to Dict {annotation: prior}
        results = priors.set_index(annotations).T.to_dict('records')[0]

        # convert priors to float
        results = {str(k): float(v) for k, v in results.items()}

        return results

    def get_controls(self) -> List:

        if CONTROLS_COL_NAME in self.inputfile.columns:

            results = self.inputfile[CONTROLS_COL_NAME].values.to_list()

            # drop CONTROLS column in self.inputfile
            self.inputfile.drop(CONTROLS_COL_NAME, axis=1, inplace=True)

            return results

        return []
