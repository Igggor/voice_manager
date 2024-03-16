from Constants import usages
# Склонение слов с числами.


def base_declension(number: int):
    """
    Базовая функция для склонения слов русского языка.

    :param number: целочисленный параметр, обозначающий числительное, которое необходимо просклонять.

    :return: Возвращает ключ-символ, соответствующий отдельной форме слова.
             "R", если слово при числе number должно стоять в родительном падеже,
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

    :param number: целочисленный параметр;
    :param string: склоняемая строка, обязательно содержащаяся в словаре usages.

    :return: Сочетание числительного и слова в нужном склонении.
    """
    key = base_declension(number)

    return usages[string][key]
