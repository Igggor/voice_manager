from Sreda.modules.storaging.units import Storage

from Sreda.static.constants import D_WORDS, MONTH_KEYS, LANGUAGES, MONTHS

from text_to_num import alpha2digit


def base_declension(number: int) -> str:
    """
    Базовая функция для склонения слов русского языка.

    :param number: ``int``: целочисленный параметр, обозначающий числительное, которое необходимо просклонять.

    :return: Возвращает ``ключ-символ``, соответствующий отдельной форме слова.
             "R", если слово при числе ``number`` должно стоять в родительном падеже,
             "I" - в именительном, "K" - в остальных случаях.
    """

    number = abs(number)
    if (10 < number < 20) or (number % 10 >= 5 or number % 10 == 0):
        return "R"
    elif number % 10 == 1:
        return "I"
    else:
        return "K"


def declension(number: int, string: str) -> str:
    """
    Представление сочетания числительного и слова в нужном формате.

    :param number: ``int``: целочисленный параметр;
    :param string: ``str``: склоняемая строка, обязательно содержащаяся в словаре usages.

    :return: Сочетание числительного и слова в нужном склонении.
    """

    key = base_declension(number)

    return D_WORDS[string][key]


def get_month(key: str, lang: str, i: bool = False) -> int | None:
    """
    Возвращает порядковый номер месяцы по его названию.

    :param key: ``str``: название месяца ("января", "февраля" и т.д);
    :param lang: ``str``: язык;
    :param i: ``bool``: если ``True``, то поиск осуществляется в списке месяцев в именительном падеже.

    :return: Порядковый номер месяца или ``None``, если передан некорректный аргумент.
    """

    if lang != "ru":
        key = get_word(text=key, lang=lang)

    if key is None:
        return None

    if i:
        for index in range(len(MONTHS)):
            if MONTHS[index] == key:
                return index + 1

        return None
    else:
        for index in range(len(MONTH_KEYS)):
            if MONTH_KEYS[index] == key:
                return index + 1

        return None


def get_language_key(language: str, lang: str) -> str | None:
    """
    Получает ключ (код) языка по его названию.

    :param language: ``str``: название языка;
    :param lang: ``str``: язык, на котором передано название.

    :return: Код языка или ``None``, если он не найден.
    """

    if lang != "ru":
        language = get_word(text=language, lang=lang)

    if language is None:
        return None

    for key in LANGUAGES.keys():
        if language == LANGUAGES[key]["ru"]:
            return key

    return None


def get_word(text: str, lang: str) -> str:
    """
    Находит вариант переданного слова на русском языке.

    :param text: ``str``: исходное слово;
    :param lang: ``str``: язык, на котором должно быть возвращено слово.

    :return: Найденный вариант слова на иностранном языке.
    """

    if text not in Storage.WORDS.keys():
        raise LookupError(f"Cannot find <{text}> word in AUXILIARY_WORDS. Add this word to constants.AUXILIARY_WORDS "
                          f"and run 'setup.py'.")

    for index in range(len(Storage.WORDS[text])):
        if Storage.WORDS[text][index].lang == lang:
            return Storage.WORDS[text][index].text


def get_language_fullname_by_code(key: str, lang: str = "ru") -> str | None:
    """
    Получает полное название языка по его коду.

    :param key: ``str``: название языка;
    :param lang: ``str``: язык ответа: ``en`` или ``ru``.

    :return: Полное название языка или ``None``, если языка с заданным кодом не найдено.
    """

    if key not in LANGUAGES.keys():
        return None

    return LANGUAGES[key][lang]


def replace_numbers(text: str, language: str) -> str:
    """
    Заменяет все слова, выражающие числа, числовыми занчениями.

    Например, ``"двадцать пять штук" → "25 штук"``.

    :param text: ``str``: исходный текст;
    :param language: ``str``: код языка.

    :return: Изменённая строка.
    """

    text = alpha2digit(text=text, lang=language, relaxed=True)
    return text
