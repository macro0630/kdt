import csv

def read_csv_dicts(path, encoding='utf-8'):
    with open(path, 'r', encoding= encoding, newline="") as f :
        reader = csv.DictReader(f)
        return list(reader)


def write_csv_dicts(path, rows, encoding="utf-8"):
    """dict 리스트 → CSV"""
    rows = list(rows)
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with open(path, "w", encoding=encoding, newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


data = [
    {"id": "1", "name": "Alice", "age": "25"},
    {"id": "2", "name": "Bob", "age": "30"},
]


import json

def read_json(path, encoding="utf-8"):
    with open(path, "r", encoding=encoding) as f:
        return json.load(f)

def write_json(path, obj, encoding="utf-8", pretty=True):
    with open(path, "w", encoding=encoding) as f:
        if pretty:
            json.dump(obj, f, ensure_ascii=False, indent=2)
        else:
            json.dump(obj, f, ensure_ascii=False, separators=(",", ":"))

data = {"users": [{"id": 1, "name": "Alice"}]}

import json

def read_jsonl(path, encoding="utf-8"):
    """JSONL → dict 리스트"""
    result = []
    with open(path, "r", encoding=encoding) as f:
        for line in f:
            line = line.strip()
            if line:
                result.append(json.loads(line))
    return result

def write_jsonl(path, records, encoding="utf-8"):
    """dict 리스트 → JSONL"""
    with open(path, "w", encoding=encoding) as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")


logs = [
    {"id": 1, "msg": "start"},
    {"id": 2, "msg": "running"},
]


