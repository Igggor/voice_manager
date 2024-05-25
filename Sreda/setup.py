from environment import build_PYTHONPATH

build_PYTHONPATH()

try:
    from Sreda.settings import GlobalContext
    from Sreda.environment import Environment, load_environment

    from Sreda.modules.collecting.processor import (build_all_triggers, ready_all, build_all_words,
                                                    ready_all_words, build_alias)
    from Sreda.modules.translation.processor import Translator

    from Sreda.static.constants import DEFAULT_TRIGGERS, AUXILIARY_WORDS, LANGUAGES, MONTH_KEYS, MONTHS

    import os

except ImportError as error:
    from settings import GlobalContext
    from environment import Environment, load_environment

    from modules.collecting.processor import (build_all_triggers, ready_all, build_all_words,
                                              ready_all_words, build_alias)
    from modules.translation.processor import Translator

    from static.constants import DEFAULT_TRIGGERS, AUXILIARY_WORDS, LANGUAGES, MONTH_KEYS, MONTHS

    import os

    print(f"Warning: something went wrong while importing modules: {error}. "
          f"Are all import paths correct?")


def setup() -> None:
    print("Loading environment...")

    load_environment()
    global_context = GlobalContext()

    print("Environment has loaded successfully.\n")

    keys = input("If any triggers need to be rebuilt, please input their keys here... ")

    print()

    if not ready_all(keys=DEFAULT_TRIGGERS.keys()) or not \
            ready_all_words(words=AUXILIARY_WORDS + MONTH_KEYS + MONTHS + [lang["ru"] for lang in LANGUAGES.values()]) \
            or not ready_all(keys=["__alias__"]) or keys.lower() != "":
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

        build_all_words(
            translator=translator, force_keys=list(),
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


if __name__ == "__main__":
    setup()
