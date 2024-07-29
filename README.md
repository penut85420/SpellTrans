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
+ `crawl-data.py` 爬取英雄資料。
+ `create-dataset.py` 根據英雄技能建立資料集。
+ `data/datasets.json` 從 Riot API 得到的技能翻譯資料。
+ `data/icon.png` 網頁介面使用的圖示，[來源](https://www.flaticon.com/free-icon/sword_3426325?related_id=3426325)。

## 模型

使用 [vLLM](https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html) 架設與 OpenAI API 相容的 LLM Backend，本範例主要使用 [Llama 3 8B Instruct](https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct) 模型，建議至少要有 16GB 以上的 GPU 記憶體。

參考指令如下：

```bash
python -m vllm.entrypoints.openai.api_server \
    --model meta-llama/Meta-Llama-3-8B-Instruct \
    --api-key auth-token-ouo123
```

根據網路速度不同，此指令需要數十分鐘才能完成下載、轉換與啟動。

## 用法

+ 架設 LLM Backend，請參考上面的指令。
+ (Optional) 執行 `crawl-data.py` 爬取最新版本的英雄資料。
+ (Optional) 如果有爬取新資料，需要執行 `create-dataset.py` 建立翻譯資料集。
+ 執行 `app.py` 啟動網頁介面主程式之後，可在 `http://127.0.0.1:7860/` 使用。

## 授權

MIT License
