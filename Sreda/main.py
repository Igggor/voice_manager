from Sreda.app import VoiceHelper

app = VoiceHelper()

try:
    app.ON()
    app.work()
except KeyboardInterrupt:
    app.EXIT()
