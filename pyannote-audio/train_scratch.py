from pyannote.audio import Model
from pyannote.audio.tasks import Segmentation
from pyannote.audio.utils.signal import binarize
from pyannote.audio.utils.metric import DiscreteDiarizationErrorRate
from pyannote.audio.pipelines.utils import get_devices
from pyannote.database import get_protocol
from pyannote.audio.models.segmentation import PyanNet

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

ami = get_protocol('AMI.SpeakerDiarization.only_words')
seg_task = Segmentation(ami, duration=5.0, max_num_speakers=4)
vad_model = PyanNet(task=seg_task, sincnet={'stride': 10})
trainer = pl.Trainer(gpus=1, max_epochs=50)
trainer.fit(vad_model)
der_scratched = test(model=vad_model, protocol=ami, subset="test")
print(f"Local DER (finetuned) = {der_scratched * 100:.1f}%")
