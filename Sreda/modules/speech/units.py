class PlayableText:
    """
    Обертка воспроизводимого текста для многофункциональной работы с ним.

    **Структура:**
        Представляет собой список ``blocks``, причём один элемент соответствует одной команде.

        Элементами являются "непрерывные части" текста одной команды. При переходе от одной такой части к другой
        вопроизведение может быть безопасно прервано.

        "Непрерывные части" состоят из словарей вида:
            ``{source: текст, language: язык текста}``.
    """

    def __init__(self):
        self.blocks = list()

    def add(self, text: str, lang: str, new: bool = True) -> None:
        """
        Добавление текста к воспроизводимой фразе.

        :param text: ``str``: добавляемый текст;
        :param lang: ``str``: код языка текста;
        :param new: ``bool`` выделяется ли новый блок под добавляемый текст.

        :return:
        """

        blocks = text.split('\n')

        if new:
            self.blocks.append(list())

        for block in blocks:
            # Empty block
            if not block:
                continue

            self.blocks[len(self.blocks) - 1].append({
                "source": block,
                "language": lang
            })

    def get_normal_text(self) -> str:
        """
        Получение текстового представления экземпляра ``PlayableText`` в читабельном виде,
        но не предназначенном для воспроизведения.

        :return: Воспроизводимый текст.
        """

        output_text = ""
        for query in self.blocks:
            for block in query:
                output_text += (block["source"] + '\n')
            output_text += '\n'

        return output_text

    def get_straight_blocks(self) -> list[dict[str, str]]:
        """
        Метод преобразование из двумерного списка блоков в сплошной одномерный.

        :return: Полученный одномерный список фраз, представляющих собой текст и код языка воспроизведения.
        """

        output_blocks = list()
        for query in self.blocks:
            for block in query:
                output_blocks.append(block)

        return output_blocks
