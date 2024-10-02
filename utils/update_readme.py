import csv
import re
import html

# 常量定义
START_MARKER = "===🔆==="
END_MARKER = "===🌛==="
README_FILENAME = 'README.md'
CSV_FILENAME = 'jokes.csv'

# 列宽度定义：前两列200px，第三列150px，其余自动调整
COLUMN_WIDTHS = [100, 200, 200, 150]

def csv_to_html_table(csv_filename):
    """
    将CSV文件转换为HTML表格。
    
    :param csv_filename: CSV文件的名称
    :return: 包含HTML表格的字符串
    """
    with open(csv_filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, quotechar='"', delimiter=',')
        headers = next(reader)
        rows = []
        for row in reader:
            if len(row) != len(headers):
                print(f"Warning: Row {reader.line_num} has {len(row)} columns instead of {len(headers)}.")
                print(f"Row data: {row}")
                # 如果列数不匹配，我们可以选择跳过这一行或者进行某种修复
                # 这里我们选择跳过这一行
                continue
            rows.append(row)

    print(f"Headers: {headers}")
    print(f"Number of columns: {len(headers)}")
    print(f"COLUMN_WIDTHS: {COLUMN_WIDTHS}")

    # 确保COLUMN_WIDTHS至少与headers长度相同
    column_widths = COLUMN_WIDTHS + [None] * (len(headers) - len(COLUMN_WIDTHS))
    print(f"Adjusted column_widths: {column_widths}")

    # 创建表格
    table = '<table>\n'

    # 添加表头
    table += '<tr>'
    for i, header in enumerate(headers):
        width_attr = f' width="{column_widths[i]}"' if i < len(column_widths) and column_widths[i] else ''
        table += f'<th{width_attr}><span>{html.escape(header)}</span></th>'
    table += '</tr>\n'

    # 添加数据行
    for row_index, row in enumerate(rows):
        table += '<tr>'
        for i, cell in enumerate(row):
            width_attr = f' width="{column_widths[i]}"' if i < len(column_widths) and column_widths[i] else ''
            # 为ID列添加id属性
            if i == 0:  # 假设ID是第一列
                table += f'<td{width_attr} id="quote-{cell}"><span>{html.escape(cell)}</span></td>'
            else:
                table += f'<td{width_attr}><span>{html.escape(cell)}</span></td>'
        table += '</tr>\n'

    table += '</table>'
    return table
def update_readme(readme_filename, csv_filename):
    """
    更新README文件，用HTML表格替换指定标记之间的内容。
    
    :param readme_filename: README文件的名称
    :param csv_filename: CSV文件的名称
    """
    # 读取README文件
    with open(readme_filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # 生成HTML表格
    table = csv_to_html_table(csv_filename)

    # 使用正则表达式替换内容
    pattern = f'{START_MARKER}.*?{END_MARKER}'
    replacement = f"{START_MARKER}\n{table}\n{END_MARKER}"
    updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    # 写入更新后的内容到README文件
    with open(readme_filename, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print(f"已成功更新 {readme_filename}")

def main():
    """
    主函数，用于执行README更新操作。
    """
    update_readme(README_FILENAME, CSV_FILENAME)

if __name__ == "__main__":
    main()