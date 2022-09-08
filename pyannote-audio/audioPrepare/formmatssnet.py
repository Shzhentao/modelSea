import os
from pydub import AudioSegment


def formatMTA(dataset_name, start, nums):
    for index in range(start, start + nums):
        outputdir = "/media/aiden/D83891573891358A/datasets/amicorpus_noise/mtassnet"
        out_mixture_file_names = os.listdir(outputdir)
        outputnoisedir = "/media/aiden/D83891573891358A/datasets/amicorpus_noise/matssnet_noise"
        out_noise_file_names = os.listdir(outputnoisedir)
        outputspeechdir = "/media/aiden/D83891573891358A/datasets/amicorpus_noise/matssnet_speech"
        out_speech_file_names = os.listdir(outputspeechdir)


        sound = AudioSegment.from_wav(os.path.join(outputdir, out_mixture_file_names[index]))
        soundn = AudioSegment.from_wav(os.path.join(outputnoisedir, out_noise_file_names[index]))
        sounds = AudioSegment.from_wav(os.path.join(outputspeechdir, out_speech_file_names[index]))
        # # 语音切割,以毫秒为单位
        start_time = 0
        internal = start_time + 5
        start_time = int(start_time * 1000)
        end_time = int(internal*1000)
        # 语音文件切割
        part = sound[start_time:end_time]
        partn = soundn[start_time:end_time]
        parts = sounds[start_time:end_time]

        out_data_path = "/media/aiden/D83891573891358A/datasets/amicorpus_noise/mtassnetFormat"
        os.makedirs(out_data_path,exist_ok=True)
        out_mixture_data_path = out_data_path + os.sep + dataset_name + os.sep + 'mixture' + os.sep + 'mixture' + str(index) + os.sep
        out_mixture_file_name = 'mixture_' + str(index) + '.wav'
        out_speech_data_path = out_data_path + os.sep + dataset_name + os.sep + 'speech' + os.sep + 'speech' + str(index) + os.sep
        out_speech_file_name = 'speech_' + str(index) + '.wav'
        out_noise_data_path = out_data_path + os.sep + dataset_name + os.sep + 'noise' + os.sep + 'noise' + str(index) + os.sep
        out_noise_file_name = 'noise_' + str(index) + '.wav'
        os.makedirs(out_mixture_data_path,exist_ok=True)
        os.makedirs(out_speech_data_path,exist_ok=True)
        os.makedirs(out_noise_data_path,exist_ok=True)
        data_file_out = os.path.join(out_mixture_data_path, out_mixture_file_name)
        data_file_outn = os.path.join(out_noise_data_path, out_noise_file_name)
        data_file_outs = os.path.join(out_speech_data_path, out_speech_file_name)
        part.export(data_file_out, format="wav")
        partn.export(data_file_outn, format="wav")
        parts.export(data_file_outs, format="wav")

if __name__ == "__main__":
    formatMTA("train", 0, 10000)
    formatMTA("test", 10000, 1000)
    formatMTA("dev",11000,1000)