import os

def find_difference():
    py_path = os.path.join('.','transfer_sentence.txt')
    java_path = os.path.join('.','sentence.txt')

    py_sentence = []
    java_sentence = []

    with open(py_path,'r',encoding='utf-8') as f1:
        py_sentence = f1.readlines()

    with open(java_path,'r',encoding='utf-8') as f1:
        java_sentence = f1.readlines()

    common = []

    for psen in py_sentence:
        for jsen in java_sentence:
            if jsen == psen:
                if psen not in common:
                    common.append(psen)

    remain = []
    for p in py_sentence:
        if p not in common:
            remain.append(p)

    output_path = os.path.join('.','remain.txt')

    with open(output_path,'w',encoding='utf-8') as fr:
        for r in remain:
            fr.write(r)
            fr.write('\n')

    # print(len(common))

if __name__=='__main__':
    find_difference()