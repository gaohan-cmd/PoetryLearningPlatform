from prompt_utils import *
import openai
import time
# import config

# os.environ['OPENAI_API_KEY'] =  config.OPENAI_API_KEY
os.environ['OPENAI_API_KEY'] = "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"
openai.api_key = os.getenv("OPENAI_API_KEY")
print(openai.Model.list())
messages = get_prompt()
messages.append({"role": "user", "content": "白日依山尽，黄河入海流。"})

while True:
    try:
        response = openai.ChatCompletion.create(
            # model="gpt-3.5-turbo-0301",
            model="gpt-3.5-turbo-instruct-0914",
            messages=messages,
            temperature=0.8,  # 0.0 - 2.0
            max_tokens=2048,
        )
        break
    except:
        time.sleep(20)

print(response.choices[0].message["content"])
