import json

import gradio as gr
from langchain.chains import LLMChain
from langchain.embeddings import TensorflowHubEmbeddings
from langchain.llms import HuggingFaceTextGenInference
from langchain.prompts import PromptTemplate
from langchain.prompts.example_selector import (
    SemanticSimilarityExampleSelector as Selector,
)
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.vectorstores import FAISS

# 初始化 LLM
tgi_url = "http://localhost:8080/"
llm = HuggingFaceTextGenInference(
    inference_server_url=tgi_url,
    max_new_tokens=128,
    do_sample=True,
    temperature=1.0,
    truncate=1000,
    stop_sequences=["\n"],
)

# 初始化 Embedding
hub_url = "https://tfhub.dev/google/universal-sentence-encoder-multilingual-large/3"
embeddings = TensorflowHubEmbeddings(model_url=hub_url)


# 讀取資料集
with open("data/datasets.json", "rt", encoding="UTF-8") as fp:
    datasets: dict[str, str] = json.load(fp)

# 初始化範例選擇器
example_selector = Selector.from_examples(
    examples=datasets,
    embeddings=embeddings,
    vectorstore_cls=FAISS,
    k=10,
)

# 建立 Example Template
example_prompt = PromptTemplate(
    input_variables=["source", "target"],
    template="Source: {source}\nTarget: {target}",
)

# 建立 Few-Shot Template
prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_prompt,
    suffix="Source: {query}\nTarget: ",
    prefix="請根據以下範例，產生一個中二的技能翻譯。",
    input_variables=["query"],
)

# Chain!
chain = LLMChain(llm=llm, prompt=prompt, verbose=True)

# 建立 Gradio 網頁介面
title = "中二技能翻譯器"
font = gr.themes.GoogleFont("Noto Sans")
theme = gr.themes.Soft(font=font)

with gr.Blocks(theme=theme, title=title) as app:
    gr.Markdown(f"# {title}")
    gr.Markdown("真不愧是闇影大人！")
    source = gr.Textbox(
        label="Source",
        show_copy_button=True,
        placeholder="e.g. Starburst Stream",
    )

    target = gr.Textbox(
        label="Target",
        show_copy_button=True,
        placeholder="輸入完後按 Enter 送出",
    )

    def send(source):
        result = chain.invoke({"query": source})
        return result["text"]

    source.submit(send, source, target, show_progress="minimal")

app.launch(favicon_path="data/icon.png", share=True)
