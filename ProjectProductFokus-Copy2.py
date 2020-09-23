#!/usr/bin/env python
# coding: utf-8

# In[8]:


import pandas as pd
import numpy as np
import pandasql as ps

targetSales = 5000000
dataCsv = pd.read_excel('cleanData.xlsx')
dataFrame = pd.DataFrame(dataCsv)

usernames = []
index = 1

query = "select DISTINCT AM from  dataFrame;"
dataUser = np.array(ps.sqldf(query)).flatten().tolist()
dataUserTemp = dataUser

print("Berikut merupakan List Nama User : ")
print(dataUser)
print("Masukan User2 yang akan dihitung Incentive Product Fokus : ")

while(1) :
    userinput = input('input username ke {} (kosongkan jika sudah): '.format(index))
    if userinput == '' :
        break;
    if userinput in dataUserTemp:
            usernames.append(userinput)
            dataUserTemp.remove(userinput)
    else : 
        print('Inputan tidak Cocok untuk data Apotek / sudah diinput sebelumnya')
    index = index + 1
    
index = 0
while (index< len(usernames)) : 
    dataFrameAmFilter = dataFrame.copy()
    query = "select * from  dataFrameAmFilter where AM = '{}';".format(usernames[index])
    dataFrameAmFilter = ps.sqldf(query)
    
    dataProductFokus = dataFrameAmFilter.copy()
    query = "select * from  dataFrameAmFilter where NAMAPROD like 'D-VIT%' "
    query = query + "or NAMAPROD like 'CALNIC%'"
    query = query + "or NAMAPROD like 'VOXIN%'"
    query = query + "or NAMAPROD like 'CEFAROX%'"
    query = query + "or NAMAPROD like 'GASTROLAN%'"
    query = query + "or NAMAPROD like 'VOMISTOP%'"
    query = query + "or NAMAPROD like 'ESTIN%'"
    query = query + "or NAMAPROD like 'ZEMINDO%'"
    query = query + "or NAMAPROD like 'BUSMIN%'"
    query = query + "or NAMAPROD like 'HI-SQUA%'"
    dataProductFokus = ps.sqldf(query)
    
    query = "select DISTINCT NAMALANG from  dataProductFokus where \"TYPE OUTLET\" = 'APOTIK' or 'TYPE OUTLET' = 'APOTEK'; "
    dataApotek = np.array(ps.sqldf(query)).flatten().tolist()
    
    print(dataApotek)
    dispenList = []
    while(1):
        userinput = str(input('masukan nama Apotik Langganan yang dispen (biarkan kosong untuk selesai)'))
        if userinput == '' :
            break;
        if userinput in dataApotek:
            dispenList.append(userinput)
            dataApotek.remove(userinput)
        else :
            print('Inputan tidak Cocok untuk data Apotek / sudah diinput sebelumnya')

    listApotekDispen = pd.DataFrame(dispenList, columns = ['dispen'])
    query = "select * from  dataProductFokus where \"NAMALANG\" not in (select dispen from listApotekDispen)"
    filterDataProductFokus = ps.sqldf(query)
    
    query = "select sum(THNA) from  filterDataProductFokus"
    sumSales = np.array(ps.sqldf(query)).flatten().tlist()
   
    if sumSales[0] >= targetSales : 
        query = "select ({} - 5000000) * 7.5/100 as \"Incentive Product Fokus\" from filterDataProductFokus ".format(sumSales[0])
        IPF = np.array(ps.sqldf(query)).flatten().tolist()
        TotalIncentive = IPF[0]
    else :
        TotalIncentive = 0
    
    print("\nTotal IPF yang diterima oleh {} adalah : {} \n".format(usernames[index],TotalIncentive))
  
    index = index + 1

