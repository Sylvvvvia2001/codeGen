import os
import ast
import yaml
import re
import astor

class MyASTVisitor(ast.NodeVisitor):
    def __init__(self):
        self.tuples = set()
        self.sets = set()
        self.schemas = set()

    def visit_Tuple(self, node):
        self.tuples.add(astor.to_source(node).strip())
        self.generic_visit(node)

    def visit_Set(self, node):
        self.sets.add(astor.to_source(node).strip())
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

        visitor = MyASTVisitor()
        for file_path in paths:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    tree = ast.parse(content)
                    visitor.visit(tree)
            except (SyntaxError, UnicodeDecodeError) as e:
                print(f"Error in file {file_path}: {e}")

        templates[file_name] = {
            'tuples': sorted(visitor.tuples),
            'sets': sorted(visitor.sets),
            'schemas': sorted(visitor.schemas)
        }
    return templates

def save_statistics_to_yaml(templates, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for file_name, stats in templates.items():
        output_path = os.path.join(output_dir, f"{file_name}_other_sentence.yaml")
        with open(output_path, 'w', encoding='utf-8') as file:
            yaml.dump({file_name: stats}, file, default_flow_style=False)

def main():
    file_names_path = 'alternative_mode/base_platforms/file_names.yaml'
    root_path = 'source/ha_components'
    output_statistics_dir = 'alternative_mode/base_platforms/other_sentence/sentence_statistic'

    file_names = read_file_names(file_names_path)
    target_files = find_files(root_path, file_names)
    templates = analyze_files(target_files)
    save_statistics_to_yaml(templates, output_statistics_dir)

if __name__ == "__main__":
    main()
