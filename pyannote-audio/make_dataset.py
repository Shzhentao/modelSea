import os
from pydub import AudioSegment
import re


def cut_to_3s(filename, outputdir, starttime, duringtime):
    '''
    切割语音长度
    :param src_dir: 用户需要切割的某个语音文件夹
    :param des_3s_dir: 切割后文件存储文件夹
    :param seconds_per_split_file: 切割后每个语音长度
    :return:
    '''
    # 获取该文件夹下所有语音数据
    sound = AudioSegment.from_wav("/media/aiden/D83891573891358A/datasets/voxconverse_dev_wav/audio/" + filename)

    # # 语音切割,以毫秒为单位
    start_time = starttime
    internal = starttime + duringtime
    start_time = int(starttime * 1000)
    end_time = int(internal*1000)

    # 语音文件切割
    num = 0
    print(len(sound))
    print(start_time)
    print(end_time)
    part = sound[start_time:end_time]
    while os.path.exists(os.path.join(outputdir, name + '_' + str(num) + '.wav')):
        num += 1
    data_file_out = os.path.join(outputdir, name + '_' + str(num) + '.wav')
    # 保存切割文件
    part.export(data_file_out, format="wav")


rttmfile = "bravd.rttm"
outputdir = "/media/aiden/D83891573891358A/datasets/voxconverse_dev_wav/output/"
with open(rttmfile, "r", encoding="utf-8") as f:
    for line in f.readlines():
        name = line.split()[1] + ".wav"
        start_time = float(line.split()[3])
        during_time = float(line.split()[4])
        cut_to_3s(name, outputdir, start_time, during_time)



