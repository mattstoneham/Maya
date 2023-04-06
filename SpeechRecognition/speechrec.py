import speech_recognition as sr


r = sr.Recognizer()

def get_string_from_audio():
    mic = sr.Microphone(device_index=4) # Snowball mic
    with mic as source:
        r.energy_threshold = 300
        r.pause_threshold = 0.666

        audio = r.listen(source)

    text = r.recognize_google(audio)
    print(text)



if __name__ == '__main__':
    get_string_from_audio()





