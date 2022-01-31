from multiclassification import MultiClassification

import argparse
import json
import os


# from textblob import TextBlob

from datetime import datetime


parser = argparse.ArgumentParser()
parser.add_argument(
    "-c",
    "--config",
    default="configs/classification_BERT_For_Amber.json",
    type=str,
    help="config file path (default: None)",
)
parser.add_argument(
    "-d",
    "--device",
    default=None,
    type=str,
    help="indices of GPUs to enable (default: all)",
)
args = parser.parse_args()
config = json.load(open(args.config))

if args.device is not None:
    config["device"] = args.device
    os.environ["CUDA_VISIBLE_DEVICES"] = args.device


# start_time = datetime.now()

classification = MultiClassification('original', config=config)
start_time = datetime.now()

results = classification.predict(["She is a hero to domestic violence victims. She's strong, beautiful and smart. I am with her! I would love to see Amber Heard reprise her role as Mera in the upcoming sequel.",
"When asked by the ACLU executive director Romero, Ms Heard claims $500,000 in space nickels are part of her $3.5 million pledge."])

end_time = datetime.now()
print(end_time - start_time)

print(results)

