import json


class Trigger:
    def __init__(self, text: str, lang: str = "ru"):
        self.text = text
        self.lang = lang

    def __eq__(self, other):
        return self.text == other.text and self.lang == other.lang

    def compatible_langs(self, lang: str) -> bool:
        """
        Проверка на совместимость языка триггера и переданного языка.

        :param lang: ``str``: код провреяемого языка;

        :return: ``True`` или ``False``.
        """

        if self.lang is None:
            return True

        if self.lang == lang:
            return True

        return False

    def check_corresponding(self, text: str, language: str) -> bool:
        """
        Проверка на то, что данный триггер встречается в переданном тексте и при этом совместим с данным языком.

        :param text: ``str``: текст;
        :param language: ``str``: код языка.

        :return: ``True`` или ``False``.
        """

        # Different languages
        if not self.compatible_langs(lang=language):
            return False

        if text.startswith(self.text):
            return True

        return False


class TriggerJSON(json.JSONEncoder):
    def default(self, obj):
        return obj.__dict__


class Storage:
    TRIGGERS = None
    WORDS = None
