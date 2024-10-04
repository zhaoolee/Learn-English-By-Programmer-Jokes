import csv
import re
from collections import Counter, defaultdict

def is_valid_word(word):
    # 检查单词是否只包含字母，并且长度大于1
    return word.isalpha() and len(word) > 1

def word_frequency_from_csv(file_path, column_name='English'):
    words = defaultdict(list)
    with open(file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if column_name in row:
                # 使用正则表达式分割单词，然后过滤
                for word in re.findall(r'\w+', row[column_name].lower()):
                    if is_valid_word(word):
                        words[word].append(row['ID'])  # 假设CSV文件中有一个'ID'列
    return words

def update_readme_with_word_frequency(readme_path, csv_path):
    # 获取词频数据
    word_data = word_frequency_from_csv(csv_path)
    
    # 计算总词频
    word_counts = {word: len(ids) for word, ids in word_data.items()}
    all_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    
    # 生成Markdown格式的词频表格
    table = "| Rank | Word | Frequency | Quotes |\n|------|------|-----------|--------|\n"
    for rank, (word, count) in enumerate(all_words, 1):
        quote_links = ', '.join([f'<a href="#/README?id=quote-{id}">{id}</a>' for id in word_data[word]])
        table += f"| {rank} | {word} | {count} | {quote_links} |\n"
    
    # 创建包含折叠部分的Markdown内容
    markdown_content = f"""## Word Frequency Analysis

Total unique words: {len(all_words)}

<details>
<summary>Click to view full word frequency table</summary>

{table}

</details>
"""
    
    # 读取README.md文件
    with open(readme_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 查找标记并替换内容
    start_marker = "===word_frequency_start==="
    end_marker = "===word_frequency_end==="
    start_index = content.find(start_marker)
    end_index = content.find(end_marker)
    
    if start_index != -1 and end_index != -1:
        new_content = (
            content[:start_index + len(start_marker)] +
            "\n" + markdown_content + "\n" +
            content[end_index:]
        )
        
        # 写入更新后的内容
        with open(readme_path, 'w', encoding='utf-8') as file:
            file.write(new_content)
        print("README.md has been updated successfully with full word frequency data.")
    else:
        print("Markers not found in README.md. Please check the file.")

# 使用示例
if __name__ == "__main__":
    readme_path = "README.md"  # README.md文件的路径
    csv_path = "jokes_with_id.csv"     # CSV文件的路径
    update_readme_with_word_frequency(readme_path, csv_path)