# -*- coding: utf-8 -*-

from PyQt5.Qt import *
import pandas as pd
import  warnings

import jieba
import collections
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np


warnings.filterwarnings("ignore")

import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = 'SimHei'  ## 设置中文显示
plt.rcParams['axes.unicode_minus'] = False

# 结合了多个停用词表
def open_dict(Dict='hahah', path='./emotion_dict/'):
    path = path + '%s.txt' % Dict
    dictionary = open(path,encoding='utf8', errors='ignore')
    dict = []
    for word in dictionary:
        word = word.strip('\n')
        word = word.strip(' ')
        dict.append(word)
    return dict
##构建 停顿词
stopwords=[]
with open('./stopwords/stopword.txt',encoding='utf8',errors='ignore') as f:
    for line in f.readlines():
            # print(line)
        stopwords.append(line.strip())
# 积极情感词典
posdict = open_dict(Dict='posdict')


# 消极情感词典
negdict = open_dict(Dict='negdict')

f = open('./emotion_dict/微博情感词典.txt',  encoding='gb18030',errors='ignore')
words = []
value = []
for word in f.readlines():
    words.append(word.split(' ')[0])
    value.append(float(word.split(' ')[1].strip('\n')))

c = {'words': words,'value': value}
fd = pd.DataFrame(c)
pos = fd['words'][fd.value > 0]
posdict = posdict + list(pos)  ##加入微博相关的正向情感词
neg = fd['words'][fd.value < 0]
negdict = negdict + list(neg)  ##加入微博相关的负向情感词
alldict = posdict + negdict



#预处理函数
def remove_characters(sentence):  # 去停用词
    cleanwordlist = [word for word in sentence if word.lower() not in stopwords]
    filtered_text = ' '.join(cleanwordlist)
    return filtered_text


def remove_emotion_characters(sentence):  # 抽取情感词
    wordlist = [word for word in sentence if word in alldict]
    filtered_text = ' '.join(wordlist)
    return filtered_text


def text_normalize(text):
    text_split = []
    for line in text:
        text_split.append(list(jieba.cut(line)))
    text_normal = []
    for word_list in text_split:
        text_normal.append(remove_characters(word_list))
    return text_normal


def text_normalize2(text):  # 基于情感词典的预处理
    text_split = []
    for line in text:
        text_split.append(list(jieba.cut(line)))
    text_normal = []
    for word_list in text_split:
        text_normal.append(remove_emotion_characters(word_list))
    return text_normal


# 单用户词云
def single_user_wordcount(df, user_name):
    new_df = df[df['user'] == user_name]
    print(new_df)
    all_comment = ''
    for elem in new_df['content'].values:
        all_comment = all_comment + elem
    split_words = list(jieba.cut(all_comment))  # 分词
    filtered_corpus = remove_characters(split_words)  # 去停用词
    filtered_corpus = [word for word in split_words if word not in stopwords]
    ##词频统计
    word_counts = collections.Counter(filtered_corpus)  # 对分词做词频统计
    word_counts_top10 = word_counts.most_common(15)  # 获取前10最高频的词
    print(word_counts_top10)  # 输出检查
    ##词云制作
    wordcloud_1 = WordCloud(
        font_path='C:/Windows/Fonts/simkai.ttf',  # 设置字体，为电脑自带黑体
        max_words=200,  # 最多显示词数
        max_font_size=100,  # 字体最大值)
        background_color='white',
    )
    wordcloud = wordcloud_1.generate_from_frequencies(word_counts)
    wordcloud.to_file('./{}.jpg'.format(user_name))
    plt.figure(figsize=(16, 12))
    plt.show()


# 单用户情感变化
def single_user_sentence(df, user_name):
    new_df = df[df['user'] == user_name]
    print(new_df)

    #
    x = np.arange(len(new_df['time'].values))
    # px=[elem.split('日')[0].replace('月','-') for elem in x]
    # print(px)
    new_df['score'] = new_df['score'].astype(float)
    y = new_df['score'].values
    y_new = [round(elem, 2) for elem in y]
    print(y)
    plt.figure()
    plt.plot(x, y_new)  # 折线图
    plt.title("{}".format(user_name))  # 显示图名

    # plt.ylim(-1, 3)
    plt.savefig('{}1.jpg'.format(user_name))
    plt.show()


