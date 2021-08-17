import wave

import numpy as np
import sounddevice as sd
import soundfile as sf
from deepspeech import Model

model_file_path = 'deepspeech-0.9.2-models.pbmm'
lm_file_path = 'deepspeech-0.9.2-models.scorer'
beam_width = 5000
lm_alpha = 0.93
lm_beta = 1.18

model = Model(model_file_path)
model.enableExternalScorer(lm_file_path)
model.setBeamWidth(beam_width)
model.setScorerAlphaBeta(lm_alpha, lm_beta)


def read_wav_file(filename):
    with wave.open(filename, 'rb') as w:
        frames = w.getnframes()
        buffer = w.readframes(frames)

    return buffer


def transcribe(audio_file):
    buffer = read_wav_file(audio_file)
    data16 = np.frombuffer(buffer, dtype=np.int16)
    text = model.stt(data16)
    print(text)
    return text


def get_speech_to_text(seconds):
    audio = sd.rec(int(seconds * 16000), samplerate=16000, channels=1)
    sd.wait()
    sf.write("audio.wav", audio, 16000)
    return transcribe("audio.wav")
