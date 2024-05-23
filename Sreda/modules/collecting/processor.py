from Sreda.environment import Environment

from Sreda.modules.translation.processor import Translator
from Sreda.modules.parser.processor import canonize_text
from Sreda.modules.collecting.units import Trigger, TriggerJSON, Storage

from Sreda.static.constants import DEFAULT_TRIGGERS, LANGUAGES

import json
import os
from tqdm import tqdm
from time import sleep


def ready_all(keys: list[str]) -> bool:
    """
    Функция проверки готовности всех триггеров для команд с ключами из списка ``keys``.

    :param keys: ``list``: список ключей команд, для которых производится проверка готовности.

    :return: ``True`` или ``False``.
    """

    triggers = load_all_triggers()

    if any(key not in triggers.keys() for key in keys):
        return False
    else:
        return True


def _roll(progress: tqdm, translator: Translator, text: str, _index: int, _total: int) -> list[Trigger]:
    """
    Функция, расширяющая список триггеров команд путём перегонки текста из одного языка в другой,
    обеспечивая работу голосового помощника на других языках.

    :param progress: ``tqdm``: прогресс-бар;
    :param translator: ``Translator``: экземпляр класса переводчика;
    :param text: ``str``: триггер, для которого производится поиск синонимов;
    :param _index: ``int``: индекс триггера;
    :param _total: ``int``: всего триггеров.

    :return: Возвращает список из триггеров, соответствующих переданному тексту.
    """

    result = list()
    for language in LANGUAGES:
        other = translator.translate_text_static(text=text, source_language="ru", destination_language=language,
                                                 high_frequency=True)

        progress.set_description(f"Processing: {_index}/{_total} --- {language}")
        progress.update(1)

        if other is None:
            continue

        result.append(Trigger(text=canonize_text(other), lang=language))

    return result


def _auto_reformat_default(arr) -> list[Trigger]:
    """
    Переформатирует список триггеров ``arr``: каждый элемент преобразовывается в экземпляр класса ``Trigger``.

    :param arr: ``list[str]`` **OR** ``list[dict[str, str]]``: преобразуемые триггеры;

    :return: Возвращает изменённый список.
    """

    triggers = list()

    for index in range(len(arr)):
        if isinstance(arr[index], str):
            triggers.append(Trigger(text=canonize_text(arr[index])))
        else:
            triggers.append(Trigger(text=canonize_text(arr[index]["text"]), lang=arr[index]["lang"]))

    return triggers


def _build_triggers(translator: Translator, key: str) -> list[Trigger]:
    """
    Расширяет существующие триггеры для команды с ключом ``key``.

    :param translator: ``Translator``: экземпляр переводчика;
    :param key: ``str``: ключ команды, для которой производится операция;

    :return: Возвращает изменённый список.
    """

    print(f"Building <{key}> triggers started.")
    sleep(1.5)

    already_built = _auto_reformat_default(arr=DEFAULT_TRIGGERS[key])

    responses = list()
    with tqdm(total=len(DEFAULT_TRIGGERS[key]) * len(LANGUAGES)) as progress:
        for index in range(len(DEFAULT_TRIGGERS[key])):
            trigger = DEFAULT_TRIGGERS[key][index]
            response = _roll(
                progress=progress, translator=translator, text=trigger, _index=index + 1,
                _total=len(DEFAULT_TRIGGERS[key])
            )

            responses += response

    responses.sort(key=lambda x: x.lang)

    def _redundant(current: Trigger) -> bool:
        """
        Проверка на то, что данный триггер является действительным, т.е. не является дублируемым.

        :param current: ``Trigger``: проверяемый триггер.

        :return: ``True`` или ``False``.
        """

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

    sleep(1.5)
    print(f"Building triggers for <{key}> finished successfully.\n")
    sleep(1.5)

    return already_built + duplicates + returning


def load_storage() -> None:
    """
    Загрузка файловых данных.

    :return:
    """

    Storage.TRIGGERS = load_all_triggers(required_keys=DEFAULT_TRIGGERS.keys())
    Storage.WORDS = load_all_words()


