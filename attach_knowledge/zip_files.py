import os
import zipfile

def zip_folder(zip_file, folder_path):
    """
    将指定文件夹下的所有文件添加到ZIP文件中。
    """
    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(folder_path, '..')))

def zip_non_python_files(zip_file, folder_path):
    """
    将指定文件夹下的所有非Python文件添加到ZIP文件中。
    """
    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if not file.endswith('.py'):
                    zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(folder_path, '..')))

def main():
    # 合并github_result和gitee_result到lib.zip
    zip_folder('attach_knowledge/lib.zip', 'retrieval/open_lib_retrieval/github_result')
    zip_folder('attach_knowledge/lib.zip', 'retrieval/open_lib_retrieval/gitee_result')

    # 将base_platforms中的非Python文件添加到base_platforms.zip
    zip_non_python_files('attach_knowledge/base_platforms.zip', 'alternative_mode/base_platforms')

    # 将components中的非Python文件添加到components.zip
    zip_non_python_files('attach_knowledge/components.zip', 'alternative_mode/components')

if __name__ == "__main__":
    main()