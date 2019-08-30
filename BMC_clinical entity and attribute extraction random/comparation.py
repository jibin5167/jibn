import os, sys

def get_tumer_result():
    gold_path = './data/EMR_info/TUMER'
    predict_path = './data/TUMER_SITE'

    if not os.path.exists(gold_path):
        print('缺少肿瘤原发部位标注数据')
        sys.exit()

    if not os.path.exists(predict_path):
        print('缺少肿瘤原发部位预测数据')
        sys.exit()

    gold_filenames = os.listdir(gold_path)

    all_predict = 0
    correct = 0
    all_gold = 0


    for gf in gold_filenames:
        gold_filepath = os.path.join(gold_path,gf)
        predict_filepath = os.path.join(predict_path,gf)

        gold_tumer = []
        predict_tumer = []
        gold = []
        predict = []
        
        with open(gold_filepath,'r',encoding='utf-8') as gf:
            gold_tumer = gf.readlines()
        gf.close

        for line in gold_tumer:
            line = line.replace('\n','')
            line = line.strip()
            if ',' in line:
                splits = line.split(',')
                gold.extend(splits)
            else:
                gold.append(line)

        with open(predict_filepath,'r',encoding='utf-8') as pf:
            predict_tumer = pf.readlines()
        pf.close

        for line in predict_tumer:
            line = line.replace('\n','')
            line = line.strip()
            predict.append(line)

        medium_predict = set(predict)
        predict = list(medium_predict)

        # temp_predict = []
        # temp_predict.extend(predict)

        # if len(predict)>1:
        #     for p_comparing in temp_predict:
        #         compos_comparing = set(p_comparing)
        #         # print('比较对象')
        #         # print (compos_comparing)
        #         # print()
        #         len_comparing = len(compos_comparing)
        #         for p_compared in temp_predict:
        #             compos_compared = set(p_compared)
        #             # print(compos_compared)
        #             len_compared = len(compos_compared)

        #             merged = compos_compared | compos_comparing
        #             # print(merged)
        #             # print()
        #             len_merged = len(merged)

        #             if len_merged > len_comparing and len_merged == len_compared:
        #                 if p_comparing in predict:
        #                     predict.remove(p_comparing)

        # if not len(temp_predict) == len(predict):
        #     print(gold_filepath)

        all_predict += len(predict)
        all_gold += len(gold)

        for item in predict:
            if item in gold:
                correct += 1

        if not set(predict) == set(gold):
            print(gold_filepath)
    print('-----------------------------------tumer')
    # correct = 199
    # all_predict = 225
    # all_gold = 213
    precision = float(float(correct)/float(all_predict))
    recall = float(float(correct)/float(all_gold))
    F_value = float(precision*recall*2.0)/(precision+recall)

    print(str(correct)+'\t'+str(all_predict)+'\t'+str(all_gold))
    print(precision)
    print(recall)
    print(F_value)
    
    return correct, all_predict, all_gold


def get_focus_result():
    gold_path = './data/EMR_info/FOCUS'
    predict_path = './data/FOCUS'

    if not os.path.exists(gold_path):
        print('缺少肿瘤大小标注数据')
        sys.exit()

    if not os.path.exists(predict_path):
        print('缺少肿瘤大小预测数据')
        sys.exit()

    gold_filenames = os.listdir(gold_path)

    all_predict = 0
    correct = 0
    all_gold = 0


    for gf in gold_filenames:
        gold_filepath = os.path.join(gold_path,gf)
        predict_filepath = os.path.join(predict_path,gf)

        gold_tumer = []
        predict_tumer = []
        gold = []
        predict = []
        
        with open(gold_filepath,'r',encoding='utf-8') as gf:
            gold_tumer = gf.readlines()
        gf.close

        for line in gold_tumer:
            line = line.replace('\n','')
            line = line.strip()
            if ',' in line:
                splits = line.split(',')
                gold.extend(splits)
            else:
                gold.append(line)

        with open(predict_filepath,'r',encoding='utf-8') as pf:
            predict_tumer = pf.readlines()
        pf.close

        for line in predict_tumer:
            line = line.replace('\n','')
            line = line.strip()
            predict.append(line)

        medium_predict = set(predict)
        predict = list(medium_predict)

        all_predict += len(predict)
        all_gold += len(gold)

        for item in predict:
            if item in gold:
                correct += 1

        # if not set(predict) == set(gold):
        #     print(gold_filepath)
    print('-----------------------------------focus')
    precision = float(float(correct)/float(all_predict))
    recall = float(float(correct)/float(all_gold))
    F_value = float(precision*recall*2.0)/(precision+recall)

    print(str(correct)+'\t'+str(all_predict)+'\t'+str(all_gold))
    print(precision)
    print(recall)
    print(F_value)

    return correct, all_predict, all_gold



