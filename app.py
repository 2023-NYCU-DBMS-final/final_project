from flask import Flask, render_template, request, redirect, url_for, make_response
import base64
import users   #users.py
import datas   #datas.py
import database_func #database_func.py


app = Flask(__name__)

#get

@app.route('/', methods=['GET'])
def index():
    if(users.checkcookie(request.cookies.get('user'))):
        #prompt out alert "you are already login, redirect to dashboard"
        response = make_response(redirect(url_for('dashboard')))
        response.set_cookie('alert', 'You are already login, redirect to dashboard')
        return response
    else:
        return render_template('home.html')

@app.route('/login', methods=['GET'])
def showlogin():
    if(users.checkcookie(request.cookies.get('user'))):
        #prompt out alert "you are already login, redirect to dashboard"
        response = make_response(redirect(url_for('dashboard')))
        response.set_cookie('alert', 'You are already login, redirect to dashboard')
        return response
    else:
        return render_template('login.html')

@app.route('/signup', methods=['GET'])
def showsignup():
    if(users.checkcookie(request.cookies.get('user'))):
        #prompt out alert "you are already login, redirect to dashboard"
        response = make_response(redirect(url_for('dashboard')))
        response.set_cookie('alert', 'You are already login, redirect to dashboard')
        return response
    else:
        return render_template('signup.html')

@app.route('/dashboard', methods=['GET'])
def showdata():
    if(users.checkcookie(request.cookies.get('user'))):
        return render_template('dashboard.html')
    else:
        #prompt out alert "you are not login as our user, redirect to login page"
        response = make_response(redirect(url_for('home')))
        response.set_cookie('alert', 'You are not login as our user, redirect to login page')
        return response

@app.route('/setting', methods=['GET'])
def showdata(): 
    if(users.checkcookie(request.cookies.get('user'))):
        return render_template('setting.html')
    else:
        #prompt out js alert window :"you are not login as our user, redirect to login page"
        response = make_response(redirect(url_for('home')))
        response.set_cookie('alert', 'You are not login as our user, redirect to login page')
        return response
    
@app.route('/logout', methods=['GET'])
def logout():
    response = make_response(redirect(url_for('home')))
    #delete all cookies
    response.delete_cookie('user')
    response.delete_cookie('alert')
    return response

@app.route('/lcity', methods=['GET'])
def lcity():
    if(users.checkcookie(request.cookies.get('user'))):
        city_list = dict()
        city_list["city"] = database_func.getcity()
        city_list["num"] = len(city_list["city"])
        #in json format
        return Flask.jsonify(city_list)
    else:
        #prompt out js alert window :"you are not login as our user, redirect to login page"
        response = make_response(redirect(url_for('home')))
        response.set_cookie('alert', 'You are not login as our user, redirect to login page')
        return response

@app.route('/updata', methods=['GET'])
def updatedata():
    if(users.checkcookie(request.cookies.get('user'))):
        datas.updatecurrent()
        return "update success"
    else:
        #prompt out js alert window :"you are not login as our user, redirect to login page"
        response = make_response(redirect(url_for('home')))
        response.set_cookie('alert', 'You are not login as our user, redirect to login page')
        return response



#################################post

@app.route('/login', methods=['POST'])
def login():
    if(users.checkcookie(request.cookies.get('user'))):
        #prompt out alert "you are already login, redirect to dashboard"
        response = make_response(redirect(url_for('dashboard')))
        response.set_cookie('alert', 'You are already login, redirect to dashboard')
        return response
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        username.replace('"',"").replace("'","").replace(";","")\
                .replace(" ","").replace("=","").replace("(","").replace(")","")\
                .replace("\\","").replace("/","")
        password.replace('"',"").replace("'","").replace(";","")\
                .replace(" ","").replace("=","").replace("(","").replace(")","")\
                .replace("\\","").replace("/","")

        if users.checklogin(username, password):
            # Set a cookie upon successful login
            response = make_response('Login successful')
            #cookie expire in 10 minutes
            response.set_cookie('user', base64.baase64encode(username.encode()).decode(), max_age=600)
            return response
        else:
            return 'Login failed'

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username')
    password = request.form.get('password')
    username.replace('"',"").replace("'","").replace(";","")\
    .replace(" ","").replace("=","").replace("(","").replace(")","")\
    .replace("\\","").replace("/","")
    password.replace('"',"").replace("'","").replace(";","")\
    .replace(" ","").replace("=","").replace("(","").replace(")","")\
    .replace("\\","").replace("/","")

    # Add your signup logic here
    # For simplicity, I'm assuming that the username is unique
    # In a real application, you'd need to check for existing usernames, handle password hashing, etc.
    if(users.add_user(username, password)):
        return 'Signup successful'
    else:
        return 'Signup failed'

