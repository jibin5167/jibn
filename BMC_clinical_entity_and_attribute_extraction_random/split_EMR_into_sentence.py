import os, shutil
# from processExcel import writeData

def split_EMR_into_sentence(path):

    filenames = os.listdir(path)
    # print(len(filenames))

    parent_path = os.path.join('.','data/split_sentence')
    if os.path.exists(parent_path):
        shutil.rmtree(parent_path,True)
    os.mkdir(parent_path)

    for name in filenames:
        filepath = os.path.join(path,name)

        lines = []
        with open(filepath,'r',encoding='utf-8') as fr:
            lines = fr.readlines()

        content = ''
        for line in lines:
            content += line
        
        content = content.replace('。',',')
        content = content.replace(':',',')
        content = content.replace('：',',')
        content = content.replace('；',',')
        content = content.replace(';',',')
        content = content.replace('，',',')
        content = content.replace('1.',',')
        content = content.replace('2.',',')
        content = content.replace('3.',',')
        content = content.replace('4.',',')
        content = content.replace('5.',',')
        content = content.replace('6.',',')
        content = content.replace('7.',',')
        content = content.replace(' 1.',',')
        content = content.replace(' 2.',',')
        content = content.replace(' 3.',',')
        content = content.replace(' 4.',',')
        content = content.replace(' 5.',',')
        content = content.replace(' 6.',',')
        content = content.replace(' 7.',',')

        split_sentence = content.split(',')
        temp_sentence = []
        for sen in split_sentence:
            if len(sen.strip())>0:
                temp_sentence.append(sen.strip())

        split_sentence = temp_sentence    

        sentences = []
        for index in range(1,len(split_sentence)):
            if '转移' in split_sentence[index] and '转移' not in split_sentence[index-1]:
                sentences.append(split_sentence[index-1]+','+split_sentence[index]+'.')


        sentence_path = os.path.join(parent_path,name)
        with open(sentence_path,'w',encoding='utf-8') as fr:
            for sen in sentences:
                if name == 'record-42.txt':
                    print(sen)
                fr.write(sen)
                fr.write('\n')

def get_single_sentence(path):
        lines = []
        
        with open(path,'r',encoding='utf-8') as fr:
            lines = fr.readlines()

        content = ''
        for line in lines:
            content += line
        
        content = content.replace('。',',')
        content = content.replace(':',',')
        content = content.replace('：',',')
        content = content.replace('；',',')
        content = content.replace(';',',')
        content = content.replace('，',',')
        content = content.replace('1.',',')
        content = content.replace('2.',',')
        content = content.replace('3.',',')
        content = content.replace('4.',',')
        content = content.replace('5.',',')
        content = content.replace('6.',',')
        content = content.replace('7.',',')
        content = content.replace(' 1.',',')
        content = content.replace(' 2.',',')
        content = content.replace(' 3.',',')
        content = content.replace(' 4.',',')
        content = content.replace(' 5.',',')
        content = content.replace(' 6.',',')
        content = content.replace(' 7.',',')

        split_sentence = content.split(',')
        temp_sentence = []
        for sen in split_sentence:
            if '转移' in sen:
                temp_sentence.append(sen.strip())
        return temp_sentence
    

if __name__=='__main__':
    Excelpath = os.path.join('.','data/CHIP2018测试数据.xlsx')
    # writeData(Excelpath)
    path = os.path.join('.','data/EMR_info/EMR')
    split_EMR_into_sentence(path)