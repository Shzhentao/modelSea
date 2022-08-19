from pyannote.audio import Model
from pyannote.audio.tasks import Segmentation
from copy import deepcopy
from pyannote.audio.utils.signal import binarize
from pyannote.audio.utils.metric import DiscreteDiarizationErrorRate
from pyannote.audio.pipelines.utils import get_devices
from pyannote.database import get_protocol
from pyannote.audio import Inference
import pytorch_lightning as pl


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
pretrained = Model.from_pretrained("pyannote/segmentation")
# test_file = next(ami.test())
# spk_probability = Inference(pretrained, step=2.5)(test_file)
# test_file["annotation"].discretize(notebook.crop, resolution=0.010)
seg_task = Segmentation(ami, duration=5.0, max_num_speakers=4)
der_pretrained = test(model=pretrained, protocol=ami, subset="test")
# print(f"Local DER (pretrained) = {der_pretrained * 100:.1f}%")
finetuned = deepcopy(pretrained)
finetuned.task = seg_task
trainer = pl.Trainer(gpus=1, max_epochs=1)
trainer.fit(finetuned)
der_finetuned = test(model=finetuned, protocol=ami, subset="test")
print(f"Local DER (finetuned) = {der_finetuned * 100:.1f}%")
