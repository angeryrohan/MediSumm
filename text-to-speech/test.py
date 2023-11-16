from gtts import gTTS
import os

text = "hello nushu I love you."
language = 'en'

tts = gTTS(text=text, lang=language, slow=False)
tts.save("output.mp3")

# Play the generated audio file
os.system("start output.mp3")
