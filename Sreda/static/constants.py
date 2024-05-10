# Вспомогательный словарь, в котором должны содержаться все склоняемые слова.
D_WORDS = {
    "час": {"R": "часов", "I": "час", "K": "часа"},
    "минута": {"R": "минут", "I": "минута", "K": "минуты"},
    "секунда": {"R": "секунд", "I": "секунда", "K": "секунды"},
    "рубль": {"R": "рублей", "I": "рубль", "K": "рубля"},
    "копейка": {"R": "копеек", "I": "копейка", "K": "копейки"},
    "метр": {"R": "метров", "I": "метр", "K": "метра"},
    "паскаль": {"R": "паскалей", "I": "паскаль", "K": "паскаля"},
    "фаренгейт": {"R": "фаренгейт", "I": "фаренгейт", "K": "фаренгейта"}
}

# Названия месяцев в им. падеже.
MONTHS = ["январь", "февраль", "март", "апрель", "май", "июнь",
          "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"]

# Названия месяцев в сочетании с числами.
MONTH_KEYS = ["января", "февраля", "марта", "апреля", "мая", "июня",
              "июля", "августа", "сентября", "октября", "ноября", "декабря"]

# Поддерживаемые языки.
LANGUAGES = {
    "ar": ["арабский"], "bg": ["болгарский"], "bn": ["бенгальский", "бенгал"], "bs": ["боснийский"],
    "cs": ["чешский"], "da": ["датский"], "de": ["немецкий"], "el": ["греческий"], "en": ["английский"],
    "es": ["испанский"], "et": ["эстонский"], "fi": ["финский"], "fr": ["французский"], "hi": ["хинди"],
    "hr": ["хорватский"], "hu": ["венгерский"], "id": ["индонезийский"], "is": ["исландский"],
    "it": ["итальянский"], "ja": ["японский"], "ko": ["корейский"], "la": ["латинский"], "lv": ["латвийский"],
    "ms": ["малайский"], "ne": ["непальский"], "nl": ["голландский", "нидерландский"], "no": ["норвежский"],
    "pl": ["польский"], "pt": ["португальский"], "ro": ["румынский"], "sk": ["словацкий"], "sq": ["албанский"],
    "sr": ["сербский"], "sv": ["шведский"], "th": ["тайский"], "tr": ["турецкий"], "uk": ["украинский"],
    "vi": ["вьетнамский"], "zh-CN": ["китайский"]
}

# Дефолтные триггеры. При создании новой команды добавлять сюда с соответствующим ключом список из вызывающих эту
# команду словосочетаний (в общем, по аналогии).
DEFAULT_TRIGGERS = {
    "notification": list(),
    "on": ["привет", "включись", "включение", "здравствуй", "приветствую", "просыпайся", "включить"],
    "features": ["что ты умеешь", "возможности", "что ты знаешь", "как ты работаешь", "справка"],
    "thanks": ["спасибо", "благодарю", "благодарность"],
    "full-off": ["отключись полностью", "отключить полностью", "полное отключение", "выключись полностью",
                 "пока", "до скорых встреч", "до свидания"],
    "off": ["отключись", "отключение", "выключись", "отключить", "выключить"],
    "time": ["сколько времени", "текущее время", "сколько сейчас времени"],
    "date": ["какой сегодня день", "сегодняшняя дата", "текущая дата"],
    "course": ["курс валют", "текущий курс валют", "курс рубля", "курс валют на данный момент"],
    "weather-now": ["какая сейчас погода", "текущая погода", "погода"],
    "create-scenario": ["создай сценарий", "добавь сценарий", "создание сценария", "добавление сценария",
                        "создать сценарий", "добавить сценарий"],
    "execute-scenario": ["запусти сценарий", "исполни сценарий", "исполнение сценария", "запуск сценария",
                         "исполнить сценарий", "запустить сценарий"],
    "delete-scenario": ["удали сценарий", "удаление сценария", "убери сценарий", "удалить сценарий", "убрать сценарий"],
    "add-notification": ["добавь уведомление", "добавь напоминание", "создай уведомление", "создай напоминание",
                         "создание напоминания", "создание уведомления", "добавление напоминания",
                         "добавление уведомления", "добавить уведомление", "добавить напоминание",
                         "создать уведомление", "создать напоминание"],
    "add-timer": ["добавь таймер", "создай таймер", "добавление таймера", "создание таймера", "добавить таймер",
                  "создать таймер"],
    "delete-notification": ["удали напоминание", "удали уведомление", "удаление напоминания", "удаление уведомления"],
    "nearest-notification": ["ближайшее уведомление", "ближайшее напоминание"],
    "create-stopwatch": ["создай секундомер", "запусти секундомер", "поставь секундомер", "запуск секундомера",
                         "создание секундомера"],
    "stop-stopwatch": ["останови секундомер", "заверши секундомер", "остановка секундомера", "завершение секундомера"],
    "translate": ["переведи текст", "переведи", "сделай перевод", "перевод текста"],
    "get-volume": ["текущий уровень громкости", "текущая громкость"],
    "set-volume": ["измени уровень громкости", "установи уровень громкости", "измени громкость", "установи громкость",
                   "изменение громкости", "изменение уровня громкости"],
    "add-TODO": ["добавь запись", "добавь заметку", "создай запись", "создай заметку", "добаление записи",
                 "добавление заметки", "создание записи", "создание заметки", "добавить запись", "добавить заметку",
                 "создать запись", "создать заметку"],
    "find-TODO": ["заметки", "записи", "заметка", "запись", "найди заметки", "найди записи", "найди заметку",
                  "найди запись", "найти заметки", "найти записи", "найти заметку", "поиск заметки", "поиск записи",
                  "поиск заметок", "поиск записей"]
}
