import os
import ast
from collections import Counter
import yaml

class MyASTVisitor(ast.NodeVisitor):
    def __init__(self):
        self.classes = []

    def visit_ClassDef(self, node):
        self.classes.append(node.name)
        self.generic_visit(node)

def read_file_names(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
        return data['file_names']

def find_files(root_path, file_names):
    target_files = {}
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file in file_names:
                file_path = os.path.join(root, file)
                if file in target_files:
                    target_files[file].append(file_path)
                else:
                    target_files[file] = [file_path]
    return target_files

def analyze_files(target_files):
    templates = {}
    for file_name, paths in target_files.items():
        if not file_name.endswith('.py'):  # 只处理 Python 文件
            continue

        class_names = set()
        for file_path in paths:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    tree = ast.parse(content)
                    visitor = MyASTVisitor()
                    visitor.visit(tree)
                    class_names.update(visitor.classes)
            except (SyntaxError, UnicodeDecodeError) as e:
                print(f"Error in file {file_path}: {e}")

        templates[file_name] = sorted(class_names)
    return templates

def save_statistics_to_yaml(templates, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for file_name, class_names in templates.items():
        output_path = os.path.join(output_dir, f"{file_name}_class.yaml")
        with open(output_path, 'w', encoding='utf-8') as file:
            yaml.dump({file_name: class_names}, file, default_flow_style=False)

def main():
    file_names_path = 'alternative_mode/base_platforms/file_names.yaml'
    root_path = 'source/ha_components'
    output_statistics_dir = 'alternative_mode/base_platforms/class/class_statistic'

    file_names = read_file_names(file_names_path)
    target_files = find_files(root_path, file_names)
    templates = analyze_files(target_files)
    save_statistics_to_yaml(templates, output_statistics_dir)

if __name__ == "__main__":
    main()
