import xlrd, os, shutil


def fileload(filename):
    EMR = []
    tumer = []
    focus = []
    metastatic = []

    workbook = xlrd.open_workbook(filename)
    table = workbook.sheets()[0]

    for row in range(table.nrows):
        EMR.append(table.row_values(row)[0])
        tumer.append(table.row_values(row)[1])
        focus.append(table.row_values(row)[2])
        metastatic.append(table.row_values(row)[3])
    
    return  EMR, tumer, focus, metastatic


def writeData(Excelpath):
    
    EMR, tumer, focus, metastatic = fileload(Excelpath)

    path = os.path.join('.','data/EMR_info')

    if os.path.exists(path):
        shutil.rmtree(path,True)

    os.mkdir(path)

    for i in range(1,len(EMR)):

        EMR_path = os.path.join(path,'EMR')
        tumer_path = os.path.join(path,'TUMER')
        focus_path = os.path.join(path,'FOCUS')
        metastatic_path = os.path.join(path,'METASTATIC')
        
        if not os.path.exists(EMR_path):
            os.mkdir(EMR_path)  
        if not os.path.exists(tumer_path):
            os.mkdir(tumer_path)  
        if not os.path.exists(focus_path):
            os.mkdir(focus_path)  
        if not os.path.exists(metastatic_path):
            os.mkdir(metastatic_path)  

        EMR_path = os.path.join(EMR_path,'record-'+str(i)+'.txt')
        tumer_path = os.path.join(tumer_path,'tumer-'+str(i)+'.txt')
        focus_path = os.path.join(focus_path,'focus-'+str(i)+'.txt')
        metastatic_path = os.path.join(metastatic_path,'metastatic-'+str(i)+'.txt')

        with open(EMR_path, 'w+', encoding='utf-8') as f1:
            f1.write(EMR[i])
            f1.writelines

        with open(tumer_path, 'w+', encoding='utf-8') as f1:
            f1.write(tumer[i])
            f1.writelines

        with open(focus_path, 'w+', encoding='utf-8') as f1:
            f1.write(focus[i])
            f1.writelines

        with open(metastatic_path, 'w+', encoding='utf-8') as f1:
            f1.write(metastatic[i])
            f1.writelines
