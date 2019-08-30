# coding: utf-8

from __future__ import print_function

import os, sys, shutil
import tensorflow as tf
import tensorflow.contrib.keras as kr

from metastatic_sentence_classification.cnn_model import TCNNConfig, TextCNN
from data.cnews_loader import read_category, read_vocab

from preprocess.processExcel import writeData
from preprocess.split_EMR_into_sentence import split_EMR_into_sentence, get_single_sentence

try:
    bool(type(unicode))
except NameError:
    unicode = str

base_dir = './data/training-data'
vocab_dir = os.path.join(base_dir, 'EMR.vocab.txt')

save_dir = './checkpoints/textcnn'
save_path = os.path.join(save_dir, 'best_validation')  # 最佳验证结果保存路径


class CnnModel:
    def __init__(self):
        self.config = TCNNConfig()
        self.categories, self.cat_to_id = read_category()
        self.words, self.word_to_id = read_vocab(vocab_dir)
        self.config.vocab_size = len(self.words)
        self.model = TextCNN(self.config)

        self.session = tf.Session()
        self.session.run(tf.global_variables_initializer())
        saver = tf.train.Saver()
        saver.restore(sess=self.session, save_path=save_path)  # 读取保存的模型

    def predict(self, message):
        # 支持不论在python2还是python3下训练的模型都可以在2或者3的环境下运行
        content = unicode(message)
        data = [self.word_to_id[x] for x in content if x in self.word_to_id]

        feed_dict = {
            self.model.input_x: kr.preprocessing.sequence.pad_sequences([data], self.config.seq_length),
            self.model.keep_prob: 1.0
        }

        y_pred_cls = self.session.run(self.model.y_pred_cls, feed_dict=feed_dict)
        return self.categories[y_pred_cls[0]]

if __name__ == '__main__':

    # Excelpath = os.path.join('.','data/source_data/subtask2_training_part1.xlsx')
    Excelpath = os.path.join('.','data/source_data/CHIP2018测试数据.xlsx')
    writeData(Excelpath)

    EMRpath = os.path.join('.','data/EMR_info/EMR')
    split_EMR_into_sentence(EMRpath)

    inputpath = os.path.join('.','data/split_sentence')
    filenames = os.listdir(inputpath)

    outputpaths = os.path.join('.','data/transfer_sentence')
    
    EMRpath = os.path.join('.','data/EMR_info/EMR')

    cnn_model = CnnModel()

    if os.path.exists(outputpaths):
        shutil.rmtree(outputpaths)
        
    os.mkdir(outputpaths)

    for name in filenames:
        filepath = os.path.join(inputpath,name)
        EMRfilepath = os.path.join(EMRpath,name)
        
        result = get_single_sentence(EMRfilepath)

        with open(filepath,encoding='UTF-8') as fr:
            lines = fr.readlines()
        fr.close

        for line in lines:
            if cnn_model.predict(line) == '部位':
                temp = line.split(',')
                for t in temp:
                    if t not in result:
                        result.append(t)

        outputpath = os.path.join(outputpaths,name)
        f = open(outputpath,'w+',encoding='utf-8')

        text = ''
    
        for index in range(len(result)):
            text += (result[index]+',')

        text = text.replace('\n','')
        text = text.replace('.','')

        # if name == 'record-42.txt':
        #     print(text)

        list_sentence = text.split(',')


        postprocess_list_sentence = []
        for sen in list_sentence:
            if '癌' in sen:
                sen = sen[sen.index('癌')+1:]
            # if '转移' in sen:
            #     sen = sen[:sen.index('转移')]
            if 'MT' in sen:
                sen = sen[sen.index('MT')+2:]
            if '血管瘤' in sen:
                sen = sen[sen.index('血管瘤')+3:]
            sen = sen.strip()
                
            if len(sen)>0:
                postprocess_list_sentence.append(sen)
        
        # if name =='record-35.txt':
        #     for ls in postprocess_list_sentence:
        #         print(ls)
        # if name == 'record-42.txt':
        #     for p in postprocess_list_sentence:
        #         print(p)


        set_sentence = set(postprocess_list_sentence)
        
        metastatic = ''
        for sen in set_sentence:
            metastatic += (sen+'   ,   ')

        f.write(metastatic)
