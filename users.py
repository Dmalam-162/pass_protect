import pyodbc
import hashlib
from flask import render_template

def users_table(name,email,password):
    
     try:
        conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\diyam\python\pass_protect\pass_db.accdb;")
        cursor = conn.cursor() 
        var1=f'{name}'
        var2=f'{email}'
        hash_pwd=hashlib.md5(password.encode('utf-8')).hexdigest().upper()

        create_query= f"""
                        CREATE TABLE {name} (
                        id COUNTER NOT NULL PRIMARY KEY,
                        website varchar(255) NOT NULL,
                        username varchar(255) NOT NULL,
                        password varchar(255) NOT NULL
                        );
                        """
        
        query2 = f"INSERT INTO USERS (User_name, Email, Password) VALUES (?, ?, ?);"
       
        cursor.execute(create_query)
        cursor.execute(query2, (var1,var2,hash_pwd)) 
        conn.commit() 
        conn.close()

        

        return render_template("vault_layout.html",user=var1)
  
     except:
          return f"<center><h1><b>username {name} already taken!!<br>Please choose another username.<h1><center>"

