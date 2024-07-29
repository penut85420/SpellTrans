import json


def main():
    datasets = list()
    data: dict[str, dict] = load_json("data/champion.json")

    for champ in data["data"].keys():
        # 讀取英雄資料
        en_data = load_json(f"data/en_US/{champ}.json")
        zh_data = load_json(f"data/zh_TW/{champ}.json")

        # 外觀造型名稱
        en_skins = en_data["data"][champ]["skins"]
        zh_skins = zh_data["data"][champ]["skins"]

        # 跳過經典造型
        for en_sk, zh_sk in zip(en_skins[1:], zh_skins[1:]):
            en_sk_name = en_sk["name"]
            zh_sk_name = zh_sk["name"]
            datasets.append(create_item(en_sk_name, zh_sk_name))

        # 主動技能名稱
        en_spells = en_data["data"][champ]["spells"]
        zh_spells = zh_data["data"][champ]["spells"]
        for en_sp, zh_sp in zip(en_spells, zh_spells):
            en_name, zh_name = en_sp["name"], zh_sp["name"]
            datasets.append(create_item(en_name, zh_name))

        # 被動技能名稱
        en_pass = en_data["data"][champ]["passive"]["name"]
        zh_pass = zh_data["data"][champ]["passive"]["name"]
        datasets.append(create_item(en_pass, zh_pass))

    with open("data/datasets.json", "wt", encoding="UTF-8") as fp:
        json.dump(datasets, fp, ensure_ascii=False, indent=4)


def load_json(file_path):
    with open(file_path, "rt", encoding="UTF-8") as fp:
        return json.load(fp)


def create_item(source, target):
    return {"source": source, "target": target}


if __name__ == "__main__":
    main()
