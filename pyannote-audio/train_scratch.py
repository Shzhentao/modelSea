from pyannote.audio import Model
from pyannote.audio.tasks import Segmentation
from pyannote.audio.utils.signal import binarize
from pyannote.audio.utils.metric import DiscreteDiarizationErrorRate
from pyannote.audio.pipelines.utils import get_devices
from pyannote.database import get_protocol
from pyannote.audio.models.segmentation import PyanNet
import pytorch_lightning as pl
from pyannote.audio import Inference

def test(model, protocol, subset="test"):
    (device,) = get_devices(needs=1)
    metric = DiscreteDiarizationErrorRate()
    files = list(getattr(protocol, subset)())
    inference = Inference(model, device=device)
    for file in files:
        reference = file["annotation"]
        hypothesis = binarize(inference(file))
        uem = file["annotated"]
        _ = metric(reference, hypothesis, uem=uem)
    return abs(metric)

# import os
# os.environ["PYANNOTE_DATABASE_CONFIG"] = '/media/aiden/C227C05090D381B7/sztCode/modelSea/pyannote-audio/AMI-diarization-setup/pyannote/database.yml'

# used to automatically find paths to wav files
from pyannote.database import FileFinder
preprocessors = {'audio': FileFinder()}

# initialize 'only_words' experimental protocol
from pyannote.database import get_protocol
only_words = get_protocol('AMI.SpeakerDiarization.only_words', preprocessors=preprocessors)


# ami = get_protocol('AMI.SpeakerDiarization.only_words')
seg_task = Segmentation(only_words, duration=5.0, max_num_speakers=4)
vad_model = PyanNet(task=seg_task, sincnet={'stride': 10})
trainer = pl.Trainer(gpus=1, max_epochs=50)
trainer.fit(vad_model)
der_scratched = test(model=vad_model, protocol=only_words, subset="test")
print(f"Local DER (scratch) = {der_scratched * 100:.1f}%")
