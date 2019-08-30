import os

def process_trainingdata():

    filepath = './LSTM_for_metastatic/data_path/train_data'
    
    lst = []
    with open(filepath,'r',encoding='utf-8') as fr:
        lines = fr.readlines()
        for line in lines:
            s = line.split('\t')
            if len(s) == 2:
                s[1] = s[1].replace('\n','')
                if  not s[1] == 'B-SU' and not s[1] == 'I-SU' and not s[1] == 'B-DR' and not s[1] == 'I-DR' and not s[1] == 'B-IS' and not s[1] == 'I-IS' and not s[1] == 'B-SD' and not s[1] == 'I-SD':
                    lst.append(line)
            else:
                lst.append(line)

    output = './LSTM_for_metastatic/data_path/train_data.txt'
    with open(output,'w',encoding='utf-8') as fr:
        for ls in lst:
            fr.write(ls)
            # fr.write('\n')

if __name__=='__main__':
    process_trainingdata()


