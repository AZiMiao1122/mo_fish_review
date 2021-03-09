import pandas as pd
import synonyms as sy
import os
from package.sql_conf import db_cursor, db_connect
from package.sql_data import *
from package.utils import *
import re
import warnings

warnings.filterwarnings('ignore')  # 移除warning打印


def press(key):
    global current_key
    try:
        current_key = key.char
    except AttributeError:
        current_key = key
    return False


# 新增单词
def insert_a_word(word, paraphrase):
    d = pd.read_sql(get_count_by_word(word), db_connect)
    if d['count'][0] > 0:
        print("该单词已存在，继续插入请按c,返回主菜单请按任意键...")
        insert = str(input())
        if insert == 'c':
            return first_main()
        else:
            return main()
    sql = insert_one(word, paraphrase)
    try:
        db_cursor.execute(sql)
        db_connect.commit()
        print("插入成功")
        return True
    except:
        print("插入异常")
        return False


def first_main():
    print("请输入单词、释义，用/分割:")
    insert_word = input().split("/")
    if len(insert_word) == 2:
        if insert_a_word(insert_word[0], insert_word[1]):
            print("插入成功,继续插入请按c,返回主菜单请按m。")
            f_m = input()
            if f_m == 'c':
                print('\n')
                return first_main()
            elif f_m == 'm':
                return main()
    else:
        print("分词错误，请重新输入...")
        return first_main()


def four_main():
    print("说明：这里会乱序给出一个单词，然后你只需要输入该单词的中文意思，按回车。只要相似度>60%，那就算是正确，每个单词会复习5遍"
          + ",那么该单词就不会再进行复习。")
    total_df_data = pd.read_sql(select(), db_connect)
    print("总共有%d个单词，若要中途退出请输入: >>> 并返回主菜单" % total_df_data.shape[0])
    true_count, error_count, review_count = 0, 0, 0
    not_playing = False
    for rem in range(5):
        temp_data = total_df_data.loc[total_df_data['review_count'] == rem].reset_index()
        random_index = get_random_array(temp_data.shape[0])
        for index in random_index:
            this_id = temp_data['id'][index]
            this_word = temp_data['word'][index]
            this_annotation = temp_data['paraphrase'][index]
            rate = 0.0
            print(this_word)
            print("请输入该单词的正确意思，不会请瞎几把填：")
            chinese = input_str()
            if chinese == '>>>':
                not_playing = True
                break
            this_annotation_sp = re.split('[ ,.，。;/]', str(this_annotation))  # 分割
            this_annotation_sp = remove_null_str(this_annotation_sp)
            for t in this_annotation_sp:
                temp_rate = sy.compare(str(chinese), str(t), seg=True)
                if temp_rate > rate:
                    rate = temp_rate
            if rate >= 0.6:
                print("✅(%f)" % rate)
                true_count = true_count + 1
                # 更新rem
                db_cursor.execute(update_rem(this_id))
                db_connect.commit()
            else:
                print("❎(%f),正确词义:%s" % (rate, this_annotation))
                error_count = error_count + 1
        if not_playing:
            break
    if error_count != 0 or true_count != 0:
        print("总共练习了%d个单词，错误%d个，正确%d个，正确率%f" % (
            true_count + error_count, error_count, true_count, true_count / (error_count + true_count)))
    return main()


def input_str():
    try:
        s = str(input())
        if s == '':
            print("不能输入空字符串，请重新输入...")
            return input_str()
        return s
    except Exception:
        print("输入异常，请重新输入.")
        return input()


# 主方法
def main():
    print("【主菜单】请根据按键操作:\n1----新增单词\n4----词汇练习\nb----退出")
    try:
        m = input()
        if str(m) == '1':
            os.system('clear')
            first_main()
        elif str(m) == '4':
            four_main()
        elif str(m) == 'b':
            return
        else:
            print("操作错误，请重新输入...")
            return main()
    except Exception as e:
        print("输入异常~")
        print(e)
        return main()


if __name__ == '__main__':
    main()
