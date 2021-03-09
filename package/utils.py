import random


# 获取随机数
def get_random_array(count):
    arr = [i for i in range(count)]
    for i in range(4):
        random.shuffle(arr)
    return arr

# 移除空元素
def remove_null_str(data):
    new_data = []
    for d in data:
        if d != '':
            new_data.append(d)
    return new_data
