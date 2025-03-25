import json
import os
from datetime import datetime

def read_json_to_list(json_file_path):
    if os.path.getsize(json_file_path) == 0:
        return []
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            return [item for item in json.load(file) if {'author', 'date', 'content', 'color'}.issubset(item)]
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def write_entry_to_json(author, content, color, json_file_path):
    entries = read_json_to_list(json_file_path)
    entries.append({
        'author': author,
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'content': content,
        'color': color
    })
    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(entries, file, indent=4, ensure_ascii=False)

def delete_entry_from_json(entry_id, json_file_path):
    entries = read_json_to_list(json_file_path)
    updated_entrie = []
    print(entry_id)
    for i in range(len(entries)):
        if i != int(entry_id):
            updated_entrie.append(entries[i])
    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(updated_entrie, file, indent=4, ensure_ascii=False)

