from VoiceHelper import *


voiceHelper = VoiceHelper()
voiceHelper.set_ON()

while True:
    voiceHelper.listen_command()
