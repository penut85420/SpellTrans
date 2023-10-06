# 中二技能翻譯

這是一個 LangChain 練習專案，透過 LLM 結合 Riot API 取得的英雄技能翻譯，以 Few-Shot Prompt 的方式獲得中二的技能翻譯。

![Demo](https://i.imgur.com/8kaGnPq.png)

## 環境

+ Ubuntu 22.04
+ Python 3.11

```bash
pip install -r requirements.txt
```

## 檔案

+ `app.py` 啟動網頁介面的主程式。
+ `crawl_data.py` 爬取英雄資料。
+ `create_dataset.py` 根據英雄技能建立資料集。
+ `data/datasets.json` 從 Riot API 得到的技能翻譯資料。
+ `data/icon.png` 網頁介面使用的圖示，[來源](https://www.flaticon.com/free-icon/sword_3426325?related_id=3426325)。

## 模型

使用 [Hugging Face Text Generation Inference](https://github.com/huggingface/text-generation-inference) Docker Image 架設 LLM Backend，可以使用 [Taiwan Llama](https://github.com/MiuLab/Taiwan-LLaMa) 或 [CKIP Llama](https://github.com/ckiplab/CKIP-Llama-2-7b)，建議至少要有 8GB 以上的 GPU 記憶體。

參考指令如下：

```bash
docker run --gpus all --shm-size 1g -p 8080:80 \
    ghcr.io/huggingface/text-generation-inference \
    --model-id ckiplab/CKIP-Llama-2-7b-chat \
    --quantize bitsandbytes-nf4
```

根據網路速度不同，此指令需要數十分鐘才能完成下載、轉換與啟動。

## 用法

+ 架設 LLM Backend，請參考上面的指令。
+ (Optional) 執行 `crawl_data.py` 爬取最新版本的英雄資料。
+ (Optional) 如果有爬取新資料，需要執行 `create_dataset.py` 建立翻譯資料集。
+ 執行 `app.py` 啟動網頁介面主程式之後，可在 `http://127.0.0.1:7860/` 使用。

## 授權

MIT License
