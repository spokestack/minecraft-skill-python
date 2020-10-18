"""
This module contains a simple dialogue management class that generates
responses and resolves entities
"""
from fuzzywuzzy import process  # type: ignore

from minecraft import recipes
from minecraft.responses import Response


class DialogueManager:
    """Simple dialogue manager

    Args:
        threshold (float): fuzzy match threshold
    """

    def __init__(self, threshold=0.5) -> None:
        self._recipes = recipes.DB
        self._names = list(self._recipes.keys())
        self._threshold = threshold
        self._response = Response

    def __call__(self, results):
        """ Maps nlu result to a dialogue response.

        Args:
            results (dict): classification results from nlu

        Returns: a string response to be synthesized by tts

        """

        intent = results["intent"]
        if intent == "RecipeIntent":
            return self._recipe(results)
        elif intent == "AMAZON.HelpIntent":
            return self._help()
        elif intent == "AMAZON.StopIntent":
            return self._stop()
        else:
            return self._error()

    def _recipe(self, results):
        slots = results.get("slots")
        if slots:
            for key in slots:
                slot = slots[key]
                if slot["name"] == "Item":
                    return self._fuzzy_lookup(slot["raw_value"])
                return self._not_found(slot["raw_value"])
        else:
            return self._response.RECIPE_NOT_FOUND_WITHOUT_ITEM_NAME.value

    def _help(self):
        return self._response.HELP_MESSAGE.value

    def _stop(self):
        return self._response.STOP.value

    def _error(self):
        return self._response.ERROR.value

    def _fuzzy_lookup(self, raw_value):
        matched, score = process.extractOne(raw_value, self._names)

        if score > self._threshold:
            recipe = self._recipes.get(matched)
            return recipe
        return raw_value

    def _not_found(self, raw_value):
        return self._response.RECIPE_NOT_FOUND_WITH_ITEM_NAME.format(raw_value)
