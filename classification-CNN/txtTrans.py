import xlrd     #xlrd在tensorflow库中应该是自带的，如果不是自带的就自己安装一个

#def fileload(filepath):     #filepath是路径，相对路径或绝对路径都可以

EMR = []   #我定义的列表
    #tumer = []  #我定义的列表
focus = []  #我定义的列表
    #metastatic = []  #我定义的列表
workbook = xlrd.open_workbook('DataEXCEL/test.xlsx')
table = workbook.sheets()[0]    #这两行代码就完成了excel表格的读取。[0]这个>参数是指表格中的第一个sheet，如果想读取其它的sheet，改一下参数就OK了

for row in range(table.nrows):     #for循环一行行的读取表格内容
	EMR.append(table.row_values(row)[0])   #[0]表示是excel表格的第一列
       # tumer.append(table.row_values(row)[1])  #[1]表示是excel表格的第二列
	focus.append(table.row_values(row)[1])   #[2]表示是excel表格的第三列
       # metastatic.append(table.row_values(row)[3])  #[3]表示是excel表格的第四列

  #  return  EMR, focus
for i in range(len(EMR)):
	EMR[i] = EMR[i].replace('\r','').replace('\n','').replace('\t','')
	focus[i] = focus[i].replace('\r','').replace('\n','').replace('\t','')
#print(focus[400])
with open('data/test.txt','w') as f:    #设置文件对象
	for i in range(len(EMR)):
		f.write(focus[i]+'\t'+EMR[i]) 
		f.write()
