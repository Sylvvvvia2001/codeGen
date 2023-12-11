import os
import yaml
import requests
import json

def classify_phrases(phrases):
    # 分割短语列表以适应token限制
    max_phrases_per_request = 130  # 根据token限制调整这个值
    chunks = [phrases[i:i + max_phrases_per_request] for i in range(0, len(phrases), max_phrases_per_request)]
    results = []

    for chunk in chunks:
        # 构造搜索查询
        search_query = ', '.join(chunk)

        # API URL 和 Headers
        url = "https://gpt-api.hkust-gz.edu.cn/v1/chat/completions"
        api_key = os.getenv('GPT_API_KEY')
        headers = {
            "Content-Type": "application/json",
            "Authorization": api_key
        }

        # 构造请求数据
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": f"你是一个短语分类器。我会给你很多代码中的类名，你可以将他们视为普通的英文短语，这些短语将会在代码语境中使用。基于开发者对智能家居设备进行连接和控制操作的语境，请对这些类名进行语义上的分类。注意：要严格遵守输出要求，首先给出每类的大概内容，然后在下一行给出该类的所有短语，短语之间用逗号隔开。输出全部使用英文，不要出现多余的字符或字段！这意味着所有短语应该是全字母的，请忽略掉短语前后的非字母字符。\n给出一个输出的范例: \nMedia and Entertainment:\nMediaPlayerEnqueue, MediaPlayerDeviceClass, MediaPlayerEntity, MediaPlayerImageView, TTSCache, TextToSpeechUrlView, TextToSpeechView\nDate and Time Management:\nDateEntityDescription, DateEntity, CalendarEventView, CalendarListView, TimeEntityDescription, TimeEntity\n分类不需要过于细致，尽量避免一个短语一类的情况，严格遵守输出格式！注意：输出格式必须遵循先后顺序，即：“每类概括:\n用逗号隔开的短语”，顺序不能颠倒！\n如果没有适合的分类，某个短语可以自成一类，不需要多余解释和多余字段！\n下面是需要分类的短语: '{search_query}' ."
                },
                {
                    "role": "user",
                    "content": f"classify {search_query}"
                }
            ],
            "temperature": 0.7
        }

        # 发送请求
        response = requests.post(url, headers=headers, data=json.dumps(data))
        results.append(response.json())

    return results

def format_classification_output(responses):
    # 提取和格式化分类结果
    formatted_output = ""
    for response in responses:
        try:
            categories = response['choices'][0]['message']['content']
            formatted_output += categories.strip() + "\n\n"
        except (KeyError, IndexError):
            formatted_output += "分类失败或返回数据格式不正确。\n\n"
    return formatted_output

def process_yaml_file(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)

    phrases = [item for item in data.values()][0]
    if len(phrases) == 0 or len(phrases) == 1:
        return "\n".join(phrases)

    responses = classify_phrases(phrases)
    return format_classification_output(responses)

def main():
    input_dir = 'alternative_mode/components/class/class_statistic'
    output_dir = 'alternative_mode/components/class/classification'

    for file_name in os.listdir(input_dir):
        file_path = os.path.join(input_dir, file_name)
        result = process_yaml_file(file_path)

        output_file = os.path.join(output_dir, file_name.replace('.yaml', '.txt'))
        with open(output_file, 'w') as file:
            file.write(result)

if __name__ == "__main__":
    main()