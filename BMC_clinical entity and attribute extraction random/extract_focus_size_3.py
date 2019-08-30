# -*- coding: utf-8 -*-
"""
@author: Administrator
"""
import re, os, shutil

def focus_size_pattern():
    filenames = os.listdir('./data/EMR_info/EMR')
    
    FOCUS_path = './data/FOCUS'
    if os.path.exists(FOCUS_path):
        shutil.rmtree(FOCUS_path, True)
    os.mkdir(FOCUS_path)

    for f in filenames:
        index = re.search('\d\d?\d?',f).group(0)
        
        path_tumer = './data/TUMER_SITE/tumer-'+index+'.txt'
        path_record = './data/EMR_info/EMR/record-'+index+'.txt'
        tumer_list = []
        focus_list = []
        focus_size = []
        medical_record = ''
        with open(path_tumer, 'r', encoding = 'UTF-8') as fr:
            line = fr.readlines()
            if len(line)>0:
                for l in line:
                    l = l[:l.index('\n')]
                    tumer_list.append(l)
        
        with open(path_record, 'r', encoding = 'UTF-8') as f:
            line = f.readlines()
            if len(line)>0:
                for l in line:
                    medical_record += l
                    
        # medical_record = medical_record.replace(':','。')
        medical_record = medical_record.replace('；','。')
        # medical_record = medical_record.replace('：','。')
        medical_record = medical_record.replace(';','。')
        # medical_record = medical_record.replace('、','。')
        medical_record, number = re.subn('1\.\D', '。', medical_record)
        medical_record, number = re.subn('2\.\D', '。', medical_record)
        medical_record, number = re.subn('3\.\D', '。', medical_record)
        medical_record, number = re.subn('4\.\D', '。', medical_record)
        medical_record, number = re.subn('5\.\D', '。', medical_record)
        medical_record, number = re.subn('6\.\D', '。', medical_record)
        medical_record, number = re.subn('7\.\D', '。', medical_record)
        medical_record, number = re.subn('8\.\D', '。', medical_record)
        medical_record, number = re.subn('9\.\D', '。', medical_record)
        medical_record, number = re.subn('\D\.\D', '。', medical_record)
        
        record_split = medical_record.split('。')
        
        if len(tumer_list)>0 and len(tumer_list[0])>0:
            for l in tumer_list:
                for r in record_split:
                    if l in r and not r in focus_list:
                        focus_list.append(r)
                        # if index == str(123):
                        #     print(r)
                    if '左乳腺' in l:
                        if '左侧乳腺' in r and not r in focus_list:
                            focus_list.append(r)
                    if '右乳腺' in l:
                        if '右侧乳腺' in r and not r in focus_list:
                            focus_list.append(r)
                    if '右侧乳腺' in l:
                        if '右乳腺' in r and not r in focus_list:
                            focus_list.append(r)
                    if '左侧乳腺' in l:
                        if '左乳腺' in r and not r in focus_list:
                            focus_list.append(r)

        # for l in tumer_list:
        #     tumer_word = set(l)
        #     for r in record_split:
        #         record_word = set(r)
        #         hybrid = tumer_word | record_word

        #         if len(hybrid)==len(record_word) and len(hybrid)>len(tumer_word) and not r in focus_list:
        #             focus_list.append(r)

                    
        if len(focus_list)>0:
            for f in focus_list:
                temp_list = []
                pattern = re.compile('((不足)?\d?\d?\d?\.?\d?\d(([CM]M?)|(.?.?[\*×X~].?\d?\d?\d?\.?\d?\d?))*[CM]M)')
                m = pattern.findall(f)
                
                # if len(m)>0:
                #     temp_list.append(m[0][0])
                if len(m)>0:
                    for mm in m:
                        temp_list.append(mm[0])

                if len(temp_list)>0:
                    for tl in temp_list:
                        flag = f.index(tl)
                        sentence = f[:flag]
                        if '淋巴结' in sentence and '融合' not in sentence and tl in temp_list:
                            temp_list.remove(tl)
                        if '距' in sentence or '短径' in sentence or '类结节影' in sentence:
                            if  tl in temp_list:
                                temp_list.remove(tl)
                        if '术后' in sentence and tl in temp_list:
                            temp_list.remove(tl)
                focus_size.extend(temp_list)
        
        focus_path = os.path.join('.',FOCUS_path,'focus-'+index+'.txt')
        with open(focus_path, 'w', encoding='utf-8') as ff:
            if len(focus_size)>0:
                for focus in focus_size:
                    ff.write(focus)
                    ff.write('\n')
            else:
                ff.write('')
        ff.close
        
if __name__=='__main__':
   focus_size_pattern()
    