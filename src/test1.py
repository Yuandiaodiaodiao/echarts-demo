import sqlite3

import csv
import os

def readfile():
    for root,_,file in os.walk('../menus'):
        return file

def solveshop(filelist):
    for filename in filelist:
        with open('../menus/'+filename,'r',encoding='utf-8-sig')as f:
            csvr = csv.reader(f)
            indexlist = []
            conn = sqlite3.connect('Z:/dataset.db')
            c = conn.cursor()
            for index, row in enumerate(csvr):
                if index == 0:
                    indexlist = row
                    print('index' + str(row))
                else:
                    try:
                        c.execute(
                            f"""INSERT INTO shop (ID,name,address,description,latitude,longitude,phone,promotion_info) 
                             VALUES ({row[0]},'{row[1]}','{row[2]}' , '{row[3]}', {row[4]},{row[5]},'{row[6]}' , '{row[
                                7]}' )""");
                    except:
                        pass
                    else:
                        conn.commit()
            conn.close()
def solvefood(filelist):
    shops=0
    foods=0
    categorys=0
    nums=0
    filelist.sort(key=lambda x:0-len(x))
    for filename in filelist:
        with open('../menus/'+filename,'r',encoding='utf-8-sig')as f:
            csvr = csv.reader((line.replace('\0','') for line in f))
            indexlist = []
            conn = sqlite3.connect('Z:/dataset.db',isolation_level=None)
            c = conn.cursor()
            shopid=None
            categoryid=None
            for index, row in enumerate(csvr):
                # if index >= 10:
                #     c.execute("COMMIT")
                #     return
                if nums%10000==0:
                    try:
                        c.execute("COMMIT")
                    except:
                        pass
                    c.execute("BEGIN TRANSACTION")
                    print(f'成功添加店铺{shops}  食品{foods}  分类{categorys}')
                nums+=1
                # if shops%1000==0 or foods%1000==0 or categorys%1000==0:


                if index == 0:
                    indexlist = row
                    # print('index' + str(row))
                else:
                    """
                    空值替换NULL
                    """
                    for index_row,item in enumerate(row):
                        if len(item)==0:
                            row[index_row]='NULL'
                    # food表
                    try:
                        if "categoryId" in indexlist:
                            strs=f"""{row[0]},{row[11]},'{row[12]}' , {row[13]} , {row[14]} , {row[15]} , {row[16]} , {row[17]} , {row[18]} , {row[19]} , {row[8]} """
                            c.execute(
                            f"""INSERT INTO food (ID,foodId,foodName,price,rating,monthSales,ratingCount,statisfyCount,statisfyRate,minPurchase,categoryId) 
                             VALUES ({strs})""")
                        else:
                            c.execute(
                            f"""INSERT INTO food (ID,foodId,foodName,price,rating,monthSales,ratingCount,statisfyCount,statisfyRate,minPurchase,categoryId) 
                             VALUES ({row[0]},{row[8]},'{row[9]}' , {row[10]}, {row[11]},{row[12]},{row[13]},{row[14]},{row[15]} ,{row[16]} ,NULL  )""")
                    except:
                        pass
                    else:
                        foods+=1
                    #shop表
                    if row[0] != shopid:
                        shopid = row[0]
                        try:

                                c.execute(
                                    f"""INSERT INTO shop (ID,name,address,description,latitude,longitude,phone,promotion_info) 
                                     VALUES ({row[0]},'{row[1]}','{row[2]}' , '{row[3]}', {row[4]},{row[5]},'{row[6]}' , '{row[
                                        7]}' )""");
                        except:
                            pass
                        else:
                            shops+=1
                    #分类表
                    if "categoryId" in indexlist:
                        if categoryid!=row[8]:
                            categoryid=row[8]
                            try:
                                c.execute(
                                    f"""INSERT INTO category (categoryId,categoryName,categoryDescription)
                                     VALUES ({row[8]},'{row[9]}','{row[10]}')""");
                            except:
                                pass
                            else:
                                categorys+=1
            try:
                c.execute("COMMIT")
            except:
                pass
            conn.close()

if __name__=="__main__":
    filestr=readfile()
    solvefood(filestr)


