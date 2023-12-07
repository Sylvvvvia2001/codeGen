import os
import yaml
import json
import requests

def process_yaml_file(file_path):
    """处理YAML文件并返回一段文字"""
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
        phrases = list(data.values())[0]
        if not phrases or len(phrases) == 1:
            return None, phrases
        text = ', '.join(phrases)
        return text, None

def classify_phrases(api_url, api_key, phrases):
    """发送请求到GPT API并获取分类结果"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": api_key
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "Classify the following phrases based on smart home devices: " + phrases
            }
        ],
        "temperature": 0.7
    }
    response = requests.post(api_url, headers=headers, data=json.dumps(data))
    return response.json() if response.status_code == 200 else None

def main():
    api_url = "https://gpt-api.hkust-gz.edu.cn/v1/chat/completions"
    api_key = os.getenv('GPT_API_KEY')
    yaml_folder = 'alternative_mode/base_platforms/class/class_statistic'
    output_folder = 'alternative_mode/base_platforms/class/classification'

    for file_name in os.listdir(yaml_folder):
        file_path = os.path.join(yaml_folder, file_name)
        phrases, single_phrase = process_yaml_file(file_path)

        if phrases is None:
            output_path = os.path.join(output_folder, file_name.replace('.yaml', '.txt'))
            with open(output_path, 'w') as output_file:
                if single_phrase:
                    output_file.write(single_phrase[0])
            continue

        print(f"Sending to GPT: {phrases}")
        response_data = classify_phrases(api_url, api_key, phrases)
        print(f"GPT Response: {response_data}")

        if response_data:
            output_path = os.path.join(output_folder, file_name.replace('.yaml', '.txt'))
            with open(output_path, 'w') as output_file:
                output_file.write(json.dumps(response_data, indent=4))

if __name__ == "__main__":
    main()
