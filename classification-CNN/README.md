# Text Classification with CNN and RNN

使用卷积神经网络进行中文文本分类

字符级CNN的论文：[Character-level Convolutional Networks for Text Classification](https://arxiv.org/abs/1509.01626)

基于TensorFlow在中文数据集上的简化实现，使用了字符级CNN对中文文本进行分类。


## 环境

- Python 2/3 
- TensorFlow 1.3以上
- numpy
- scikit-learn
- scipy

## 数据集


类别如下：

```
体育, 财经, 房产, 家居, 教育, 科技, 时尚, 时政, 游戏, 娱乐
类别自己定义，如软件测试中可自己定义：“串口”，“并口”等等类别
在代码中的修改有一下2处：
1 cnews_loader.py的read_category()函数中的categories = ['体育', '财经', '房产', '家居', '教育', '科技', '时尚', '时政', '游戏', '娱乐']，列表中的按照实际需要定义，多少个都可以。
2 cnn_model.py的TCNNConfig(object)函数中的num_classes = 10，设置为实际定义的类别数。
```

- train.txt: 训练集
- val.txt: 验证集
- test.txt: 测试集

train.txt和val.txt格式一致，都是经过标注的数据；test.txt数据无标注数据。
在data文件夹下面给了这三个数据集的例子，具体可以参考下。


## CNN卷积神经网络

### 配置项

CNN可配置的参数如下所示，在`cnn_model.py`中。

```
    """CNN配置参数"""

    embedding_dim = 64      # 词向量维度
    seq_length = 600        # 序列长度
	
    num_classes = 10        # 类别数
	
    num_filters = 128       # 卷积核数目
    kernel_size = 5         # 卷积核尺寸
    vocab_size = 5000       # 词汇表达小
    hidden_dim = 128        # 全连接层神经元
	
    dropout_keep_prob = 0.5 # dropout保留比例
	
    learning_rate = 1e-3    # 学习率
    batch_size = 64         # 每批训练大小
	
    num_epochs = 10         # 总迭代轮次
	
    print_per_batch = 100    # 每多少轮输出一次结果
    save_per_batch = 10      # 每多少轮存入tensorboard
```
工程应用中需要自己调整的超参数共有三个，num_classes，drop_keep_prob和num_epochs。
num_classes：这个超参数就是上面自己定义的分类类别数
drop_keep_prob：这个超参数取值在(0,1)之间，一般在使用中会进一步缩小到(0.3,0.7)之间。这个参数就是试出来的，暂时还没有经验可循。
num_epochs：这个超参数制定的是CNN模型的训练次数，由于在CNN模型中使用了early stopping策略（即当模型训练到一定程度时会自动停止，可能是局部最优也可能是全局最优），因此这个参数设置的大点就好了，10000以上吧。

### CNN模型

具体参看`cnn_model.py`的实现。

### 训练与验证

运行 `python run_cnn.py train`，可以开始训练。
执行上述指令就是用使用训练数据训练CNN模型，训练过程中可以使用验证数据来观察模型训练的好坏



### 测试

运行 `python run_cnn.py test` 在测试集上进行测试。
执行上述指令是用测试集数据来验证一下模型的好坏，这一步可有可无，没多大意义，真正在工程应用中使用该模型的借口不在这个地方，是下面介绍的predict.py文件。


### 工程中应用上述训练好的模型
运行 `python preidict.py` 来预测文本的类别。
其中，要修改一下待预测文本的输入方式。
'''
if __name__ == '__main__':
    cnn_model = CnnModel()
    test_demo = '三星ST550以全新的拍摄方式超越了以往任何一款数码相机'          #将此处修改为自己要预测的文本，有很多文本时，写个for循环就可以了，让文本一个个的输入进行分类
    print(cnn_model.predict(test_demo))       #cnn_model.predict(test_demo)：此函数的输出是CNN模型预测的test_demo这个文本的类别
'''



### Python处理excel文件（.xlsx格式，不确定.xls格式是否可用，没用过）

举个例子吧，我现在正在用的：


import xlrd     #xlrd在tensorflow库中应该是自带的，如果不是自带的就自己安装一个

def fileload(filepath):     #filepath是路径，相对路径或绝对路径都可以
    
	EMR = []   #我定义的列表
    tumer = []  #我定义的列表
    focus = []  #我定义的列表
    metastatic = []  #我定义的列表

    workbook = xlrd.open_workbook(filepath)
    table = workbook.sheets()[0]    #这两行代码就完成了excel表格的读取。[0]这个参数是指表格中的第一个sheet，如果想读取其它的sheet，改一下参数就OK了

    for row in range(table.nrows):     #for循环一行行的读取表格内容
        EMR.append(table.row_values(row)[0])   #[0]表示是excel表格的第一列
        tumer.append(table.row_values(row)[1])  #[1]表示是excel表格的第二列
        focus.append(table.row_values(row)[2])   #[2]表示是excel表格的第三列
        metastatic.append(table.row_values(row)[3])  #[3]表示是excel表格的第四列
    
    return  EMR, tumer, focus, metastatic

