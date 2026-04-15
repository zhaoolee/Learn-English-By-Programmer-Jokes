import os
from utils.joke_skill import generate_skill_assets
from utils.update_readme import update_readme
from utils.word_frequency_from_csv import update_readme_with_word_frequency


def main():
    # Define paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    readme_path = os.path.join(current_dir, 'README.md')
    csv_with_id_path = os.path.join(current_dir, 'jokes_with_id.csv')
    references_dir = os.path.join(current_dir, 'references')

    # Call update_readme function
    print("Updating README with CSV data...")
    update_readme(readme_path, csv_with_id_path)

    # Call update_readme_with_word_frequency function
    print("Updating README with word frequency data...")
    update_readme_with_word_frequency(readme_path, csv_with_id_path)

    # Generate Hermes skill reference files
    print("Generating Hermes skill reference files...")
    generate_skill_assets(csv_with_id_path, references_dir)
    print("All updates completed successfully.")

    # 将README.md文件复制到docs目录下
    docs_path = os.path.join(current_dir, 'docs')
    if not os.path.exists(docs_path):
        os.makedirs(docs_path)
    readme_docs_path = os.path.join(docs_path, 'README.md')
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    with open(readme_docs_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"已成功更新 {readme_docs_path}")


if __name__ == "__main__":
    main()
