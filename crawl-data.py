import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from tqdm import trange


def main():
    version = get_version()
    champions: dict[str, dict] = get_champions(version)
    with open("data/champion.json", "wt", encoding="UTF-8") as fp:
        json.dump(champions, fp, ensure_ascii=False, indent=4)

    with ThreadPoolExecutor(max_workers=16) as executor:
        futures = [
            executor.submit(get_champ, champ, lang, version)
            for champ in champions["data"]
            for lang in ("en_US", "zh_TW")
        ]

        with trange(len(futures), ncols=100) as prog:
            [prog.update() for _ in as_completed(futures)]


def get_version(offset=0):
    url = "https://ddragon.leagueoflegends.com/api/versions.json"
    resp = requests.get(url)
    return json.loads(resp.text)[offset]


def get_champions(version):
    url = f"http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json"
    resp = requests.get(url)
    return json.loads(resp.text)


def get_champ(champ, lang, version):
    cdn_url = f"http://ddragon.leagueoflegends.com/cdn/{version}/data"
    url = f"{cdn_url}/{lang}/champion/{champ}.json"
    resp = requests.get(url)

    fn = f"data/{lang}/{champ}.json"
    os.makedirs(f"data/{lang}", exist_ok=True)
    with open(fn, "wt", encoding="UTF-8") as fp:
        fp.write(resp.text)


if __name__ == "__main__":
    main()
