https://blog.csdn.net/weixin_44070509/article/details/123774888
Miss : 属于说话人A的时长, 但系统没有分到说话人A音频中;
False Alarm : 被系统误分到说话人A音频中, 但实际不属于说话人A的时长;
Overlap : 被系统分为说话人A和说话人B同时说话, 但实际没有同时说话的时长;
Confusion : 被系统分为说话人A的, 但是实际属于说话人B的时长;
Reference Length : 是整条音频的总时长。
DER的计算公式见图 DER.png


结果RTTM格式说明
https://www.github.com/nryant/dscore#rttm