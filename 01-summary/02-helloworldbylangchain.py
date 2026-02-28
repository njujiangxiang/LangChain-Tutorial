from  langchain_openai import ChatOpenAI


model = ChatOpenAI(
    model_name = "qwen3.5-plus",
    api_key="sk-ea696c7fcc5a44efb003c7876cb02bc1",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",

)

res = model.invoke("您好，您是谁？您有什么技能？")

print(res.content)
