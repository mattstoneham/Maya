import speech_recognition as sr

r = sr.Recognizer()
mic_name = 'Microphone (Blue Snowball )'
#mic_name = 'Microphone Array (IntelÂ® Smart'

def get_string_from_audio(device_index, debug = False):
    mic = sr.Microphone(device_index=device_index) # Snowball mic
    with mic as source:
        r.energy_threshold = 300
        r.pause_threshold = 0.666
        if debug:
            print('Recording')
        audio = r.listen(source)
    if debug:
        print('Finished recording, sending to Google')
    text = r.recognize_google(audio)
    if debug:
        print('Google responded:')
    print(text)


def test():
    print('test')
    get_string_from_audio(device_index=get_microphone_index_by_name(mic_name), debug=True)

def get_microphones():
    return sr.Microphone.list_microphone_names()

def get_microphone_index_by_name(string_match):
    microphones = get_microphones()
    return microphones.index(string_match)

if __name__ == '__main__':
    get_string_from_audio(device_index=get_microphone_index_by_name(mic_name))



''' test 

for m in sr.Microphone.list_microphone_names():
    print(m)

'''