def get_metastatic_result():
    gold_path = './data/EMR_info/METASTATIC'
    predict_path = './data/METASTATIC_SITE'
    metastatic_withlocation = './data/METASTATIC_withlocation'
    metacompletion_withlocation = './data/META_COMPLETATION_withlocation'

    if not os.path.exists(gold_path):
        print('缺少转移部位标注数据')
        sys.exit()

    if not os.path.exists(predict_path):
        print('缺少转移部位预测数据')
        sys.exit()

    gold_filenames = os.listdir(gold_path)

    all_predict = 0
    correct = 0
    all_gold = 0


    for gf in gold_filenames:
        gold_filepath = os.path.join(gold_path,gf)
        predict_filepath = os.path.join(predict_path,gf)
        medium_path = os.path.join(metastatic_withlocation,gf)
        metacompletion_path = os.path.join(metacompletion_withlocation,gf)

        gold_tumer = []
        predict_tumer = []
        gold = []
        predict = []
        
        with open(gold_filepath,'r',encoding='utf-8') as gf:
            gold_tumer = gf.readlines()
        gf.close

        for line in gold_tumer:
            line = line.replace('\n','')
            line = line.strip()
            if ',' in line:
                splits = line.split(',')
                for s in splits:
                    if len(s) == 0:
                        splits.remove(s)
                gold.extend(splits)
            else:
                gold.append(line)

        with open(predict_filepath,'r',encoding='utf-8') as pf:
            predict_tumer = pf.readlines()
        pf.close

        for line in predict_tumer:
            line = line.replace('\n','')
            line = line.strip()
            predict.append(line)

        medium_predict = set(predict)
        predict = list(medium_predict)

        all_predict += len(predict)
        all_gold += len(gold)

        for item in predict:
            if item in gold:
                correct += 1

        if not set(predict) == set(gold):
            # print(gold_filepath)

            medium_result = []
            meta_completation_result = []
            with open(medium_path,'r',encoding='utf-8') as fmp:
                medium_result = fmp.readlines()
            
            with open(metacompletion_path,'r',encoding='utf-8') as fmp:
                meta_completation_result = fmp.readlines()
            '''
            print('---------------------------------------metastaticwithlocation')
            for mr in medium_result:
                mr = mr.replace('\n','')
                print(mr)

            print('---------------------------------------metastaticcompletationwithlocation')
            for mr in meta_completation_result:
                mr = mr.replace('\n','')
                print(mr)

            print('---------------------------------------predict')
            for p in set(predict):
                if not p in set(gold):
                    print(p)
                # print('\n')
            print('---------------------------------------gold')
            for p in set(gold):
                if not p in set(predict):
                    print(p)
                # print('\n')
            '''
    print('-----------------------------------metastatic')
    # correct = 605
    # all_predict = 699
    # all_gold = 701
    precision = float(float(correct)/float(all_predict))
    recall = float(float(correct)/float(all_gold))
    F_value = float(precision*recall*2.0)/(precision+recall)

    print(str(correct)+'\t'+str(all_predict)+'\t'+str(all_gold))
    print(precision)
    print(recall)
    print(F_value)

    return correct, all_predict, all_gold


if __name__=='__main__':

    c1, p1, g1 = get_tumer_result()
    c2, p2, g2 = get_focus_result()
    c3, p3, g3 = get_metastatic_result()

    correct = c1+c2+c3
    all_predict = p1+p2+p3
    all_gold = g1+g2+g3

    print('-----------------------------------total_average_weight')
    precision = float(float(correct)/float(all_predict))
    recall = float(float(correct)/float(all_gold))
    F_value = float(precision*recall*2.0)/(precision+recall)

    print(str(correct)+'\t'+str(all_predict)+'\t'+str(all_gold))
    print(precision)
    print(recall)
    print(F_value)

    correct1 = c1*0.2+c2*0.3+c3*0.5
    all_predict1 = p1*0.2+p2*0.3+p3*0.5
    all_gold1 = g1*0.2+g2*0.3+g3*0.5
    
    print('-----------------------------------total_weighted_weight')
    precision = float(float(correct1)/float(all_predict1))
    recall = float(float(correct1)/float(all_gold1))
    F_value = float(precision*recall*2.0)/(precision+recall)

    print(str(correct)+'\t'+str(all_predict)+'\t'+str(all_gold))
    print(precision)
    print(recall)
    print(F_value)
