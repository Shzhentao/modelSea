import os
import shutil
import numpy as np
import wave
import os

import random



#    * waveData -- The read data
#    * framerate -- The sampling rate
def wav_read(filename):
    f = wave.open(filename, 'rb')
    params = f.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]
    strData = f.readframes(nframes)  # read audio file, in string format
    waveData = np.frombuffer(strData, dtype=np.int16)  # convert string to int16
    # waveData = waveData*1.0/(max(abs(waveData)))#wave normalization
    waveData = waveData/32768 #wave normalization
    f.close()
    return waveData, framerate

def combinaNoise(filenames, length):
    waveDatas = []
    index = random.randint(0,(len(filenames)-1))
    while True:
        filename = filenames[index]
        index += 1
        if index > 19999:
            index = 0
        f = wave.open(filename, 'rb')
        params = f.getparams()
        _, _, framerate, nframes = params[:4]
        strData = f.readframes(nframes)  # read audio file, in string format
        waveData = np.frombuffer(strData, dtype=np.int16)  # convert string to int16
        # waveData = waveData*1.0/(max(abs(waveData)))#wave normalization
        waveData = waveData/32768 #wave normalization
        waveDatas.extend(list(waveData))
        f.close()
        if len(waveDatas) > length:
            return np.array(waveDatas[:length]), framerate

def wav_write(waveData, filepath, filename, fs):
    outData = np.array(waveData, dtype='int16')  
    outData = np.array(waveData*32768,dtype='int16')
    outfile = filepath + os.sep + filename
    outwave = wave.open(outfile, 'wb')  
    outwave.setnchannels(1)
    outwave.setsampwidth(2)
    outwave.setframerate(fs)
    outwave.writeframes(outData.tostring())  # outData:int16.
    outwave.close()

def mix_snr(x1, x2, snr):
    # x1.shape = [-1,1]
    # x2.shape = [-1,1]
    minator = np.sqrt(np.sum(np.abs(x1)**2))
    denominator = np.sqrt((np.sum(np.abs(x2)**2))*(10**(snr/10)))
    alpha = minator/denominator
    # Check the divide 0 and set alpha=0
    if np.isfinite(alpha) == False:
        alpha = 0
        print('Divide zero occurs!')
        print('The mix gian is set to zero!')
    return alpha


def mix_and_create_dataset(args,path,file_num):
    dataset_name = args
    out_data_path = path
    ori_speech_path = out_data_path + os.sep + "amicorpus" + "_ori"
    ori_noise_path = out_data_path + os.sep + "wham_noise" + os.sep + 'tr'
    speech_wav_file_list = []
    speech_wav_file_list_new = []
    noise_wav_file_list = []
    noises = os.listdir(ori_noise_path)
    for i in range(file_num):
        noise_wav_file_list.append(os.path.join(ori_noise_path, noises[i]))
    for path,_,file_list in os.walk(ori_speech_path):  
        for file_name in file_list:
            speech_wav_file_list.append(os.path.join(path, file_name))
            speech_wav_file_list_new.append(os.path.join("amicorpus".join(path.split("amicorpus_ori")), file_name))
    num = 0
    for file_index in range(len(speech_wav_file_list)):
        print('file index is:',file_index)
        rand_speech_ind = file_index 
        speech_wav_file = speech_wav_file_list[rand_speech_ind]
        speech, speech_fs = wav_read(speech_wav_file)
        noise, noise_fs = combinaNoise(noise_wav_file_list, len(speech))

        file_index = num
        if speech.size == noise.size:
            noise_snr = random.uniform(-5,5)
            speech = np.reshape(speech,(-1,1))
            noise = np.reshape(noise,(-1,1))
            noise_alpha = mix_snr(speech,noise,noise_snr)
            noisy = speech + noise_alpha*noise
            mixture = noisy
            out_mixture_data_path = out_data_path + os.sep + dataset_name + os.sep + 'mixture' + os.sep + 'mixture' + str(file_index) + os.sep
            out_mixture_file_name = 'mixture_' + str(file_index) + '.wav'
            out_speech_data_path = out_data_path + os.sep + dataset_name + os.sep + 'speech' + os.sep + 'speech' + str(file_index) + os.sep
            out_speech_file_name = 'speech_' + str(file_index) + '.wav'
            out_noise_data_path = out_data_path + os.sep + dataset_name + os.sep + 'noise' + os.sep + 'noise' + str(file_index) + os.sep
            out_noise_file_name = 'noise_' + str(file_index) + '.wav'
            out_mixture2_file_name = os.path.basename(speech_wav_file_list_new[file_index])
            if not os.path.exists(os.path.dirname(out_mixture_data_path)):
                os.makedirs(os.path.dirname(out_mixture_data_path))
            if not os.path.exists(os.path.dirname(out_speech_data_path)):
                os.makedirs(os.path.dirname(out_speech_data_path))
            if not os.path.exists(os.path.dirname(out_noise_data_path)):
                os.makedirs(os.path.dirname(out_noise_data_path))
            if not os.path.exists(os.path.dirname(speech_wav_file_list_new[file_index])):
                os.makedirs(os.path.dirname(speech_wav_file_list_new[file_index]))
            wav_write(speech, out_speech_data_path, out_speech_file_name, speech_fs)
            wav_write(noise_alpha*noise, out_noise_data_path, out_noise_file_name, noise_fs)
            wav_write(mixture, out_mixture_data_path, out_mixture_file_name, speech_fs)
            wav_write(mixture, os.path.dirname(speech_wav_file_list_new[file_index]), out_mixture2_file_name, speech_fs)
            num += 1

if __name__ == "__main__":
    ## combine

    args = 'train'
    data_path = '/media/aiden/D83891573891358A/datasets/amicorpus_noise'
    num_file = 20000
    mix_and_create_dataset(args, data_path, num_file)

    ## resample
    # data = "/media/aiden/D83891573891358A/datasets/amicorpus_back/wham_noise/tr"
    # datas = os.listdir(data)
    # for i in range(20000):
    #     speech = os.path.join(data, datas[i])
    #     speech2 = os.path.join(data, datas[i][:-4] + "_" + ".wav")
    #     a = f"ffmpeg -i {speech} -ar 16000 {speech2}"
    #     # shutil.move(speech2, speech)
    #     os.system(a)
    #     os.remove(speech)
    #     shutil.move(speech2, speech)