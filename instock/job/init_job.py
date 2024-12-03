#!/usr/local/bin/python3
# -*- coding: utf-8 -*-


import logging
import sqlite3
import os.path
import sys

cpath_current = os.path.dirname(os.path.dirname(__file__))
cpath = os.path.abspath(os.path.join(cpath_current, os.pardir))
sys.path.append(cpath)
import instock.lib.database as mdb

__author__ = 'myh '
__date__ = '2023/3/10 '


# 创建新数据库。
def create_new_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Example of creating a table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS example_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        value REAL
    )
    ''')

    # Example of inserting data
    cursor.execute('INSERT INTO example_table (name, value) VALUES (?, ?)', ('example', 123.45))
    conn.commit()

    # Example of querying data
    cursor.execute('SELECT * FROM example_table')
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    conn.close()


# 创建基础表。
def create_new_base_table():
    with sqlite3.connect('database.db') as conn:
        with conn.cursor() as db:
            create_table_sql = """CREATE TABLE IF NOT EXISTS `cn_stock_attention` (
                                  `datetime` datetime(0) NULL DEFAULT NULL, 
                                  `code` varchar(6) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                                  PRIMARY KEY (`code`) USING BTREE,
                                  INDEX `INIX_DATETIME`(`datetime`) USING BTREE
                                  ) CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;"""
            db.execute(create_table_sql)


def check_database():
    with sqlite3.connect('database.db') as conn:
        with conn.cursor() as db:
            db.execute(" select 1 ")


def main():
    # 检查，如果执行 select 1 失败，说明数据库不存在，然后创建一个新的数据库。
    try:
        check_database()
    except Exception as e:
        logging.error("执行信息：数据库不存在，将创建。")
        # 检查数据库失败，
        create_new_database()
    # 执行数据初始化。


# main函数入口
if __name__ == '__main__':
    main()
