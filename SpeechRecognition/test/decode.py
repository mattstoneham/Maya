
import speechrec as sr
print('test')

r = sr.Recognizer()

def decode(audiofile, method='Google'):
    text = None
    with sr.AudioFile(audiofile) as source:
        # load audio to memory
        audio_data = r.record(source)

        # recognise
        if method=='Google':
            text = r.recognize_google(audio_data)
    return(text)



audiofile = 'D:\\PythonProjects\\SpeechRecognition\\sample_audio\\set_timeline_to_selected.wav'
text = decode(audiofile)

