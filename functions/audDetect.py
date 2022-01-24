import speech_recognition as sr
from gtts import gTTS
import librosa
import soundfile as sf
import warnings

# open the file
def aud2txt():
	try:
		warnings.filterwarnings('ignore')
		file = 'functions/processing/aud.wav'
		# obj = gTTS(text='Привет Как дела?', lang='ru', slow=False)
		# obj.save(file)
		# print(librosa.load(file))
		sf.write(file, librosa.load(file)[0], librosa.load(file)[1])
		# mic = sr.Microphone()
		with sr.AudioFile(file) as source:
		# with mic as source:
		    # listen for the data (load audio to memory)
		    # recognize (convert from speech to text)
		    # initialize the recognizer
		    sr.Recognizer().adjust_for_ambient_noise(source)
		    # clean_audio = sr.Recognizer().record(source)
		    # recognized_speech_ibm = sr.Recognizer().recognize_ibm(clean_audio, username="apkikey", password= "your API Key")
		    text = sr.Recognizer().recognize_google(sr.Recognizer().record(source), language='ru-RU')
		    # text = sr.Recognizer().recognize_google(sr.Recognizer().listen(source), language='ru-RU')
		    # print(text)
		    return(text)
	except Exception as e:
		print(str(e))
		# return(str(e))


# print(aud2txt())