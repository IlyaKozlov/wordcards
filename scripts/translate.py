#!/usr/bin/python3
import json

import requests
import argparse
import textwrap

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description="Translate a word or phrase.")

# Add arguments to the parser
parser.add_argument("phrase", type=str, help="Words or phrase to translate.")
parser.add_argument(
    "--url",
    type=str,
    default="http://localhost:2218",
    help="URL to the translation service.",
)

args = parser.parse_args()

# Send the POST request to the translation service
response = requests.post(
    f"{args.url}/translate/translate",
    headers={
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    },
    data={"word": args.phrase},
)

# Check if request was successful
max_size = 300
current_size = 0

if response.status_code == 200:
    # Display the response content in streaming format, line wrapped
    for line in response.iter_lines():
        data = json.loads(line)
        text = data["text"]
        current_size += len(text)
        if current_size > max_size:
            print("\r", end="")
            flag = False
            inp = input()
            if inp.lower() == "q":
                exit(0)
            max_size += 66 * 3
        if line:
            print(textwrap.fill(text, width=66))
else:
    print(f"Error: {response.status_code} - {response.text}")
