from reg import sensitive, insensitive, rdc_emotes, general_emotes
from utils import sentiments, examples
import pandas as pd
import csv
import re
from openai import OpenAI
import tiktoken
import time
import json
import os


from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(
    os.path.dirname(os.path.dirname(__file__)), '..', '.env'))

token = os.getenv("OPENAI_KEY")

client = OpenAI(
    api_key=token
)


def send_batch(batch, sentiment_legend, example_block, example_response):

    prompt_messages = "\n".join(
        [f"{i+1}. \"{msg}\"" for i, msg in enumerate(batch)]
    )

    prompt = (
        "You are a classification algorithm.  \n"
        "Classify each of the following Twitch chat messages into one of the categories below:\n"
        f"{sentiment_legend}\n\n"
        "Respond with a JSON object of the form:\n"
        "{\n"
        f'  "labels": [i0, i1, i2, …, i{len(batch)}]\n'
        "}\n"
        f"Make sure the array “labels” has exactly {len(batch)} integers, one for each message.\n\n"
        f"Here is an example. Given:\n{example_block}\n"
        f"Your response should be:\n{example_response}\n\n"
        f"Classify these messages according to the rules I provided:\n{prompt_messages}"
    )

    functions = [{
        "name": "classify_messages",
        "parameters": {
            "type": "object",
            "properties": {
                "labels": {
                    "type": "array",
                    "items": {"type": "integer", "minimum": 0, "maximum": 9},
                    "minItems": len(batch),
                    "maxItems": len(batch)
                }
            },
            "required": ["labels"]
        }
    }]

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",  # or any supported model
            messages=[
                {"role": "system",
                    "content": "You are a sentiment classification assistant."},
                {"role": "user", "content": prompt}
            ],
            functions=functions,
            function_call={"name": "classify_messages"},
            temperature=0,
        )
        data = response.choices[0].message.function_call.arguments
        labels = json.loads(data)["labels"]
        return labels
    except Exception as e:
        print("API error:", e)
        return []


def main():
    batch = []
    row_batch = []
    max_batch_len = 100
    input_file = "../data/data.csv"
    output_file = "../data/sentiment.csv"

    fsensitive = sensitive + rdc_emotes + general_emotes

    print(f"Sentiment data will be stored in {output_file}")

    sentiment_legend = "\n".join([
        f"{label} = {sidx}" for _, (label, sidx) in enumerate(sentiments)
    ])

    example_block = ""
    for (message, _) in examples:
        example_block += f'"{message}", '
    example_block = example_block[:-2]

    example_response = {"name": "classify_messages",
                        "arguments": {
                            "labels": [
                                sidx for _, sidx in examples
                            ]
                        }}

    with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
            open(output_file, 'w', newline='', encoding='utf-8') as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        writer.writerow(
            ['username', 'message', 'channel', 'date', 'sentiment'])

        for row in reader:
            if len(row) != 4:
                continue  # skip malformed rows
            written = False

            username, message, channel, date = row
            for regex, sidx in fsensitive:
                if re.search(regex, message):
                    writer.writerow([username, message, channel, date, sidx])
                    written = True
                    break
            for ind, sidx in insensitive:
                if isinstance(ind, re.Pattern) and re.search(ind, message.lower()):
                    writer.writerow([username, message, channel, date, sidx])
                    written = True
                    break
                elif not isinstance(ind, re.Pattern) and ind in message:
                    writer.writerow([username, message, channel, date, sidx])
                    written = True
                    break
            if not written:
                batch.append(message)
                row_batch.append([username, message, channel, date])
                if max_batch_len == len(batch):
                    print(f"Sending batch of {len(batch)} messages...")

                    labels = send_batch(
                        batch, sentiment_legend, example_block, example_response)
                    for row_data, label in zip(row_batch, labels):
                        writer.writerow(row_data + [label])

                    batch = []
                    row_batch = []
                    time.sleep(1.5)
        if batch:
            print(f"Sending final batch of {len(batch)} messages...")
            labels = send_batch(batch)
            for row_data, label in zip(row_batch, labels):
                writer.writerow(row_data + [label])


if __name__ == "__main__":
    main()
