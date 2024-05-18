from Sreda.settings import GlobalContext, Environment, load_environment

from Sreda.modules.storaging.processor import (build_all_triggers, ready_all, build_all_words,
                                               ready_all_words, build_alias)
from Sreda.modules.translation.processor import Translator

from Sreda.static.constants import DEFAULT_TRIGGERS, AUXILIARY_WORDS, LANGUAGES, MONTH_KEYS, MONTHS

import whisper
import os


def setup() -> None:
    print("Loading environment...")

    load_environment()
    global_context = GlobalContext()

    print("Environment has loaded successfully.\n")

    keys = input("If any triggers need to be rebuilt, please input their keys here... ")
    keys_words = input("If any words need to be rebuilt, please input them here... ")

    print()

    if not ready_all(keys=DEFAULT_TRIGGERS.keys()) or not \
            ready_all_words(words=AUXILIARY_WORDS + MONTH_KEYS + MONTHS + [lang["ru"] for lang in LANGUAGES.values()]) \
            or not ready_all(keys=["__alias__"]) or keys.lower() != "" or keys_words.lower() != "":
        print("Building triggers and words started. Please wait, it may take some time.\n")

        translator = Translator()

        if keys.lower() == "all":
            build_all_triggers(
                translator=translator, force_keys=list(DEFAULT_TRIGGERS.keys()), keys=[],
                dynamic=Environment.DYNAMIC_BUILDING
            )
        else:
            build_all_triggers(
                translator=translator, force_keys=keys.split(), keys=list(DEFAULT_TRIGGERS.keys()),
                dynamic=Environment.DYNAMIC_BUILDING
            )

        if keys_words.lower() == "all":
            build_all_words(
                translator=translator,
                force_keys=AUXILIARY_WORDS + MONTH_KEYS + MONTHS + [lang["ru"] for lang in LANGUAGES.values()], keys=[],
                dynamic=Environment.DYNAMIC_BUILDING
            )
        else:
            build_all_words(
                translator=translator, force_keys=keys_words.split(),
                keys=AUXILIARY_WORDS + MONTH_KEYS + MONTHS + [lang["ru"] for lang in LANGUAGES.values()],
                dynamic=Environment.DYNAMIC_BUILDING
            )

        if not ready_all(keys=["__alias__"]):
            build_alias(translator, alias=global_context.NAME)

        print("Building triggers and words finished successfully.\n")
    else:
        print("Triggers, alias and words are already up-to-date.\n")

    if not ready_all(keys=DEFAULT_TRIGGERS.keys()):
        raise ImportError("Unexpected error while building triggers.")

    print("Loading model...")

    path = os.path.join(Environment.__ROOT__, "model")
    whisper.load_model(name=Environment.MODEL, download_root=path)

    print("Model has loaded successfully.\n")


if __name__ == "__main__":
    setup()
