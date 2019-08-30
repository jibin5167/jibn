#coding:utf-8
import tensorflow as tf
import numpy as np
import os, argparse, re, shutil
from LSTM_for_metastatic.model import BiLSTM_CRF
from LSTM_for_metastatic.utils import str2bool, get_logger, get_entity, get_BODY_entity, post_process_metastatic, remove_number, pattern_completion
from LSTM_for_metastatic.data import read_corpus, read_dictionary, tag2label, random_embedding, read_testdata, output_data

os.environ['CUDA_VISIBLE_DEVICES'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1,2'  
config = tf.ConfigProto()
config.gpu_options.allow_growth = True

parser = argparse.ArgumentParser(description='BiLSTM-CRF for Chinese NER task')
parser.add_argument('--train_data', type=str, default='./LSTM_for_metastatic/data_path', help='train data source')
parser.add_argument('--test_data', type=str, default='./LSTM_for_metastatic/data_path', help='test data source')
parser.add_argument('--data_source', type=str, default='./data/transfer_sentence', help='test data file')
parser.add_argument('--output_data', type=str, default='./data/METASTATIC_SITE', help='test data file')
parser.add_argument('--batch_size', type=int, default=100, help='#sample of each minibatch')
parser.add_argument('--epoch', type=int, default=50, help='#epoch of training')
parser.add_argument('--hidden_dim', type=int, default=300, help='#dim of hidden state')
parser.add_argument('--optimizer', type=str, default='Adam', help='Adam/Adadelta/Adagrad/RMSProp/Momentum/SGD')
parser.add_argument('--CRF', type=str2bool, default=True, help='use CRF at the top layer. if False, use Softmax')
parser.add_argument('--lr', type=float, default=0.001, help='learning rate') 
parser.add_argument('--clip', type=float, default=5.0, help='gradient clipping')
parser.add_argument('--update_embedding', type=str2bool, default=True, help='update embedding during training')
parser.add_argument('--dropout', type=float, default=0.5, help='dropout keep_prob')
parser.add_argument('--embedding_dim', type=int, default=300, help='random init char embedding_dim')
parser.add_argument('--shuffle', type=str2bool, default=True, help='shuffle training data before each epoch')
parser.add_argument('--demo_model', type=str, default='temp', help='model for test and demo')
parser.add_argument('--mode', type=str, default='demo', help='train/test/demo')
args = parser.parse_args()

word2id = read_dictionary(os.path.join('.', args.train_data, 'word2id.pkl'))
embeddings = random_embedding(word2id, args.embedding_dim)

paths = {}
timestamp = args.demo_model 
output_path = os.path.join('.', args.train_data+"_save", timestamp)
if not os.path.exists(output_path): os.makedirs(output_path)
summary_path = os.path.join(output_path, "summaries")
paths['summary_path'] = summary_path
if not os.path.exists(summary_path): os.makedirs(summary_path)
model_path = os.path.join(output_path, "checkpoints/")
if not os.path.exists(model_path): os.makedirs(model_path)
ckpt_prefix = os.path.join(model_path, "model")
paths['model_path'] = ckpt_prefix
result_path = os.path.join(output_path, "results")
paths['result_path'] = result_path
if not os.path.exists(result_path): os.makedirs(result_path)
log_path = os.path.join(result_path, "log.txt")
paths['log_path'] = log_path
get_logger(log_path).info(str(args))

## read corpus and get training data
if args.mode != 'demo':
    train_path = os.path.join('.', args.train_data, 'train_data')
    test_path = os.path.join('.', args.test_data, 'test_data')
    train_data = read_corpus(train_path)
    test_data = read_corpus(test_path)
    test_size = len(test_data)

if args.mode == 'train':
    model = BiLSTM_CRF(args, embeddings, tag2label, word2id, paths, config=config)
    model.build_graph()

    ## train model on the whole training data
    print("train data: {}".format(len(train_data)))
    model.train(train=train_data, dev=test_data)  # use test_data as the dev_data to see overfitting phenomena

elif args.mode == 'demo':
    ckpt_file = tf.train.latest_checkpoint(model_path)
    #print(ckpt_file)
    paths['model_path'] = ckpt_file
    model = BiLSTM_CRF(args, embeddings, tag2label, word2id, paths, config=config)
    model.build_graph()
    saver = tf.train.Saver()
    with tf.Session(config=config) as sess:
        saver.restore(sess, ckpt_file)
        filenames = os.listdir(args.data_source)
        
        if os.path.exists(args.output_data):
            shutil.rmtree(args.output_data,True)
        os.mkdir(args.output_data)

        medium_path = './data/METASTATIC_withlocation'
        if os.path.exists(medium_path):
            shutil.rmtree(medium_path)
        os.mkdir(medium_path)
        
        m_path = './data/META_COMPLETATION_withlocation'
        if os.path.exists(m_path):
            shutil.rmtree(m_path)
        os.mkdir(m_path)
        
        for ft in filenames:

            seq = re.search('\d\d?\d?',ft).group(0)
            f1 = 'metastatic-'+seq+'.txt'

            testdata_path = os.path.join(args.data_source, ft)
            output_path = os.path.join(args.output_data, f1)
            medium_paths = os.path.join(medium_path,f1)
            m_paths = os.path.join(m_path,f1)
            
            data = '考虑转移'+read_testdata(testdata_path)

            if len(data)>0:
                demo_sent = data
                demo_sent = list(demo_sent.strip())
                demo_data = [(demo_sent, ['O'] * len(demo_sent))]
                tag = model.demo_one(sess, demo_data)
                BODY = get_BODY_entity(tag, demo_sent)
                if len(BODY)>0:
                    post_body = post_process_metastatic(BODY)
                    output_data(post_body,medium_paths)

                    # if seq=='72':
                    #     for i in range(len(post_body)):
                    #         print(post_body[i])

                    
                    post_body1 = pattern_completion(post_body,seq)
                    post_body2 = remove_number(post_body1,data)

                    output_data(post_body1,m_paths)
                    output_data(post_body2,output_path)

                else:
                    output_data(None,output_path)
                    output_data(None,medium_paths)
                    output_data(None,m_paths)
            else:
                # print(ft)
                output_data(None,output_path)
                output_data(None,medium_paths)
                output_data(None,m_paths)
