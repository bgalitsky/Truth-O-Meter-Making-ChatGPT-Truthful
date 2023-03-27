import json
import logging
import os
import pickle
import warnings
import random
from pathlib import Path

import spacy
from spacy.util import minibatch, compounding
from spacy.training import Example
from spacy.tokens.span import Span
from typing import List, Union, Dict

from tqdm import tqdm


class NamedEntityRecognizer:
    """Baseline string NER that extracts entities from raw text."""

    BASE_MODEL = "en_core_web_lg"

    def __init__(self, model_folder_path: str = None, labels: List[str] = None):
        """
        Args:
            labels: list of all entity types to be trained from. PER, ORG, etc.
        """
        if labels is None:
            labels = []
        if model_folder_path is not None:
            model_file_path = os.path.join(model_folder_path, "model.pkl")
            with open(model_file_path, "rb") as f:
                self._model = pickle.load(f)
        else:
            self._model = spacy.load(NamedEntityRecognizer.BASE_MODEL)
            # update labels
            ner = self._model.get_pipe("ner")

            for label in labels:
                # noinspection PyUnresolvedReferences
                ner.add_label(label)
        # we need to keep track of other pipes so we don't use them during train, eval and predict
        self._other_pipes = [pipe for pipe in self._model.pipe_names if pipe != 'ner']
        self._logger = logging.getLogger(__name__)

    def fit(self, training_file_path: str, n_iter: int):
        """ trains NER model on `training_file_path` for `n_iter'

        Args:
            training_file_path:
            n_iter:

        Returns:

        """
        # Loading training data
        with open(training_file_path, 'rb') as fp:
            train_data = pickle.load(fp)

        # optimizer for NER
        # noinspection PyUnresolvedReferences
        optimizer = self._model.get_pipe("ner").create_optimizer()

        # train
        with self._model.disable_pipes(*self._other_pipes), warnings.catch_warnings():  # only train NER:
            # show warnings for misaligned entity spans once
            warnings.filterwarnings("ignore", category=UserWarning, module='spacy')
            for itn in range(n_iter):
                random.shuffle(train_data)
                losses = {}
                sizes = compounding(4., 32., 1.001)
                batches = minibatch(train_data, size=sizes)
                for batch in tqdm(batches):
                    examples = []
                    for texts, annotations in batch:
                        doc = self._model.make_doc(texts)
                        try:
                            # noinspection PyArgumentList
                            example = Example.from_dict(doc, annotations)
                            examples.append(example)
                        except Exception:
                            self._logger.exception("Cannot Construct Example")
                    self._model.update(examples, sgd=optimizer, drop=0.35, losses=losses)

    def evaluate(self, eval_file_path: str) -> Dict[str, Union[float, Dict[str, float]]]:
        """runs evaluation of `nlp` model using `eval_file_path`

          Args:
              eval_file_path: str

          Returns:
              dictionary of evaluations metrics for NER and per entity types (LABEL =  CUS, ORG, PER)
              {
                'ents_f': 0.5818645640074213,
                'ents_p': 0.5689987526930491,
                'ents_per_type': {'LABEL': {'f': 0.053728578045391384,
                                            'p': 0.03550658096112642,
                                            'r': 0.11037107516650808}
                                }
                'ents_r': 0.5953256614070471,
                'speed': 22903.55629019938,
                'token_acc': 1.0,
                'token_f': 1.0,
                'token_p': 1.0,
                'token_r': 1.0
             }

          """
        # load eval data
        with open(eval_file_path, 'rb') as ep:
            eval_data = pickle.load(ep)

        with self._model.disable_pipes(*self._other_pipes), warnings.catch_warnings():  # only eval NER:
            # show warnings for misaligned entity spans once
            warnings.filterwarnings("ignore", category=UserWarning, module='spacy')
            examples = []
            for batch in minibatch(eval_data, size=compounding(4., 32., 1.001)):
                for texts, annotations in batch:
                    doc = self._model.make_doc(texts)
                    example = Example.from_dict(doc, annotations)
                    examples.append(example)
            return self._model.evaluate(examples)

    def predict(self, text: str) -> List[Span]:
        """ predicts all the entities that are present in a text after running it through pipeline.

        Args:
            text: str

        Returns:
            list[span] each span is for an entity
                use span.text, span.label
        """
        with self._model.disable_pipes(*self._other_pipes):
            doc = self._model(text)
            return [entity for entity in doc.ents]

    def save(self, save_folder: str):
        """Saves model to `save_folder/model.pkl`

        Args:
            save_folder: output folder that contains the resulting model.

        Returns:

        """
        Path(save_folder).mkdir(parents=True, exist_ok=False)
        model_file_path = os.path.join(save_folder, "model.pkl")
        with open(model_file_path, "wb") as f:
            pickle.dump(self._model, f)
        # save metadata separately
        with open(os.path.join(save_folder, "metadata.json"), "w") as f:
            json.dump(self._model.meta, f, indent=4)
        self._logger.info("Saved model to " + model_file_path)
