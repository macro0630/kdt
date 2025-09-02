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
