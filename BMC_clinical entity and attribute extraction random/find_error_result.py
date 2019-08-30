import os

def find_error_entity():
    gold_path = os.path.join('.','gold.txt')
    recognition_path = os.path.join('.','result.txt')
    comparation_path = os.path.join('.','comparation.txt')

    gold_results = []
    recognition_results = []

    comparation_results = []
    with open(gold_path,encoding='utf-8') as f1:
        lines1 = f1.readlines()
        for line in lines1:
            gold_results.append(line)

    with open(recognition_path, encoding="utf-8") as f2:
        lines2 = f2.readlines()
        for line in lines2:
            recognition_results.append(line)

    for i in range(len(gold_results)):
        if gold_results[i] not in recognition_results[i]:
            result = gold_results[i]+'\t'+recognition_results[i]
            comparation_results.append(result)
            comparation_results.append('\n')

    with open(comparation_path,'w+',encoding='utf-8') as f3:
        for element in comparation_results:
            f3.write(element)
            f3.writelines

if __name__=='__main__':
    find_error_entity()