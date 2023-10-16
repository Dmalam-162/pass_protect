import pyodbc
from flask import render_template


def vault(web_site,usr_nm,user_pass,table_nm):
    
    conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\diyam\python\pass_protect\pass_db.accdb;")
  
     
    cursor = conn.cursor() 
    global table
    table=f"{table_nm}"
    var4=f'{web_site}'
    var5=f'{usr_nm}'
    var6=f'{user_pass}'
    
    query = f"INSERT INTO [{table}] (website, username, password) VALUES (?, ?, ?);"

    cursor.execute(query, (var4,var5,var6)) 
    conn.commit() 
    cursor.execute(f"SELECT * FROM {table};")
    
    rows = cursor.fetchall() 
   
    
    return render_template("user_vault.html",dataset=rows,user=table)
   


def view(table):
    conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\diyam\python\pass_protect\pass_db.accdb;")
  
    cursor = conn.cursor() 
    cursor.execute(f"SELECT * FROM {table};")
    rows = cursor.fetchall() 
   
    return render_template("user_vault.html",dataset=rows,user=table)


def delete_rec(id,user):
    conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\diyam\python\pass_protect\pass_db.accdb;")
    cursor = conn.cursor()  
           
    del_query=f"DELETE FROM {user} WHERE ID={id};"
    cursor.execute(del_query);
    conn.commit()
    cursor.execute(f"SELECT * FROM {user};")
    
    row_2 = cursor.fetchall() 

    return render_template("user_vault.html",dataset=row_2,user=user)

    
def update_rec(id,user,pwd,usr,web):
    conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\diyam\python\pass_protect\pass_db.accdb;")
    cursor = conn.cursor()  
           
    cursor.execute(f'UPDATE {user} SET website=?, username=?,password=? WHERE id=?', (web, usr,pwd, id))
    
    conn.commit()
    cursor.execute(f"SELECT * FROM {user};")
    
    row_3 = cursor.fetchall() 

    return render_template("user_vault.html",dataset=row_3,user=user)