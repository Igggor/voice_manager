from Sreda.settings import Environment

from Sreda.modules.translation.processor import Translator
from Sreda.modules.parser import canonize_text
from Sreda.modules.triggers.units import Trigger, TriggerJSON

from Sreda.static.constants import DEFAULT_TRIGGERS, LANGUAGES

import json


def ready_all(keys: list[str]) -> bool:
    """
    Функция проверки готовности всех триггеров для команд с ключами из списка ``keys``.

    :param keys: ``list``: список ключей команд, для которых производится проверка готовности.

    :return:
    """

    with open("storage/triggers.json", "r") as file:
        data_json = json.load(file)

    if any(key not in data_json["main"].keys() for key in keys):
        return False
    else:
        return True


def _roll(translator: Translator, text: str, _way: set[str]) -> list[Trigger]:
    """
    Функция, расширяющая список триггеров команд путём перегонки текста из одного языка в другой,
    получая таким обращом синонимы уде существующих триггеров, и к тому же обеспечивающая работу голосового помощника
    на других языках.

    :param translator: ``Translator``: экземпляр класса переводчика;
    :param text: ``str``: триггер, для которого производится поиск синонимов;
    :param _way: ``set``: вспопогательный сет, детектирующий нахождение пути перевода для данного языка;

    :return: Возвращает список из триггеров, соответствующих переданному тексту.
    """

    def equal(first: str, second: str) -> bool:
        """
        Проверка на идентичность двух строк.

        :param first: ``str``: 1-ая строка;
        :param second: ``str``: 2-ая строка.

        :return: ``True`` или ``False``.
        """

        return canonize_text(text=first) == canonize_text(text=second)

    result = list()
    current_id = 0

    for language in LANGUAGES:
        current_id += 1

        other = translator.translate_text_static(text=text, source_language="ru", destination_language=language,
                                                 high_frequency=True)
        back = translator.translate_text_static(text=other, source_language=language, destination_language="ru",
                                                high_frequency=True)
        rev_back = translator.translate_text_static(text=back, source_language="ru", destination_language=language,
                                                    high_frequency=True)

        if other is None or back is None or rev_back is None:
            continue

        # Проверка на однозначность перевода. Если перевод не однозначен, он игнорируется.
        if equal(rev_back, other):
            _way.add(language)

            new = canonize_text(text=back)
            result.append(Trigger(text=new, lang=language))

    return result


def _auto_reformat_default(arr: list[str]) -> list[Trigger]:
    """
    Переформатирует список триггеров ``arr``: каждый элемент преобразовывается в экземпляр класса ``Trigger``.

    :param arr: ``list``: преобразуемый список триггеров;

    :return: Возвращает изменённый список.
    """

    triggers = list()

    for index in range(len(arr)):
        triggers.append(Trigger(text=arr[index]))

    return triggers


def _build_triggers(translator: Translator, key: str, _way: set[str]) -> list[Trigger]:
    """
    Расширяет существующие триггеры для команды с ключом ``key``.

    :param translator: ``Translator``: экземпляр переводчика;
    :param key: ``str``: ключ команды, для которой производится операция;
    :param _way: ``set``: вспопогательный сет, детектирующий нахождение пути перевода для данного языка.

    :return: Возвращает изменённый список.
    """

    print(f"Building <{key}> triggers started. Please wait, this process may take some time.")

    already_built = _auto_reformat_default(arr=DEFAULT_TRIGGERS[key])

    responses = list()
    for index in range(len(DEFAULT_TRIGGERS[key])):
        trigger = DEFAULT_TRIGGERS[key][index]
        response = _roll(translator=translator, text=trigger, _way=_way)

        responses += response
        print(f"Building <{key}> triggers: {round((index + 1) / len(DEFAULT_TRIGGERS[key]) * 100)}% "
              f"(time left: ≈ {(len(DEFAULT_TRIGGERS[key]) - index - 1) * 2} minutes).")

    responses.sort(key=lambda x: x.lang)

    def _redundant(current: Trigger) -> bool:
        """
        Проверка на то, что данный триггер является действительным, т.е. не является дублируемым и не встречается в
        списке дефолтных триггеров.

        :param current: ``Trigger``: проверяемый триггер.

        :return: ``True`` или ``False``.
        """

        if current.text in DEFAULT_TRIGGERS[key]:
            return True
        if current in duplicates:
            return True
        return False

    duplicates = list()
    for value in responses:
        if responses.count(value) > 1 and value not in duplicates:
            duplicates.append(value)

    returning = list()
    for trigger in (responses + duplicates):
        if not _redundant(current=trigger):
            returning.append(trigger)

    return already_built + returning


def _build_ones_triggers(translator: Translator, key: str) -> list[dict[str, str]]:
    """
    Комплекс действий от проверки готовности триггера для данной команды ``key`` до, если необходимо,
    их построения из уже существующих триггеров ``DEFAULT_TRIGGERS`` и записи в хранилище.

    :param translator: ``Translator``: экземпляр переводчика;
    :param key: ``str``: ключ команды, для которой строятся триггеры.

    :return: Возвращает списко из фраз, которые являются триггерами для заданной команды с ключом ``key``.
    """

    with open("storage/triggers.json", "r") as file:
        data_json = json.load(file)

    if key in data_json["main"].keys():
        return data_json["main"][key]

    if not Environment.BUILD:
        raise ImportError("Cannot import triggers from triggers.json. "
                          "Building of triggers only possible in BUILD-mode. You should set <BUILD> = True.")

    BUILDING_WAY = set()
    if key not in DEFAULT_TRIGGERS.keys():
        raise LookupError(f"Cannot find the DEFAULT_TRIGGERS for {key} key. You should add it manually.")

    new = _build_triggers(translator=translator, key=key, _way=BUILDING_WAY)
    data_json["main"][key] = new

    if len(new):
        for language in LANGUAGES:
            if language not in BUILDING_WAY:
                print(f"Warning: cannot find the {key} special trigger-way for <{language}>-language. "
                      f"Probability of incorrect app working for this language.")

    with open("storage/triggers.json", "w") as file:
        json.dump(data_json, file, cls=TriggerJSON, indent=4)

    # Сделано для того, чтобы в любом случае возвращалась строка.
    with open("storage/triggers.json", "r") as file:
        data_json = json.load(file)

    print(f"Building triggers for <{key}> finished.")
    return data_json["main"][key]


def build_all_triggers(translator: Translator, keys: list[str]) -> dict[str, list[dict[str, str]]]:
    """
    Функция построения триггеров из уже существующих ``DEFAULT_TRIGGERS`` для всех команд с ключами из списка ``keys``.

    :param translator: ``Translator``: экземпляр переводчика;
    :param keys: ``list``: список, содержащий ключи команд, для которых необходимо построить триггеры.

    :return: Готовый словарь вида ``{ key: [`` триггеры для команды с ключом ``key ] }``
    """

    triggers = dict()

    for key in keys:
        triggers[key] = _build_ones_triggers(translator=translator, key=key)

    return triggers
