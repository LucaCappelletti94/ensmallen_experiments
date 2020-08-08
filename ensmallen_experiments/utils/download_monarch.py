import re
import os
import tempfile

import bs4
import requests
from tqdm.auto import tqdm
from encodeproject import download
import urllib.request

def get_files_from_url(dir_url):
    """Given the url to a http folder, return the list of urls present in it.

    Arguments
    ---------
    dir_url: str,
        The url of the http folder
    """
    r = requests.get(dir_url)
    soup = bs4.BeautifulSoup(r.text)
    urls = []
    for link in soup.findAll('a'):
        file = link.get('href')
        if file.startswith(".") or not file.endswith(".nt"):
            continue
        url = dir_url + file
        urls.append(url)
    return urls


def download_file(file_pointer, url: str):
    """Read the content of the url and write it to the file pointer
    Since the files are  big, this function use streaming download.
    Arguments
    ---------
    file_pointer: _io.BufferedWriter,
        The file pointer obtained from a open() where the content will be written.
    url: str,
        The url of the file to download.
    """
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        for chunk in r.iter_content(chunk_size=8192):
            file_pointer.write(chunk)


def download_monarch(filename: str,
                     dir_url: str = """https://archive.monarchinitiative.org/202008/rdf/""",
                     predicate_blacklist_re = ("rdf-schema#label"),
                     object_blacklist_re = ("\".+\"")):
    """
    Download monarch into a single edge file.

    Arguments
    ---------
    filename: str,
        The path where the monarch file will be saved.
    dir_url: str,
        The url from where to retreive the files urls
    """
    urls = get_files_from_url(dir_url)
    directory = os.path.dirname(filename)
    split_re = re.compile('(?<=\>) (?=[\<\.\"])')
    pred_black = re.compile(predicate_blacklist_re)
    object_blacklist_re = re.compile(object_blacklist_re)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(filename, "wb") as f:
        f.write(bytes("\t".join(["subject", "edge_label", "object", "relation"]) + "\n", encoding='utf8'))
        for url in tqdm(urls):
            for line in urllib.request.urlopen(url):
                try:
                    (s, p, o, period) = split_re.split(line.decode("utf-8"))
                except:
                    pass
                if not pred_black.match(p) and not object_blacklist_re.match(o):
                    f.write(line)

tmp = os.path.join(tempfile.mkdtemp(), "tempfile")
download_monarch(tmp)