def score_to_label(x):
    if float(x)>0:
        return '积极'
    if float(x)==0:
        return '中性'
    else:
        return '消极'
#单用户占比
def single_user_bingtu(df,user_name):
    print('etl for pic2.....')
    new_df = df[df['user'] == user_name]
    new_df['label']=new_df['score'].map(lambda x:score_to_label(x))
    churnvalue = new_df["label"].value_counts()
    labels = new_df["label"].value_counts().index
    print('churnvalue',churnvalue)
    print('labels', labels)
    plt.figure()
    plt.pie(churnvalue, labels=labels, autopct='%1.1f%%',
            shadow=True)
    plt.title("{}情绪占比".format(user_name))
    plt.savefig('{}2.jpg'.format(user_name))
    plt.show()



class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.files=[]
        self.initUI()
        # 评分后的文件
        self.score_file='result_for_all.csv'
        self.score_df=pd.read_csv('result_for_all.csv',header=None,sep='|',names=['time','user','content','score'])

        # 原始文件
        self.original_file='C:/Users/Administrator/Downloads/微博-新冠肺炎（1-2月） - 复件.csv'
        #self.original_df= 'C:/Users/Administrator/Downloads/微博-新冠肺炎（1-2月） - 复件.csv'

    def clear_file(self):
        self.l_test_load.setText("")
        self.l_train_load.setText("")
        pix = QPixmap("")
        self.l_picture.setPixmap(pix)
        self.table.clearContents()

    def showMsg(self):
        QMessageBox.warning(self, "警告", "请先选择数据文件路径", QMessageBox.Yes)

    def showMsgEnd(self):
        QMessageBox.warning(self, "提示", "已经是最后一张图片", QMessageBox.Yes)

    def showMsgStart(self):
        QMessageBox.warning(self, "提示", "已经是第一张图片", QMessageBox.Yes)

    def showNextPicture(self):
        if self.index < len(self.p_load)-1:
            self.index = self.index + 1
            pix = QPixmap(self.p_load[self.index])
            self.l_picture.setPixmap(pix)
        else:
            self.showMsgEnd()

    def showBackPicture(self):
        if self.index > 0:
            self.index = self.index - 1
            pix = QPixmap(self.p_load[self.index])
            self.l_picture.setPixmap(pix)
        else:
            self.showMsgStart()

    #找出发微博比较多的客户
    def get_user_names(self):
        user_df = pd.read_csv('result_for_all.csv', header=None, sep='|', names=['time', 'user', 'content', 'score'])
        user_df = user_df[1:]
        use_cnt = user_df.groupby(['user']).count().reset_index()
        use_cnt_list = use_cnt[use_cnt['time'] > 30]['user'].values
        return use_cnt_list


    def process(self):
        import numpy as np
        import pandas as pd

        user_name=self.cb.currentText()
        print(user_name)

        single_user_wordcount(self.score_df,user_name)

        pic_name=str(user_name)+'.jpg'
        p_load = [pic_name]
        self.p_load = p_load
        self.index = 0
        pix = QPixmap(self.p_load[self.index])
        self.l_picture.setPixmap(pix)

        new_df = self.score_df[self.score_df['user'] == user_name]
        content=new_df['content'].values
        score = new_df['score'].values
        for i in range(0, 10, 1):
            self.table.setItem(i, 0, QTableWidgetItem(str(content[i])))
            self.table.setItem(i, 1, QTableWidgetItem(str(score[i])))

    def process2(self):
        import numpy as np
        import pandas as pd

        user_name = self.cb.currentText()
        print(user_name)

        single_user_sentence(self.score_df, user_name)
        single_user_bingtu(self.score_df, user_name)

        pic_name1 = str(user_name) + '1.jpg'
        pic_name2 = str(user_name) + '2.jpg'
        p_load = [pic_name1,pic_name2]
        self.p_load = p_load
        self.index = 0
        pix = QPixmap(self.p_load[self.index])
        self.l_picture.setPixmap(pix)

    def process3(self):
        pass
        #获取用户的情况
        # df = pd.read_csv(self.original_file, encoding='gb18030', warn_bad_lines=False, error_bad_lines=False, header=None)
        # df = df[1:]
        # print(df.columns)
        # df2 = df[[0,1, 2, 3, 4, 5, 6, 7]]
        # #用户ID	用户主页链接	微博发布时间	用户名	微博内容	转发数	评论数	点赞数
        #
        #
        # df2=df2.fillna(0)
        # df2=df2[[0, 1, 2, 3, 5, 6, 7]]
        # print(df2)
        #
        # df2[5]=df2[5].astype(float)
        # df2[6] = df2[6].astype(float)
        # df2[7] = df2[7].astype(float)
        #
        # 转发数=sum(df2[5].values)
        # 评论数=sum(df2[6].values)
        # 点赞数=sum(df2[7].values)
        #
        # mystr='用户：'+str(user_name) +' 共发送 {} 条微博， 转发数共计 {} 次，\n评论数共计 {} 次，点赞数共计 {} 次'.format(len(df2),str(转发数),str(评论数),str(点赞数))
        # print(mystr)
        # self.l_picture.setText(mystr)

    def initUI(self):
        # 设置窗口
        self.setWindowTitle("基于情感词典的新冠疫情监控系统")
        self.resize(1000, 600)
        self.move(400, 200)

        # 设置显示测试数据文件名称及路径
        self.l_test_name = QLabel(self)
        self.l_test_name.setText("选择用户:")
        self.l_test_name.resize(100, 20)
        self.l_test_name.move(10, 20)

        # 下拉菜单
        self.cb = QComboBox(self)  # 创建一个 Qcombo  box实例
        self.cb.resize(550, 20)
        self.cb.move(110, 20)
        ID_LIST = self.get_user_names()
        for elem in ID_LIST:
            self.cb.addItem(elem)  # 添加 item




        # 设置文件选择按钮
        self.b_file = QPushButton(self)
        self.b_file.setText("词云分析")
        self.b_file.move(700, 20)
        self.b_file.clicked.connect(self.process)

        # 设置清空文件按钮
        self.b_clear = QPushButton(self)
        self.b_clear.setText("情感分析")
        self.b_clear.move(800, 20)
        self.b_clear.clicked.connect(self.process2)

        # 设置开始按钮
        self.b_start = QPushButton(self)
        self.b_start.setText("其余维度画像")
        self.b_start.move(900, 20)
        self.b_start.clicked.connect(self.process3)



        # 设置数据展示
        horizontalHeader = ['content', 'score']
        self.table = QTableWidget(self)
        self.table.setColumnCount(2)
        self.table.setRowCount(10)
        self.table.horizontalHeader().setDefaultSectionSize(200)
        self.table.verticalHeader().setDefaultSectionSize(45)
        # self.table.horizontalHeader().resizeSection(0, 300)
        self.table.verticalHeader().resizeSection(0, 40)
        self.table.setHorizontalHeaderLabels(horizontalHeader)
        self.table.resize(410,500)
        self.table.move(20, 60)

        # 设置图片展示
        self.l_picture = QLabel(self)
        self.l_picture.setGeometry(450, 60, 500, 500)
        self.l_picture.setStyleSheet("border: 2px solid black")
        self.l_picture.setScaledContents(True)

        # 设置展示下一张图片
        self.b_next = QPushButton(self)
        self.b_next.setText("下一张")
        self.b_next.move(850, 565)
        self.b_next.clicked.connect(self.showNextPicture)

        # 设置展示上一张图片
        self.b_next = QPushButton(self)
        self.b_next.setText("上一张")
        self.b_next.move(750, 565)
        self.b_next.clicked.connect(self.showBackPicture)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())