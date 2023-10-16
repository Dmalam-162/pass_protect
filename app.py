from flask import Flask,render_template,Response,request,redirect,url_for,flash,session
from flask.sessions import SecureCookieSessionInterface
import hashlib
import pyodbc
import pyperclip
from pass_check import *
from pass_vault import vault,delete_rec,update_rec,view
from users import users_table
from pass_generate import *
from strength_check import pass_strength,crack_time


app = Flask(__name__)

app.config['SECRET_KEY'] = 'this-is-a-secret-key'
app.config['SESSION_COOKIE_SECURE'] = True

@app.route('/')
def hello_world():
    return render_template('index.html')



@app.route('/passwordGenerator')
def generate():
    return render_template('generator.html')

@app.route('/passwordGenerator/generate',methods=['GET','POST'])
def generated():
    
    if request.method=='POST':
        num = request.form['num']
        strength =  request.form.get('strength')
        
    output= generate_password(num,strength)
    
    return render_template("generated_pass.html",output=output,copy='copy to clipboard')

@app.route('/copy-to-clipboard', methods=['POST'])
def copy_to_clipboard():
    
    if request.method=='POST':
        
        text = request.form['pass']
        if text:
            pyperclip.copy(text)
            
            return  render_template("generated_pass.html",copy='copied !')
        else:
            return f'No text provided.'

@app.route('/strength_checker')
def strength():
    return render_template('strength_check.html')

@app.route('/strength_checker/check', methods=['GET','POST'])
def check_strength():
    if request.method=='POST':
        passwd= request.form['passwd']
        strength= pass_strength(passwd)
        
        if strength=="Strong" :
            cracking_speed = 2000
        elif strength=="Intermediate" :
            cracking_speed = 1296
        elif strength=="Weak" :
          cracking_speed = 2000

        est_time=crack_time(passwd,cracking_speed)

        if strength=='Weak':
            return render_template("weak.html",est_time=est_time,strength=strength)
        elif strength=='Intermediate':
            return render_template("inter.html",est_time=est_time,strength=strength)
        elif strength=='Strong':
            return render_template("strong.html",est_time=est_time,strength=strength)


@app.route('/vault') 
def sign_in():
    return render_template('create.html')

@app.route('/login') 
def log_in():
    return render_template('login.html')

@app.route('/loggedin', methods=['GET','POST']) 
def logged_in():
    if request.method=='POST':
        user_name = request.form['user_name']
        user_pwd = request.form['user_pwd']

       
        conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\diyam\python\pass_protect\pass_db.accdb;")
        cursor = conn.cursor() 
        hash_pwd=hashlib.md5(user_pwd.encode('utf-8')).hexdigest().upper()

        try:

            cursor.execute(f"SELECT * FROM USERS WHERE User_name=? and Password=?;", (user_name, hash_pwd))   
            rows = cursor.fetchall() 
            conn.commit()
            
            if(rows):
              
               session['username']=user_name
               return render_template('vault_layout.html',user=user_name)
            else:
                 return render_template('unauthorized.html')

        except:
               return render_template('unauthorized.html')
        
@app.route('/loggedin/<user>', methods=['GET','POST']) 
def logged_in_user(user):
     user_nm=str(user)
     return render_template('vault_layout.html',user=user_nm)

@app.route('/vault/create', methods=['GET','POST'])
def signed_in():
    if request.method=='POST':
        user_name = request.form['user_name']
        user_email = request.form['user_email']
        user_pwd = request.form['user_pwd']
        con_pwd= request.form['con_pwd']
        session['username']=user_name
        if con_pwd==user_pwd:
         
         return users_table(user_name,user_email,user_pwd)
        
@app.route('/vault/view/<user>', methods=['GET','POST']) 
def vault_view(user):
     table=str(user)
     return view(table)

@app.route('/vault/save/<user>', methods=['GET','POST']) 
def vault_manage(user):
  
    if request.method=='POST':
        pwd = request.form['pwd']
        usr = request.form['usr']
        web = request.form['web']
        table=str(user)
        
        return vault(web,usr,pwd,table)
    
@app.route('/delete/<user>/<int:id>')
def delete(id,user):
    table=str(user)
    return delete_rec(id=id,user=table)

@app.route('/update/<user>/<int:id>', methods=['GET','POST'])
def update(id,user):
    table=str(user)
    
    return render_template('update.html',user=table,id=id)

@app.route('/vault/save/<user>/<int:id>/update', methods=['GET','POST'])
def updated(id,user):
    table=str(user)
    if request.method=='POST':
        pwd = request.form['pwd']
        usr = request.form['usr']
        web = request.form['web']

        return update_rec(id=id,user=table,pwd=pwd,usr=usr,web=web)
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')
   

@app.route('/pwned')
def pwned():
    return render_template('pwned.html')

@app.route('/pwned/check', methods=['GET','POST']) 
def checking():
     if request.method=='POST':
        pwd = request.form['passwd']
     
     return main(f'{pwd}')



@app.route('/learn')
def learn():
    return render_template('learn_more.html')

if __name__ == '__main__':
    app.run()
