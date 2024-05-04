from Constants import D_WORDS, MONTH_KEYS, LANGUAGES

from text_to_num import alpha2digit


def base_declension(number: int):
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


def declension(number: int, string: str):
    """
    Представление сочетания числительного и слова в нужном формате.

    :param number: ``int``: целочисленный параметр;
    :param string: ``str``: склоняемая строка, обязательно содержащаяся в словаре usages.

    :return: Сочетание числительного и слова в нужном склонении.
    """

    key = base_declension(number)

    return D_WORDS[string][key]


def get_base(text: str):
    """
    Находит исходное слово по склонённому (обратная функция для ``declension``).

    :param text: ``str``: слово, для которого необходимо найти исходное (в именительном падеже).

    :return: Исходное слово или, если оно не найдено, ``None``.
    """

    for base in D_WORDS.keys():
        if any(text == sub for sub in D_WORDS[base].values()):
            return base

    return None


def get_month(key: str):
    """
    Возвращает порядковый номер месяцы по его названию.

    :param key: ``str``: название месяца ("января", "февраля" и т.д).

    :return: Порядковый номер месяца или ``None``, если передан некорректный аргумент.
    """

    for index in range(len(MONTH_KEYS)):
        if MONTH_KEYS[index] == key:
            return index + 1

    return None


def get_language_key(language: str):
    """
    Получает ключ (код) языка по его названию.

    :param language: ``str``: название языка.

    :return: Код языка или ``None``, если он не найден.
    """

    for key in LANGUAGES.keys():
        if language in LANGUAGES[key]:
            return key

    return None


def replace_numbers(text: str, language: str):
    """
    Заменяет все слова, выражающие числа, числовыми занчениями.

    Например, ``"двадцать пять штук" → "25 штук"``.

    :param text: ``str``: исходный текст;
    :param language: ``str``: код языка.

    :return: Изменённая строка.
    """

    text = alpha2digit(text=text, lang=language)
    return text
