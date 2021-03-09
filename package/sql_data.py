# 查询数量
def get_count_by_word(word):
    return "select count(*) as count from word_review where word = '%s'" % word


# 插入
def insert_one(word, paraphrase):
    return '''insert into word_review (word,paraphrase) value ('%s','%s')''' % (
        word, paraphrase)


# 查询
def select():
    return "select * from word_review where review_count < 5"


def update_rem(id):
    return "update word_review set review_count = review_count + 1 where id = %d " % id
