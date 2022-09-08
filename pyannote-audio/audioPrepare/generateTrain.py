import os
from pydub import AudioSegment
import re


def cut_to(filename, outputdir, outputnoisedir, outputspeechdir, starttime, duringtime, tdict):
    index = tdict[filename]
    out_mixture_data_path = "/media/aiden/D83891573891358A/datasets/amicorpus_noise/train/" + 'mixture' + os.sep + 'mixture' + str(index) + os.sep
    out_mixture_file_name = 'mixture_' + str(index) + '.wav'
    sound = AudioSegment.from_wav(os.path.join(out_mixture_data_path, out_mixture_file_name))
    out_noise_data_path = "/media/aiden/D83891573891358A/datasets/amicorpus_noise/train/" + 'noise' + os.sep + 'noise' + str(index) + os.sep
    out_noise_file_name = 'noise_' + str(index) + '.wav'
    soundn = AudioSegment.from_wav(os.path.join(out_noise_data_path, out_noise_file_name))
    out_speech_data_path = "/media/aiden/D83891573891358A/datasets/amicorpus_noise/train/" + 'speech' + os.sep + 'speech' + str(index) + os.sep
    out_speech_file_name = 'speech_' + str(index) + '.wav'
    sounds = AudioSegment.from_wav(os.path.join(out_speech_data_path, out_speech_file_name))
    # # 语音切割,以毫秒为单位
    start_time = starttime
    internal = starttime + duringtime
    if duringtime > 5:
        start_time = int(starttime * 1000)
        end_time = int(internal*1000)
        # 语音文件切割
        num = 0
        part = sound[start_time:end_time]
        partn = soundn[start_time:end_time]
        parts = sounds[start_time:end_time]
        while os.path.exists(os.path.join(outputdir, name + '_' + str(num) + '.wav')):
            num += 1
        # out_data_path = "/media/aiden/D83891573891358A/datasets/amicorpus_noise/mtassnet"
        # dataset_name = "train"
        # out_mixture_data_path = out_data_path + os.sep + dataset_name + os.sep + 'mixture' + os.sep + 'mixture' + str(index) + os.sep
        # out_mixture_file_name = 'mixture_' + str(index) + '.wav'
        # out_speech_data_path = out_data_path + os.sep + dataset_name + os.sep + 'speech' + os.sep + 'speech' + str(index) + os.sep
        # out_speech_file_name = 'speech_' + str(index) + '.wav'
        # out_noise_data_path = out_data_path + os.sep + dataset_name + os.sep + 'noise' + os.sep + 'noise' + str(index) + os.sep
        # out_noise_file_name = 'noise_' + str(index) + '.wav'
        data_file_out = os.path.join(outputdir, name + '_' + str(num) + '.wav')
        data_file_outn = os.path.join(outputnoisedir, name + '_' + str(num) + '.wav')
        data_file_outs = os.path.join(outputspeechdir, name + '_' + str(num) + '.wav')
        # 保存切割文件
        part.export(data_file_out, format="wav")
        partn.export(data_file_outn, format="wav")
        parts.export(data_file_outs, format="wav")

rttmdir = "../AMI-diarization-setup/only_words/rttms/train"
rttmfiles = os.listdir(rttmdir)
tdict = {}
for index, rttmfile in enumerate(rttmfiles):
    tdict.update({rttmfile[:-5] + ".Mix-Headset.wav": index})
for rttmfile in rttmfiles:
    # rttmfile = "bravd.rttm"
    rttmroot = os.path.join(rttmdir, rttmfile)
    outputdir = "/media/aiden/D83891573891358A/datasets/amicorpus_noise/mtassnet"
    outputnoisedir = "/media/aiden/D83891573891358A/datasets/amicorpus_noise/matssnet_noise"
    outputspeechdir = "/media/aiden/D83891573891358A/datasets/amicorpus_noise/matssnet_speech"
    os.makedirs(outputdir, exist_ok=True)
    os.makedirs(outputnoisedir, exist_ok=True)
    os.makedirs(outputspeechdir, exist_ok=True)
    with open(rttmroot, "r", encoding="utf-8") as f:
        for line in f.readlines():
            name = line.split()[1] + ".Mix-Headset.wav"
            start_time = float(line.split()[3])
            during_time = float(line.split()[4])
            cut_to(name, outputdir, outputnoisedir, outputspeechdir, start_time, during_time, tdict)