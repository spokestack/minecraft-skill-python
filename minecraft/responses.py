import random
from enum import Enum

from minecraft.recipes import DB


class Response(Enum):
    RANDOM = random.choice(list(DB.keys()))
    WELCOME = (
        "Welcome to Minecraft Helper. You can ask a question like, What's the "
        f"recipe for a {RANDOM}. What can I help you with?"
    )
    ERROR = "Sorry, I can't understand the command. Please say it again."
    HELP_MESSAGE = (
        f"You can ask questions such as, what's the recipe for a {RANDOM}, or, "
        "you can say exit. Now, what can I help you with?"
    )
    RECIPE_NOT_FOUND_WITH_ITEM_NAME = (
        "I'm sorry, I currently do not know the recipe for {}."
    )
    RECIPE_NOT_FOUND_WITHOUT_ITEM_NAME = (
        "I'm sorry, I currently do not know that recipe."
    )
