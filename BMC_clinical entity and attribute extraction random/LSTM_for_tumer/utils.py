import logging, sys, argparse, re


def str2bool(v):
    # copy from StackOverflow
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')
        
def get_tumer_surgery_sentence(medical_record):
    medical_record = re.sub('。', ',', medical_record)
    medical_record = re.sub('\d\.', ',', medical_record)
    medical_record = re.sub(';', ',', medical_record)
    medical_record = re.sub('；', ',', medical_record)
    choosed = medical_record.split(',')
    tumer_surgery_sentence = []
    
    for ch in choosed:
        if '恶性肿瘤' in ch and '考虑' not in ch:
            tumer_surgery_sentence.append(ch)
        elif '乳术后' in ch:
            i = ch.index('乳术后')
            ch = ch[i-1:i+3]
            tumer_surgery_sentence.append(ch)
    return tumer_surgery_sentence

def get_tumer_zhanwei_sentence(medical_record):
    medical_record = re.sub('。', ',', medical_record)
    medical_record = re.sub('\d\.', ',', medical_record)
    medical_record = re.sub(';', ',', medical_record)
    medical_record = re.sub('；', ',', medical_record)
    choosed = medical_record.split(',')
    tumer_zhanwei_sentence = []
    
    for ch in choosed:
        if '占位' in ch and '考虑' not in ch:
            tumer_zhanwei_sentence.append(ch)
    return tumer_zhanwei_sentence
    
def post_process_tu_crf(tu_su_site):
    tu_su = tu_su_site.split(' ')
    if len(tu_su)>1:
        tu_su_site = tu_su[1]
    elif len(tu_su)==1:
        tu_su_site = tu_su[0]
    else: tu_su_site = ''
    if len(tu_su_site)>4 and '肺' in tu_su_site and '叶' in tu_su_site:
        tu_su_site = tu_su_site[:4]
    if '门区' in tu_su_site:
        tu_su_site = tu_su_site[:-1]
    return tu_su_site
        
def get_choosen_sentence(sentence):
    choosed = []
    for s in sentence:
        if '结节' in s and 'CT' in s:
            if s not in choosed:
                choosed.append(s)
        elif '密度' in s and 'CT' in s:
            if s not in choosed:
                choosed.append(s)
        elif '团块' in s and 'CT' in s:
            if s not in choosed:
                choosed.append(s)
        elif '肿块' in s and 'CT' in s:
            if s not in choosed:
                choosed.append(s)
        elif '增高' in s and 'CT' in s:
            if s not in choosed:
                choosed.append(s)
        elif '团片' in s and 'CT' in s:
            if s not in choosed:
                choosed.append(s)
        elif '软组织' in s and 'CT' in s:
            if s not in choosed:
                choosed.append(s)
        elif '不规则' in s and '软组织' in s:
            if s not in choosed:
                choosed.append(s)
        elif '软组织' in s and '密度' in s:
            if s not in choosed:
                choosed.append(s)
        elif '肿块' in s and '软组织' in s:
            if s not in choosed:
                choosed.append(s)
        elif '空洞性病变' in s:
            if s not in choosed:
                choosed.append(s)
        elif '结节' in s and '软组织' in s:
            if s not in choosed:
                choosed.append(s)
        elif '肿块' in s and '软组织' in s:
            if s not in choosed:
                choosed.append(s)
        elif '不规则' in s and '密度' in s:
            if s not in choosed:
                choosed.append(s)
    return choosed

def get_reco_sentence(post_choosed):
    reco_sentence = []
    for pch in post_choosed:
        if '团块' in pch:
            if pch not in reco_sentence:
                reco_sentence.append(pch)
        elif '肿块' in pch:
            if pch not in reco_sentence:
                reco_sentence.append(pch)
        elif '肿物' in pch:
            if pch not in reco_sentence:
                reco_sentence.append(pch)
        elif '团片' in pch:
            if pch not in reco_sentence:
                reco_sentence.append(pch)
        elif '软组织' in pch:
            if pch not in reco_sentence:
                reco_sentence.append(pch)
        elif '不规则' in pch and '密度' in pch:
            if pch not in reco_sentence:
                reco_sentence.append(pch)
        elif '不规则' in pch and '结节' in pch:
            if pch not in reco_sentence:
                reco_sentence.append(pch)
        elif '空洞性' in pch:
            if pch not in reco_sentence:
                reco_sentence.append(pch)
#        elif '密度' in pch:
#            if pch not in reco_sentence:
#                reco_sentence.append(pch)
    return reco_sentence

def get_Tumer_entity(tag_seq, char_seq):
    length = len(char_seq)
    TUMER = []
    for i, (char, tag) in enumerate(zip(char_seq, tag_seq)):
        if tag == 'B-TU':
            if 'tumer' in locals().keys():
                TUMER.append(tumer)
                del tumer
            tumer = str(i) + ' ' + char
            if i+1 == length:
                TUMER.append(tumer)
#            print(tumer)
        if tag == 'I-TU':
            if 'tumer' in locals().keys():
                tumer += char
            else: tumer = char
            
            if i+1 == length:
                TUMER.append(tumer)
        if tag not in ['I-TU', 'B-TU']:
            if 'tumer' in locals().keys():
                TUMER.append(tumer)
                del tumer
            continue
    return TUMER

def postprocess_tumerlist(TUMER):
    TUMER_post = []
    for tumer in TUMER:
        if len(tumer)>0:
            tumer_split = tumer.split(' ')
            if len(tumer_split)>1:
                TUMER_post.append(tumer_split[1])
            else:
                TUMER_post.append(tumer_split[0])
                
    tumer_set = set(TUMER_post)
    tumer_list = list(tumer_set)
    return tumer_list
    

def postprocess_tumerlist1(TUMER):
    TUMER_post = []
    if len(TUMER)==1:
        if len(TUMER[0].split(' '))==2:
            s = TUMER[0].split(' ')[1].strip()
            if s.endswith('叶肺癌')==0:
                s = s[:-1]
                TUMER_post.append(s)
            else:
                s = s[:-2]
                TUMER_post.append(s)
        else:
            s = TUMER[0].strip()
            if s.endswith('叶肺癌')==0:
                s = s[:-1]
                TUMER_post.append(s)
            else:
                s = s[:-2]
                TUMER_post.append(s)
        tumer_temp = set(TUMER_post)
        TUMER_post = list(tumer_temp)
    else: 
        for tumer in TUMER:
            if len(tumer.split(' '))==2:
                s = tumer.split(' ')[1].strip()
                if s.endswith('叶肺癌')==0:
                    s = s[:-1]
                    TUMER_post.append(s)
                else:
                    s = s[:-2]
                    TUMER_post.append(s)
            else:
                s = tumer.strip()
                if s.endswith('叶肺癌')==0:
                    s = s[:-1]
                    TUMER_post.append(s)
                else:
                    s = s[:-2]
                    TUMER_post.append(s)
        tumer_temp = set(TUMER_post)
        TUMER_post = list(tumer_temp)
    return TUMER_post

def get_logger(filename):
    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)
    handler = logging.FileHandler(filename)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s: %(message)s'))
    logging.getLogger().addHandler(handler)
    return logger
