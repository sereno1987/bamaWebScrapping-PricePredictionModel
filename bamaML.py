import re
import requests
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import errorcode


# --------------------------------------------load first page---------------------------------
base_url="https://bama.ir/car/all-brands/all-models/all-trims?page="

# --------------------------------------------variables-----------------------------------------
l = []

# --------------------------------------------scrapping-----------------------------------------

for page in range(1, 1*10, 10):

    # load a webpage
    r = requests.get ( base_url + str ( page ))
    c = r.content
    soup=BeautifulSoup(c , "html.parser")
    details = soup.find_all("div", {"class": "listdata"})
    for detail in details:
        car = {}
        car["name"] = detail.find("h2").text.replace("\r\n", "").replace(" ", "")
        car["year"] = detail.find("span",{"class":"year-label"}).text.replace("\r\n", "").replace(" ", "")
        car["km"] = detail.find("p", {"class": "price"}).text.replace("\n\r", "").replace(" ", "")
        if car["km"]=="کارکردصفر":
            car["km"]=" کارکرد0"
        if car["km"] =="-" or car["km"]=="کارتکس":
            continue
        car["price"] = detail.find("p", {"class": "cost"}).text.replace("\n\r", "").replace(" ", "")
        if car["price"]== "توافقی" or car["price"]=="درتوضیحات" or "پیش" in car["price"] or car["price"]=="حواله":
            continue
        l.append(car)


# --------------------------------------------insert to db----------------------------------------

try:
  cnx = mysql.connector.connect(user='root',
                                password='root',
                                host='127.0.0.1',
                                database='bama')
  cursor = cnx.cursor()
  compare_list=[]
  for i in range(len(l)):
      car_name = l[i]['name']
      year = l[i]['year'].replace("،", "")
      km = int((l[i]['km']).replace(",", "").replace("کارکرد", "").replace("کارتکس", ""))
      # km=km.lstrip((re.split('(\d+)',km))[0])
      # km=locale.atoi(km)
      price = (l[i]['price']).replace(",", "").replace("تومان", "")
      # compare_list.append(car_name,price,km,year)
      # print(compare_list)

      cursor.execute("INSERT INTO car (name,year, price, km) VALUES('%s','%s','%s','%i')" % (car_name, year, price, km))
      cnx.commit()
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
    cnx.close()


