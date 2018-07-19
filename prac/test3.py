import vlc, time
from mutagen.mp3 import MP3
sound = "../sounds/Heartless.mp3"
p = vlc.MediaPlayer(sound)
audio = MP3(sound)
print(audio.info.length)
try:
    p.play()
    time.sleep(audio.info.length + 2)
except:
    print ("stopping!")
    p.stop()

