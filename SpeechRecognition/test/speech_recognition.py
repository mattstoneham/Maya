
import speech_recognition as sr

r = sr.Recognizer()
mic = sr.Microphone(device_index=4) # Snowball mic
with mic as source:
    print('Say something')
    audio = r.listen(source)

    r.energy_threshold = 300
    r.pause_threshold = 1
    print('Finished')

text = r.recognize_google(audio)
print(text)




print('test')
microphones = sr.Microphone.list_microphone_names()
for microphone in microphones:
    print(microphone)


