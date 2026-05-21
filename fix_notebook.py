import json
with open('colab_worker.ipynb', 'r', encoding='utf-8') as f:
    data = json.load(f)
cells = data.get('cells', [])
for cell in cells:
    if cell.get('cell_type') == 'code':
        source = cell.get('source', [])
        for i, line in enumerate(source):
            if 'DEBUG_MINER' in line and 'true' in line:
                source[i] = line.replace('true', 'false').replace('visibility', 'stealth')
with open('colab_worker.ipynb', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)
