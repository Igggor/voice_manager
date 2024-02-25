from funcs import *
#Инициализация переменных
sr = speech_recognition.Recognizer()
sr.pause_threshold = 0.5
r = speech_recognition.Recognizer()
m = speech_recognition.Microphone(device_index=1)
is_work = True
is_play = False


#Слушаем и убираем шум
with m as source:
    r.adjust_for_ambient_noise(source)


#Словарик с командами и основными словами бота, типо небольшая иишка
commands_dict = {
    "alias": ('помощник', "бот", "помощь", "ты", "среда", "голосовой", "троечка", ''),
    "tbr": ("помоги", 'скажи', 'расскажи', 'покажи', 'сколько', 'произнеси', "какой"),
    'commands': {
        "here": ['тут', 'спишь', 'на месте'],
        "thanks": ["спасибо", "благодарю"],
        'off': ['пока', "отключись", "до свидания"],
        'greeting': ['привет', 'приветствую'],
        'date_now': ['текущее время', 'сейчас времени', 'который час'],
        "weather": ["какая погода", "погода", "погоду"],
        "curs": ["евро", "доллар", "курс валют"],
    }
}


#Отключение бота
def off():
    global is_work
    is_work = False
    return "Я был рад помогать тебе, жду возможности помочь ещё"


def here():
    return "Я тут, работаю, тебе помогаю"


#Основнй цикл работы ассистента
speak("Приветствую, я голосовой помощник Боня, я готов помогать тебе")
while(is_work):
    query = listen_command()
    print(f"[Log] Распознано: {query}")
    if query.startswith(commands_dict["alias"]):
    # обращаются к боту
        cmd = query
        query = list(cmd.split())
        #Удаляем обраение к ассистенту
        for x in commands_dict['alias']:
            cmd = cmd.replace(x, "").strip()
        #Удаляем действие
        for x in commands_dict['tbr']:
            cmd = cmd.replace(x, "").strip()
        #Получаем команду
        for k, v in commands_dict['commands'].items():
            if cmd in v:
                if k == "open_link":
                    if (query[-1] == "telegram" or query[-1] == "телеграм"): speak(globals()[k]("telegram"))
                    elif (query[-1] == "вк"): speak(globals()[k]("vk"))
                    if (query[-1] == "ютуб" or query[-1] == "youtube"): speak(globals()[k]("youtube"))
                else:
                    speak(globals()[k]())
                break