import numpy as np
import wave

def wav_read(filename):
    f = wave.open(filename, 'rb')
    params = f.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]
    print("this wave's framerate is " + str(framerate))
    strData = f.readframes(nframes)  # read audio file, in string format
    waveData = np.frombuffer(strData, dtype=np.int16)  # convert string to int16
    print("this wave's length of wavedata is " + str(len(waveData)))

if __name__ == "__main__":
    targetAudio1 = "/media/aiden/D83891573891358A/datasets/amicorpus_back/amicorpus/EN2001a/audio/EN2001a.Mix-Headset.wav"
    targetAudio1 = "/media/aiden/D83891573891358A/datasets/amicorpus_back/amicorpus/EN2001a/audio/EN2001a.Mix-Headset.wav"
    wav_read(targetAudio1)