import json
from concurrent.futures import ThreadPoolExecutor

import requests


def main():
    version = get_version()
    champions: dict[str, dict] = get_champions(version)

    champs = list(champions["data"].keys())

    cdn_url = f"http://ddragon.leagueoflegends.com/cdn/{version}/data"
    url_fmt = "{}/{}/champion/{}.json"
    langs = ("en_US", "zh_TW")

    args = [(lang, champ) for champ in champs for lang in langs]

    def get_champ(args):
        i, (lang, champ) = args
        url = url_fmt.format(cdn_url, lang, champ)
        resp = requests.get(url)

        fn = f"data/{lang}/{champ}.json"
        with open(fn, "wt", encoding="UTF-8") as fp:
            fp.write(resp.text)

        print(f"{i} Done")

    with ThreadPoolExecutor(max_workers=12) as executor:
        executor.map(get_champ, enumerate(args))


def get_version(offset=0):
    url = "https://ddragon.leagueoflegends.com/api/versions.json"
    resp = requests.get(url)
    return json.loads(resp.text)[offset]


def get_champions(version):
    url = f"http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json"
    resp = requests.get(url)
    return json.loads(resp.text)


if __name__ == "__main__":
    main()
