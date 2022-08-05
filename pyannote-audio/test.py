from pyannote.audio import Pipeline
pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization@2022.07")

# apply the pipeline to an audio file
diarization = pipeline("/media/aiden/D83891573891358A/datasets/bravd.wav")

# dump the diarization output to disk using RTTM format
with open("bravd.rttm", "w") as rttm:
    diarization.write_rttm(rttm)

with open("bravd.rttm", "r", encoding="utf-8") as f:
    for line in f.readlines():
        print(line)