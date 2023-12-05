import os
import yaml

def read_base_platforms(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
        return data['base_platforms']

def collect_file_names(base_platforms, root_path):
    file_names = set()
    for base_path in base_platforms:
        # 调整路径格式并连接根路径
        relative_path = base_path.strip("/**").replace("homeassistant/components/", "").replace("\\", "/")
        full_path = os.path.join(root_path, relative_path)

        if not os.path.exists(full_path):
            print(f"Directory not found: {full_path}")
            continue

        for root, dirs, files in os.walk(full_path):
            for file in files:
                file_names.add(file)
    
    return sorted(file_names)

def save_file_names(file_names, output_file):
    with open(output_file, 'w') as file:
        yaml.dump({"file_names": file_names}, file, default_flow_style=False)

def main():
    core_files_path = 'source/.core_files.yaml'  # 替换为实际的 .core_files.yaml 路径
    root_path = 'source/ha_components'  # 替换为实际的 base_platforms 根目录
    output_file = 'alternative_mode/base_platforms/file_names.yaml'

    base_platforms = read_base_platforms(core_files_path)
    file_names = collect_file_names(base_platforms, root_path)
    save_file_names(file_names, output_file)

if __name__ == "__main__":
    main()
