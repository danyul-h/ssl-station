import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration
import json

filename = "scraped.json"
with open(filename, "r") as file:
    data = json.load(file)

extrapolating = [] #we're going to extrapolate shifts for these needs, they don't already have shifts and we need to generate them

for i in data:
    if not i["shifts"]:
        extrapolating.append(i)

# for i in extrapolating:
    # print(i)


model_name = "t5-small"
tokenizer = T5Tokenizer.from_pretrained(model_name, legacy=False)
model = T5ForConditionalGeneration.from_pretrained(model_name, device_map="auto")

inputs = [f"Extract a date that this event will occur on in a format that matches, \"Thu Jul 24, 2025\", and is based off the information in the json: {i}" for i in extrapolating]
input_ids = tokenizer(inputs, return_tensors="pt", padding=True, truncation=True).input_ids.to("cuda")
with torch.no_grad():
    output_ids = model.generate(input_ids, max_length=256)

extrapolations = [tokenizer.decode(output) for output in output_ids]

filename = "extrapolations.json"
with open(filename, "w") as file:
    json.dump(extrapolations, file, indent=4)