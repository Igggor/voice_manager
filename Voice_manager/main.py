from VoiceHelper import *


voiceHelper = VoiceHelper()
voiceHelper.setON()

while voiceHelper.globalContext.ON:
    voiceHelper.listenCommand()
