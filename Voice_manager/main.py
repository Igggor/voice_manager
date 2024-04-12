from VoiceHelper import VoiceHelper

voiceHelper = VoiceHelper()
voiceHelper.ON()

while True:
    voiceHelper.listen_command()
