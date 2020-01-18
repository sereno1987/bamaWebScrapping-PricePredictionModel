import mysql.connector
import numpy as np
from mysql.connector import errorcode
from sklearn import tree
from sklearn import preprocessing
x=[]
y=[]

try:
    cnx = mysql.connector.connect(user='root',
                                  password='root',
                                  host='127.0.0.1',
                                  database='bama')
    cursor = cnx.cursor()
    cursor.execute("SELECT * From car")
    result = cursor.fetchall()
    le = preprocessing.LabelEncoder()
    # ------------------------------------------------------normalize

    x1=[]
    for item in result:
        x1.append(str(item[0]))
    le.fit(x1)
    z = le.transform(x1)
    # print(z)
    reversed=le.inverse_transform(z)



    # -------------------------------------------------------------
    name=[]
    i=0
    for item in result:
        x4=[]

        x4.append(z[i])
        x4.append(item[2])
        x4.append(item[3])
        x.append(x4)
        y.append(item[1])
        i+=1

    clf=tree.DecisionTreeClassifier()
    clf=clf.fit(x,y)
    new_data=[['پژو،206،تیپ5', 0, "1398"]]
    if new_data[0][0] in reversed:
        result = np.where(reversed == new_data[0][0])
        new_data=[[z[result[0][0]],new_data[0][1],new_data[0][2]]]
    answer=clf.predict(new_data)
    print(answer)
    # else:
    #     print("there is no data available for this car")


except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
    cnx.close()