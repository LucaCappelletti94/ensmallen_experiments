import compress_json
from encodeproject import download
from tqdm.auto import tqdm
import os

data = compress_json.load("graphs.json")
for url in tqdm(data.values(), desc="Downloading graphs"):
    path = url.split("/")[-1]
    if os.path.exists(path):
        continue
    download(url, path)