def load_all_triggers(required_keys: list[str] = None) -> dict[str, list[Trigger]]:
    """
    Функция загрузки триггеров.

    :param required_keys: ``list``: список, содержащий ключи команд, для которых необходимо построить триггеры.
        Если не передан, то будет возвращёно всё содержимое ``triggers.json``.

    :return: Готовый словарь вида ``{ key: [`` триггеры для команды с ключом ``key ] }``.

    :raise LookupError: в случае, если не найдено построенных триггеров для какой-либо команды.
    """

    path = os.path.join(Environment.__ROOT__, "storage/triggers.json")
    with open(path, "r") as file:
        data_json: dict[str, list[dict[str, str]]] = json.load(file)["main"]

    new_data_json: dict[str, list[Trigger]] = dict()
    for key in data_json.keys():
        new_data_json[key] = _auto_reformat_default(arr=data_json[key])

    if required_keys is None:
        return new_data_json

    for key in required_keys:
        if key not in data_json.keys():
            raise LookupError(f"Cannot find the DEFAULT_TRIGGERS for {key} key. You should add it manually.")

    return new_data_json


def load_all_words() -> dict[str, list[Trigger]]:
    """
    Функция загрузки слов.

    :return: Готовый словарь вида ``{ key: [`` перевод слова ``key`` на поддерживаемые языки ``] }``.
    """

    path = os.path.join(Environment.__ROOT__, "storage/words.json")

    with open(path, "r") as file:
        data_json: dict[str, list[dict[str, str]]] = json.load(file)["main"]

    new_data_json: dict[str, list[Trigger]] = dict()
    for key in data_json.keys():
        new_data_json[key] = _auto_reformat_default(arr=data_json[key])

    return new_data_json


def _build_ones_triggers(translator: Translator, data_json: dict[str, list[Trigger]], key: str, force: bool = False) \
        -> None:
    """
    Комплекс действий от проверки готовности триггера для данной команды ``key`` до, если необходимо,
    их построения из уже существующих триггеров ``DEFAULT_TRIGGERS`` и записи в хранилище.

    :param translator: ``Translator``: экземпляр переводчика;
    :param data_json: загруженные из файла триггеры;
    :param key: ``str``: ключ команды, для которой строятся триггеры;
    :param force: ``bool``: будет ли перезаписан триггер для данной команды. По усполчанию ``False``.

    :return:
    """

    if not force and key in data_json.keys():
        return

    new = _build_triggers(translator=translator, key=key)

    data_json[key] = new


def _dump_data(data_json, path: str = "storage/triggers.json") -> None:
    """
    Загрузка данных в файл.

    :param path: ``str``: путь для записи;
    :param data_json: данные для записи.

    :return:
    """

    new_data_json = {"main": data_json}
    _path = os.path.join(Environment.__ROOT__, path)
    with open(_path, "w") as file:
        json.dump(new_data_json, file, cls=TriggerJSON, ensure_ascii=False, indent=4, sort_keys=True)


def build_all_triggers(translator: Translator, force_keys: list[str], keys: list[str], dynamic: bool = False) -> None:
    """
    Функция построения триггеров из уже существующих ``DEFAULT_TRIGGERS`` для всех команд с ключами из списка ``keys``.

    :param translator: ``Translator``: экземпляр переводчика;
    :param force_keys: ``list``: список, содержащий ключи команд, для которых будут `перестроены`
      триггеры (или построены новые);
    :param keys: ``list``: список, содержащий ключи команд, для которых необходимо построить триггеры.
    :param dynamic: ``bool``: если установлено ``True``, то сохранение в файл будет производиться после построения
    триггеров для `каждой` команды. Т.к. объём данных может быть очень большим, передача значения ``True``
    может вызвать проблемы с скоростью выполнения.

    :return:
    """

    data_json = load_all_triggers()

    for key in force_keys:
        _build_ones_triggers(translator=translator, data_json=data_json, key=key, force=True)

        if dynamic:
            _dump_data(data_json)

    for key in keys:
        _build_ones_triggers(translator=translator, data_json=data_json, key=key)

        if dynamic:
            _dump_data(data_json)

    if not dynamic:
        _dump_data(data_json)


