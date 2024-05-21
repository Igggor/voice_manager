from environment import build_PYTHONPATH

build_PYTHONPATH()

try:
    from Sreda.app import VoiceHelper
except ImportError as error:
    from app import VoiceHelper
    print(f"Warning: something went wrong while importing VoiceHelper: {error}. "
          f"Are all import paths correct?")


app = VoiceHelper()

try:
    app.ON()
    app.work()
except KeyboardInterrupt:
    app.EXIT()
