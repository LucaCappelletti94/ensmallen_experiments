import compress_json
from encodeproject import download
from tqdm.auto import tqdm
import gzip
import shutil
import zipfile
import os

graphs = compress_json.load("graphs.json")
for data in tqdm(graphs.values(), desc="Downloading graphs"):
    if os.path.exists(data["extraction_path"]):
        continue
    path = data["url"].split("/")[-1]
    download(data["url"], path)
    
    if path.endswith(".gz"):
        with gzip.open(path, 'rb') as f_in:
            with open(data["extraction_path"], 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
    elif path.endswith(".zip"):
        with zipfile.ZipFile(path, 'r') as zip_ref:
            zip_ref.extractall(data["extraction_path"])