@app.route('/userpage')
def userpage():
    # Check if the user is logged in (you need to implement this logic)
    username = request.cookies.get('user')

    if username:
        return render_template('userpage.html', username=username)
    else:
        # Redirect to login page with an alert
        response = make_response(redirect(url_for('loginpage')))
        response.set_cookie('alert', 'Please login first')
        return response

@app.route('/lsite', methods=['POST'])
def lcity():
    if(users.checkcookie(request.cookies.get('user'))):
        site_list = dict()
        site_list["city"]=database_func.getcity(request.form.get('city'))
        site_list["num"]=len(site_list["city"])
        #in json format
        return Flask.jsonify(site_list)
    else:
        #prompt out js alert window :"you are not login as our user, redirect to login page"
        response = make_response(redirect(url_for('home')))
        response.set_cookie('alert', 'You are not login as our user, redirect to login page')
        return response

@app.route('/updategraph', methods=['POST'])
def updategraph():
    if(users.checkcookie(request.cookies.get('user'))):
        database_func.updategraph(request.form.get('city'),request.form.get('site'))
        curdata = database_func.getcurrentdata(request.form.get('city'),request.form.get('site'))
        return Flask.jsonify(curdata)
    else:
        #prompt out js alert window :"you are not login as our user, redirect to login page"
        response = make_response(redirect(url_for('home')))
        response.set_cookie('alert', 'You are not login as our user, redirect to login page')
        return response


#password_old
#password
#password_conf
@app.route('/uppwd', methods=['POST'])
def updataNewPassword():
    if(users.checkcookie(request.cookies.get('user'))):
        oldpwd = request.cookies.get('password_old')
        newpwd = request.form.get('password')
        confpwd = request.form.get('password_conf')
        oldpwd.replace('"',"").replace("'","").replace(";","")\
                .replace(" ","").replace("=","").replace("(","").replace(")","")\
                .replace("\\","").replace("/","")
        newpwd.replace('"',"").replace("'","").replace(";","")\
              .replace(" ","").replace("=","").replace("(","").replace(")","")\
              .replace("\\","").replace("/","")
        confpwd.replace('"',"").replace("'","").replace(";","")\
               .replace(" ","").replace("=","").replace("(","").replace(")","")\
               .replace("\\","").replace("/","")
        if(users.checklogin(base64.b64decode(request.cookies.get('user')).decode(),oldpwd)):
            if newpwd == confpwd:
                if users.updatepassword(base64.b64decode(request.cookies.get('user')).decode(),newpwd):
                    return "update success"
                else:
                    return "update failed(unknown error))"
            else:
                return "update failed(password not match)"
        else:
            return "update failed(wrong old password)"
    else:
        #prompt out js alert window :"you are not login as our user, redirect to login page"
        response = make_response(redirect(url_for('home')))
        response.set_cookie('alert', 'You are not login as our user, redirect to login page')
        return response

@app.route('/currentdata', methods=['POST'])
def currentdata():
    if(users.checkcookie(request.cookies.get('user'))):
        curdata = database_func.getcurrentdata(request.form.get('city'),request.form.get('site'))
        return Flask.jsonify(curdata)
    else:
        #prompt out js alert window :"you are not login as our user, redirect to login page"
        response = make_response(redirect(url_for('home')))
        response.set_cookie('alert', 'You are not login as our user, redirect to login page')
        return response
    
@app.route('/deleteAcc', methods=['POST'])
def deleteAcc():
    if(users.checkcookie(request.cookies.get('user'))):
        if deleteAcc(base64.b64decode(request.cookies.get('user')).decode()):
            response = make_response(redirect(url_for('home')))
            response.delete_cookie('user')
            response.delete_cookie('alert')
            return response
        else:
            return "delete failed(unknown error)"
    else:
        #prompt out js alert window :"you are not login as our user, redirect to login page"
        response = make_response(redirect(url_for('home')))
        response.set_cookie('alert', 'You are not login as our user, redirect to login page')
        return response

if __name__ == '__main__':
    app.run(debug=True)
