from flask import Flask,render_template,redirect,url_for,send_file,flash
from flask_session import Session
import mysql.connector

mydb=mysql.connector.connect(host='localhost',user='root',password='admin',db='rapido',auth_plugin='mysql_native_password')
app=Flask(__name__)
app.secret_key='dinesh123'
@app.route('/')
def dashboard():
    cursor=mydb.cursor()
    cursor.execute('delete from submissions where created_at < DATE_SUB(NOW(), INTERVAL 2 HOUR)')
    mydb.commit()
    # cursor.execute('SELECT * FROM submissions WHERE created_at > DATE_SUB(NOW(), INTERVAL 2 HOUR) order by created_at desc')
    cursor.execute('SELECT center_name,area,DATE_FORMAT(created_at, "%H:%i") AS time_only FROM submissions;')
    data=cursor.fetchall()
    return render_template('dashboard.html',data=data)

@app.route('/areas')
def areas():
    cursor=mydb.cursor()
    cursor.execute('select distinct area from centers order by area')
    centers=cursor.fetchall()
    return render_template('areas.html',centers=centers)

@app.route('/centers/<area>')
def centers(area):
    cursor=mydb.cursor()
    cursor.execute('select center_name,area from centers where area=%s order by center_id',[area])
    center_names=cursor.fetchall()
    print(center_names)
    return render_template('centers.html',center_names=center_names)

@app.route('/active/<center_name>')
def active(center_name):
    cursor=mydb.cursor()
    cursor.execute('select count(center_name) from submissions where center_name=%s',[center_name])
    count=cursor.fetchone()
    print(f'{count=}')
    if count[0]==0:
        cursor=mydb.cursor()
        cursor.execute('select area from centers where center_name=%s',[center_name])
        area=cursor.fetchone()
        print(f'executed this code {area=}')
        cursor.execute('insert into submissions(center_name,area) values(%s,%s)',[center_name,area[0]])
        mydb.commit()
        cursor.close()
        flash(f'{center_name} added successfully')
        return redirect(url_for('dashboard'))
    else:
        flash(f'{center_name} already exists')
        return redirect(url_for('dashboard'))
# @app.route('/active/<center_name><area_name>')
# def active(center_name,area_name):
#     cursor=mydb.cursor()
#     cursor.execute('select count(center_name) from submissions')
#     count_s=cursor.fetchone()
#     if count_s[0]==0:
#         cursor.execute('insert into submissions(center_name,area) values(%s,%s)',[center_name,area_name])
#         mydb.commit()
#         return render_template('dashboard.html')
#     elif count_s[0]==1:
#         return render_template('dashboard.html')
#     cursor.execute('select * from submissions')
#     data=cursor.fetchall()
#     return render_template('activeareas.html',data=data)

@app.route('/notactive/<center_name>')
def notactive(center_name):
    cursor=mydb.cursor()
    cursor.execute('delete from submissions where center_name=%s',[center_name])
    return redirect(url_for('dashboard'))

@app.route('/admin')
def admin():
    cursor=mydb.cursor()
    cursor.execute('select * from centers')
    center_data=cursor.fetchall()
    return render_template('admin.html',center_data=center_data)


app.run(use_reloader=True,debug=True)