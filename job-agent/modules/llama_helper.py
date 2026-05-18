import requests
import json
import re


OLLAMA_URL='http://localhost:11434/api/generate'
MODEL='llama3'

def clean_json_text(text):
        text = text.replace("```json", "").replace("```", "").strip()
        match = re.search(r'\{.*', text, re.DOTALL)
        if match:
            text=match.group(0)
        open_braces = text.count('{')
        close_braces = text.count('}')
        if open_braces > close_braces:
            text += '}' * (open_braces - close_braces)
        return text


def ask_llama(prompt,expect_json=False,retries=3):
    payload={
        'model':MODEL,
        'prompt':prompt,
        'stream':False,
        'options':{
            'temperature':0
        }
    }
    for attempt in range(retries):    
        try:
            response=requests.post(OLLAMA_URL,json=payload)
            text=response.json()['response'].strip()
            if expect_json:
                text = clean_json_text(text)
                return json.loads(text)
            return text
        except json.JSONDecodeError as e:
            print(f"Attempt {attempt+1} failed {e}")
            if attempt==retries-1:
                print("Raw response was")
                print(text)
                raise e

if __name__ == "__main__":
    reply = ask_llama(
        "Return a JSON object with key 'status' and value 'working'. JSON only, no explanation.",
        expect_json=True
    )
    print(reply)
    print(type(reply))