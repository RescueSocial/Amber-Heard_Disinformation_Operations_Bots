import torch
import transformers
import argparse
import json
import os
from transformers import BertForSequenceClassification, BertConfig

if os.name =='nt':
    PRETRAINED_MODEL = os.path.join(os.getcwd(), r"models\pytorch_model_GPU.bin")
else:
    PRETRAINED_MODEL = os.path.join(os.getcwd(), "models/pytorch_model_GPU.bin")

def get_model_and_tokenizer(
    model_type, model_name, tokenizer_name, num_classes, state_dict
):
    model_class = getattr(transformers, model_name)
    model = model_class.from_pretrained(
        pretrained_model_name_or_path=None,
        config=model_type,
        num_labels=num_classes,
        state_dict=state_dict,
    )
    tokenizer = getattr(transformers, tokenizer_name).from_pretrained(model_type)
    return model, tokenizer

def load_checkpoint(model_type="original", checkpoint=None, device='cpu',config='null'):
    loaded = {}
    if device == 'cpu':
        loaded['state_dict'] = torch.load(checkpoint, map_location=torch.device('cpu'))
    else:
        loaded['state_dict'] = torch.load(checkpoint)
    loaded['config'] = config
    class_names = loaded["config"]["dataset"]["args"]["classes"]
    model, tokenizer = get_model_and_tokenizer(
        **loaded["config"]["arch"]["args"], state_dict=loaded["state_dict"]
    )
    return model, tokenizer, class_names

class MultiClassification:
    def __init__(self, model_type="original", checkpoint=PRETRAINED_MODEL, device="cpu", config="null"):
        super(MultiClassification, self).__init__()
        self.model, self.tokenizer, self.class_names = load_checkpoint(
            model_type=model_type, checkpoint=checkpoint, device=device, config=config
        )
        self.device = device
        self.model.to(self.device)

    @torch.no_grad()
    def predict(self, text):
        self.model.eval()
        inputs = self.tokenizer(
            text, return_tensors="pt", truncation=True, padding=True
        ).to(self.model.device)
        out = self.model(**inputs)[0]
        scores = torch.sigmoid(out).cpu().detach().numpy()
        results = {}
        for i, cla in enumerate(self.class_names):
            results[cla] = (
                scores[0][i]
                if isinstance(text, str)
                else [scores[ex_i][i].tolist() for ex_i in range(len(scores))]
            )
        return results
