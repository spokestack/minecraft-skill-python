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
        self._threshold = threshold

    def __call__(self, results):
        """ Maps nlu result to a dialogue response.

        Args:
            results (dict): classification results from nlu

        Returns: a string response to be synthesized by tts

        """

        intent = results["intent"]
        if intent == "RecipeIntent":
            slots = results.get("slots")

            if slots:
                for key in slots:
                    slot = slots[key]
                    if slot["name"] == "Item":

                        matched, score = process.extractOne(
                            slot["raw_value"], list(self._recipes.keys())
                        )
                        if score > self._threshold:
                            recipe = self._recipes.get(matched)
                            return recipe
                        return Response.RECIPE_NOT_FOUND_WITH_ITEM_NAME.format(
                            slot["raw_value"]
                        )
            else:
                return Response.RECIPE_NOT_FOUND_WITHOUT_ITEM_NAME.value

        elif intent == "AMAZON.HelpIntent":
            return Response.HELP_MESSAGE.value

        elif intent == "AMAZON.StopIntent":
            return "Goodbye!"

        else:
            return Response.ERROR.value
