import csv
import sqlite3

csv_file = r"../TuiJian/result.csv"
# 打开CSV文件
with open(csv_file, 'r', encoding='utf-8') as file:
    csv_data = file.readlines()

    # 连接到SQLite数据库
    db_file = r"../TuiJian/db.sqlite3"
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # 创建表（如果不存在）
    cursor.execute("CREATE TABLE IF NOT EXISTS TuiJian_case_item (name TEXT, text TEXT, itype TEXT, biaoqian TEXT, lianjie TEXT)")

    # 插入数据
    for row in csv_data[:1]:
        item_list = row.split(',')
        a = item_list
        if len(item_list) != 5:
            continue
        else:
            cursor.execute("INSERT INTO TuiJian_case_item (name, text, itype, biaoqian, lianjie) VALUES (?, ?, ?, ?, ?)", a)
            print("========================{}\t插入成功=======================\n".format(a[0]))

    # 提交更改并关闭连接
    conn.commit()
    conn.close()