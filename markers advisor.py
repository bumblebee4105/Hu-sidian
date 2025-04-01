import requests
import json
import re
from time import sleep
import tkinter as tk
from tkinter import filedialog, scrolledtext
from docx import Document

skills = ["Overzicht creëren", "Kritisch oordelen", "Juiste kennis ontwikkelen", "Kwalitatief product maken", "Plannen", "Boodschap delen", "Samenwerken", "Flexibel opstellen", "Pro-actief handelen", "Reflecteren"]
base_url = "https://lef.open-ict.hu.nl/_next/data/-GkJ0agPE1pg0v5JgrPh_/nl.json?vaardigheid="
keys_input = "pageProps.vaardigheden."
skill_list = ""
skill_item = ""

OLLAMA_API_URL = "http://localhost:11434/api/generate"

def fetch_url(url, skill, text, keys=None):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)
        
        print(f"Niveau's voor {skill}:")
        try:
            json_response = response.json()
            
            def get_nested_value(d, path):
                keys = path.split(".")
                for key in keys:
                    if isinstance(d, dict) and key in d:
                        d = d[key]
                    else:
                        return "Key not found"
                return d
            
            def process_nested_data(data):
                if isinstance(data, dict):
                    return "\n".join(f"{k}: {v['title']}" if isinstance(v, dict) and 'title' in v else f"{k}: {v}" for k, v in data.items())
                elif isinstance(data, list):
                    return "\n".join(str(item) for item in data)
                else:
                    return data
            
            if keys:
                extracted_data = {key: process_nested_data(get_nested_value(json_response, key)) for key in keys}
                for key, value in extracted_data.items():
                    for i in range(1, 5):
                        if f"{i}:" in value:
                            value = value.replace(f"{i}:", f"\nNiveau {i}:")
                            judgement = judge_input(value, text)
                    return judgement
            else:
                print(json.dumps(json_response, indent=4))  # Pretty print JSON
        except json.JSONDecodeError:
            print(response.text)  # Print raw response if not JSON
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def sanitize_response(name):
    return re.sub(r'[<>:"/\\|?*]', '', name).strip()

def judge_input(nivea_text, text):
    try:
        prompt = f"Niveau eisen:\n\n{nivea_text}.\n\nDocument: {text}. geef een uitleg in het Nederlands waarom dit document wel of niet aan deze vardigheid nivea's voldoet."
        response = requests.post(OLLAMA_API_URL, json={"model": "gemma3:1b", "prompt": prompt, "stream": False})
        response.raise_for_status()
        return response.json().get("response", "Unnamed Code")
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"
    
def sumarize_judgement(beoordeling):
    try:
        prompt = f"beoordeling:\n\n{beoordeling}. geef een samenvatting in het Nederlands van deze beoordeling. ga iedere vaardigheid langs en hun niveau's en geeft een uitleg waarom hij wel of niet behaald is."
        response = requests.post(OLLAMA_API_URL, json={"model": "gemma3:12b", "prompt": prompt, "stream": False})
        response.raise_for_status()
        return response.json().get("response", "Unnamed Code")
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

def generate(text):
    skill_list = ""
    for i in range(len(skills)):
        append = skills[i].replace(" ", "+")
        keys_new = keys_input + str(skills[i])
        url = base_url + append
        keys = [key.strip() for key in keys_new.split(",") if key.strip()] if keys_new else None
        print(skills[i])
        skill_item = fetch_url(url, skills[i], text, keys)
        print(skill_item)
        print("\n")
        skill_list = skill_list + skill_item + "\n\n"
        print("\n")
        sleep(1)
    summary = sumarize_judgement(skill_list)
    print(summary)

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    text = '\n'.join([para.text for para in doc.paragraphs])
    return text

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Word Documents", "*.docx")])
    if file_path:
        text = extract_text_from_docx(file_path)
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.INSERT, text)
        generate(text)

# Create GUI
root = tk.Tk()
root.title("DOCX Text Extractor")
root.geometry("600x400")

btn_open = tk.Button(root, text="Open DOCX File", command=open_file)
btn_open.pack(pady=10)

text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=20)
text_area.pack(pady=10)

root.mainloop()
