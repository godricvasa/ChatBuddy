import mysql.connector
from mysql.connector import errorcode


def add_user(cnx,username,password):
  insert_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
#   print(cnx)
  cursor = cnx.cursor()
  cursor.execute("use projectDB")
  #add new users
  cursor.execute(insert_query,(username,password))
  cnx.commit()
  print("done")
#   print(res);

def checkUser(cnx,username,password):
  select_query = "select id,username,password from  users where username=%s and password=%s"
#   print(cnx)
  cursor = cnx.cursor()
  cursor.execute("use projectDB")
  #add new users
  cursor.execute(select_query,(username,password))
  res = cursor.fetchall()
#   cnx.commit()
  print(f"{res[0]}")

def connector(route,username,password):
    try:
      cnx = mysql.connector.connect(host="localhost",
      user="root",password="1234",database="projectDB")
      #based on route - reg / -log 
      #check from which the request came from
      if(route=="register"):
       add_user(cnx,username,password)
      else: 
        checkUser(cnx,username,password) 

    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
      else:
        print(err)
    else:
      cnx.close()
    #   return "user added successfully"




   

