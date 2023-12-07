import os
import yaml
import requests

def read_yaml_files(directory):
    """
    读取指定目录下所有子目录中的 YAML 文件。
    """
    phrases = []
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".yaml"):
                filepath = os.path.join(subdir, file)
                with open(filepath, 'r') as f:
                    data = yaml.safe_load(f)
                    phrases.extend(data)
    return phrases

def classify_phrases(phrases, api_url, api_key):
    """
    调用 GPT API 对词语进行分类。
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": api_key
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "You are a language model designed for smart devices industry. Classify the following phrases: " + ", ".join(phrases)
            }
        ],
        "temperature": 0.7
    }
    response = requests.post(api_url, headers=headers, json=data)
    return response.json()

def write_classified_phrases(classified_phrases, output_directory):
    """
    将分类后的词语写入 YAML 文件。
    """
    for category, phrases in classified_phrases.items():
        with open(os.path.join(output_directory, f"{category}.yaml"), 'w') as f:
            yaml.dump(phrases, f)

# 主程序
def main():
    input_directory = "alternative_mode/base_platforms/class/class_statistic"
    output_directory = "alternative_mode/base_platforms/class/classification"
    api_url = "https://gpt-api.hkust-gz.edu.cn/v1/chat/completions"
    api_key = os.getenv('GPT_API_KEY')

    phrases = read_yaml_files(input_directory)
    classified_phrases = classify_phrases(phrases, api_url, api_key)
    write_classified_phrases(classified_phrases, output_directory)

if __name__ == "__main__":
    main()
