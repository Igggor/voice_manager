from VoiceHelper import *

voiceHelper = VoiceHelper()
voiceHelper.ON()

while True:
    voiceHelper.listen_command()
