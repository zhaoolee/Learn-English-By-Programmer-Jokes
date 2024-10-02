import os
from utils.update_readme import update_readme
from utils.word_frequency_from_csv import update_readme_with_word_frequency

def main():
    # Define paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    readme_path = os.path.join(current_dir, 'README.md')
    csv_with_id_path = os.path.join(current_dir, 'jokes_with_id.csv')  # 新增路径
    # Call update_readme function
    print("Updating README with CSV data...")
    update_readme(readme_path, csv_with_id_path)  # 使用新的 CSV 文件

    # Call update_readme_with_word_frequency function
    print("Updating README with word frequency data...")
    update_readme_with_word_frequency(readme_path, csv_with_id_path)  # 使用新的 CSV 文件
    print("All updates completed successfully.")

if __name__ == "__main__":
    main()