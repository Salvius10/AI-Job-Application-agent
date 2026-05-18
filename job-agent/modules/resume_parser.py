from modules.llama_helper import ask_llama

def parse_resume(file_path='my_resume.txt'):
    with open(file_path,'r') as f:
        resume_text=f.read()
    prompt=f"""Extract this resume into a single JSON object.
    RULES:
    - Return ONLY the JSON object, nothing else
    - No markdown, no explanation, no extra text
    - All values must be on one line, no line breaks inside strings
    - Use double quotes for all keys and string values

    Required keys:
    - "name" (string)
    - "email" (string)  
    - "skills" (list of strings)
    - "experience" (list of objects with keys: role, company, years)
    - "education" (string)

    Resume:
    {resume_text}"""

    result=ask_llama(prompt,expect_json=True)
    return result

