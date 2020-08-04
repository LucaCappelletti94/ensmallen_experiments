import compress_json
from encodeproject import download
from tqdm.auto import tqdm

data = compress_json.load("graphs.json")
for url in tqdm(data.values(), desc="Downloading graphs"):
    download(url)
