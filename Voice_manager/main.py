from funcs import *
#Инициализация переменных
sr = speech_recognition.Recognizer()
sr.pause_threshold = 0.5
r = speech_recognition.Recognizer()
m = speech_recognition.Microphone(device_index=1)
is_work = True


#Основнй цикл работы ассистента
speak("Приветствую, я твой универсальный помощник Среда. Ты можешь узнать о моих возможностях на сайте или просто спросив меня.")
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
                speak(globals()[k]())
                break