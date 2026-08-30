import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def llm_call(prompt, model, temperature=1, thinking=False):
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=os.environ.get("NVIDIA_API_KEY"),
        timeout=30.0
    )

    completion = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        top_p=0.95,
        max_tokens=16384,
        seed=42,
        extra_body={"chat_template_kwargs": {"thinking": thinking}},
        stream=False
    )

    return completion.choices[0].message.content