def build_alias(translator: Translator, alias: list[str]) -> None:
    """
    Функция нахождения обращения на многих языках.

    :param translator: ``Translator``: экземпляр переводчика;
    :param alias: ``list``: имена на русском.

    :return:
    """

    data_json = load_all_triggers()

    print(f"Building alias started.")
    sleep(1.5)

    already_built = _auto_reformat_default(arr=alias)

    responses = list()
    with tqdm(total=len(alias) * len(LANGUAGES)) as progress:
        for index in range(len(alias)):
            trigger = alias[index]
            response = _roll(
                progress=progress, translator=translator, text=trigger, _index=index + 1,
                _total=len(alias)
            )

            responses += response

    responses.sort(key=lambda x: x.lang)

    def _redundant(current: Trigger) -> bool:
        """
        Проверка на то, что данный триггер является действительным, т.е. не является дублируемым.

        :param current: ``Trigger``: проверяемый триггер.

        :return: ``True`` или ``False``.
        """

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

    writable = already_built + duplicates + returning

    sleep(1.5)
    print(f"Building alias finished successfully.\n")
    sleep(1.5)

    data_json["__alias__"] = writable
    _dump_data(data_json)


def ready_all_words(words: list[str]) -> bool:
    """
    Функция проверки готовности всех триггеров для команд с ключами из списка ``keys``.

    :param words: ``list``: список слов, для которых производится проверка готовности.

    :return: ``True`` или ``False``.
    """

    loaded = load_all_words()

    if any(value not in loaded.keys() for value in words):
        return False
    else:
        return True


def _build_words(translator: Translator, word: str) -> list[Trigger]:
    """
    Строит перевод для слова ``word``.

    :param translator: ``Translator``: экземпляр переводчика;
    :param word: ``str``: слово, для которого производится операция;

    :return: Возвращает изменённый список.
    """

    print(f"Building <{word}> started.")
    sleep(1.5)

    already_built = _auto_reformat_default(arr=[word])

    responses = list()
    with tqdm(total=len(LANGUAGES)) as progress:
        response = _roll(
            progress=progress, translator=translator, text=word, _index=1,
            _total=1
        )

        responses += response

    responses.sort(key=lambda x: x.lang)

    def _redundant(current: Trigger) -> bool:
        """
        Проверка на то, что данный триггер является действительным, т.е. не является дублируемым.

        :param current: ``Trigger``: проверяемый триггер.

        :return: ``True`` или ``False``.
        """

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

    sleep(1.5)
    print(f"Building for <{word}> finished successfully.\n")
    sleep(1.5)

    return already_built + duplicates + returning


def _build_ones_words(translator: Translator, data_json: dict[str, list[Trigger]], key: str, force: bool = False) \
        -> None:
    """
    Комплекс действий от проверки готовности триггера для данной команды ``key`` до, если необходимо,
    их построения из уже существующих триггеров ``DEFAULT_TRIGGERS`` и записи в хранилище.

    :param translator: ``Translator``: экземпляр переводчика;
    :param data_json: загруженные из файла слова;
    :param key: ``str``: слово.
    :param force: ``bool``: будет ли перезаписано данное слово. По усполчанию ``False``.

    :return:
    """

    if not force and key in data_json.keys():
        return

    new = _build_words(translator=translator, word=key)

    data_json[key] = new


def build_all_words(translator: Translator, force_keys: list[str], keys: list[str], dynamic: bool = False) -> None:
    """
    Функция построения слов на поддерживаемых языках.

    :param translator: ``Translator``: экземпляр переводчика;
    :param force_keys: ``list``: список, содержащий слова, которые будут `перестроены`;
    :param keys: ``list``: слова на русском;
    :param dynamic: ``bool``: если установлено ``True``, то сохранение в файл будет производиться после построения
    триггеров для `каждой` команды. Т.к. объём данных может быть очень большим, передача значения ``True``
    может вызвать проблемы с скоростью выполнения.

    :return:
    """

    data_json = load_all_words()

    for key in force_keys:
        _build_ones_words(translator=translator, data_json=data_json, key=key, force=True)

        if dynamic:
            _dump_data(data_json)

    for key in keys:
        _build_ones_words(translator=translator, data_json=data_json, key=key)

        if dynamic:
            _dump_data(path="storage/words.json", data_json=data_json)

    if not dynamic:
        _dump_data(path="storage/words.json", data_json=data_json)
