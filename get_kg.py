import json
import openai
import csv
import os


openai.api_key = os.getenv("OPENAI_API_KEY")
prompt_text = """Given a text, extract a knowledge graph from the text by extrapolating as many relationships as possible from the text. Every node has an id, label, and its NER tag in BOI format. Every edge has a to and from with node ids, and a label. Edges are directed, so the order of the from and to is important.

Examples:

Text: Toto is taba's friend

{ "nodes": [ { "id": 1, "label": "Toto", "ner_tag": "B-PERSON" }, { "id": 2, "label": "Tata", "ner_tag": "B-PERSON" } ], "edges": [ { "from": 1, "to": 2, "label": "friend" } ] }

Text : 
"""
error_f = open("./ouput/logs/error.txt", "a")
lesson = "univers.csv"
dir = os.path.splitext(lesson)[0]
num = 0
if not os.path.exists(dir):
    os.makedirs(dir)
with open(lesson, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        if csvreader.line_num <= num :
            continue
        print(row[0], row[1])
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt_text + row[1],
                temperature=0,
                max_tokens=1500,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
        except Exception as e:
            print("TryAgain", e)
            error_f.write(f'{csvreader.line_num}\n')
            continue

        print("OK", row[0])
        try:
            graph = json.loads(
                response["choices"][0]["text"].split("\n\n")[1])
        except Exception as e:
            print(
                e, f'response from document {csvreader.line_num} is not jsonified')
            error_f.write(f'{csvreader.line_num}\n')
            continue
        res = {str(csvreader.line_num): {
            "text": row[1], "graph": graph}}
        print("OK again", row[0])
        with open(os.path.join(dir, str(csvreader.line_num)+".json"), "w") as json_file:
            print(os.path.join(dir, str(csvreader.line_num)+".json"))
            json.dump(res, json_file, indent=4)