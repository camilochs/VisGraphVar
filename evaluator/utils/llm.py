
import yaml
import base64
from openai import OpenAI, OpenAIError
from pathlib import Path

current_path = Path(__file__).resolve().parent

def load_client():
  return OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=read_api_key(),
    )

def read_api_key():
    with open(current_path / 'config.yaml') as f:
        config = yaml.safe_load(f)
    return config['api_key_openrouter']

def encode_image(image_path):
    image = None
    with open(image_path, "rb") as image_file:
        image = base64.b64encode(image_file.read()).decode('utf-8')
    return image

def execute_llm(model_name, prompt, image_path):
    client = load_client()
    image = encode_image(image_path)
    output = ""
    try:
        completion = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image}"
                            },
                        },
                    ],
                    
                
                }
            ],
        )
        output = completion.choices[0].message.content.strip()
        return output
    except OpenAIError as e:
        print(f"Error: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False
    