from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
import base64
import users   #users.py
import datas   #datas.py
import database_func #database_func.py


app = Flask(__name__)

#get

@app.route('/', methods=['GET'])
def homePage():
    if(request.cookies.get('user')!=None and users.checkcookie(request.cookies.get('user'))):
        #prompt out alert "you are already login, redirect to dashboard"
        
        response = make_response(redirect(url_for('dashboardPage')))
        return response
    else:
        return render_template('home.html')

@app.route('/login', methods=['GET'])
def loginPage():
    if(request.cookies.get('user')!=None and users.checkcookie(request.cookies.get('user'))):
        #prompt out alert "you are already login, redirect to dashboard"
        response = make_response(redirect(url_for('dashboardPage')))
        return response
    else:
        return render_template('login.html')

@app.route('/signup', methods=['GET'])
def signupPsge():
    if(request.cookies.get('user') !=None and users.checkcookie(request.cookies.get('user'))):
        #prompt out alert "you are already login, redirect to dashboard"
        response = make_response(redirect(url_for('dashboardPage')))
        return response
    else:
        return render_template('signup.html')

@app.route('/dashboard', methods=['GET'])
def dashboardPage():
    if(request.cookies.get('user')!=None and users.checkcookie(request.cookies.get('user'))):
        return render_template('dashboard.html')
    else:
        #prompt out alert "you are not login as our user, redirect to login page"
        response = make_response(redirect(url_for('homePage')))
        return response

@app.route('/setting', methods=['GET'])
def SettingPage():
    if(request.cookies.get('user')!=None and users.checkcookie(request.cookies.get('user'))):
        return render_template('setting.html')
    else:
        #prompt out js alert window :"you are not login as our user, redirect to login page"
        response = make_response(redirect(url_for('homePage')))
        return response
    
@app.route('/logout', methods=['GET'])
def logoutAPI():
    response = make_response(redirect(url_for('homePage')))
    #delete all cookies
    response.set_cookie('user', '', expires=0)
    response.set_cookie('alert', '', expires=0)
    return response

@app.route('/lcity', methods=['GET'])
def lcityAPI():
    if(request.cookies.get('user')!=None and users.checkcookie(request.cookies.get('user'))):
        city_list = dict()
        city_list["city"] = database_func.getcity()
        #in json format
        return jsonify(city_list)
    else:
        #prompt out js alert window :"you are not login as our user, redirect to login page"
        response = make_response(redirect(url_for('homePage')))
        return response

@app.route('/updata', methods=['GET'])
def updatedataAPI():
    if(request.cookies.get('user')!=None and users.checkcookie(request.cookies.get('user'))):
        datas.updatecurrent()
        return "update success"
    else:
        #prompt out js alert window :"you are not login as our user, redirect to login page"
        response = make_response(redirect(url_for('homePage')))
        return response



#################################post

@app.route('/login', methods=['POST'])
def loginAPI():
    if(request.cookies.get('user')!=None and users.checkcookie(request.cookies.get('user'))):
        #prompt out alert "you are already login, redirect to dashboard"
        response = make_response(redirect(url_for('dashboardPage')))
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
            response = make_response(redirect(url_for('dashboardPage')))
            #cookie expire in 10 minutes
            response.set_cookie('user', base64.b64encode(username.encode()).decode(), max_age=600)
            return response
        else:
            return 'Login failed'

@app.route('/signup', methods=['POST'])
def signupAPI():
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
        response = make_response(redirect(url_for('loginPage')))
        return 'Signup successful'
    else:
        res=make_response('Signup failed')
        return 'Signup failed'

@app.route('/lsite', methods=['POST'])
def lsiteAPI():
    if(request.cookies.get('user')!=None and users.checkcookie(request.cookies.get('user'))):
        """
        post input from this code
        fetch('/lsite', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ name: 'site', city: selectedCity }),
            })
        """
        selectCity = request.get_json()['city']
        if(selectCity!=None):
            site_list = dict()
            site_list["site"]=database_func.get_site_in_city(selectCity)
            print(site_list)
            #in json format
            return jsonify(site_list)
        else:
            site_list = dict()
            site_list["site"]=list()
            #in json format
            return jsonify(site_list)
    else:
        #prompt out js alert window :"you are not login as our user, redirect to login page"
        response = make_response(redirect(url_for('homeAPI')))
        return response

@app.route('/updategraph', methods=['POST'])
def updategraphAPI():
    if(request.cookies.get('user')!=None and users.checkcookie(request.cookies.get('user'))):
        print(request.form.get('city'))
        print(request.form.get('site'))
        database_func.updategraph(request.form.get('city'),request.form.get('site'))
        curdata = database_func.getcurrentdata(request.form.get('city'),request.form.get('site'))
        res=dict()
        res["data"]=curdata
        res['img1']=open('static/img/1.png','rb').read()
        res['img2']=open('static/img/2.png','rb').read()
        return jsonify(res)
    else:
        #prompt out js alert window :"you are not login as our user, redirect to login page"
        response = make_response(redirect(url_for('homeAPI')))
        return response

#password_old
#password
#password_conf
@app.route('/uppwd', methods=['POST'])
def updataNewPasswordAPI():
    if(request.cookies.get('user')!=None and users.checkcookie(request.cookies.get('user'))):
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
        response = make_response(redirect(url_for('homePage')))
        return response

@app.route('/currentdata', methods=['POST'])
def currentdataAPI():
    if(request.cookies.get('user')!=None and users.checkcookie(request.cookies.get('user'))):
        curdata = database_func.getcurrentdata(request.form.get('city'),request.form.get('site'))
        return jsonify(curdata)
    else:
        #prompt out js alert window :"you are not login as our user, redirect to login page"
        response = make_response(redirect(url_for('homePage')))
        return response
    
@app.route('/deleteAcc', methods=['POST'])
def deleteAccAPI():
    if(request.cookies.get('user')!=None and users.checkcookie(request.cookies.get('user'))):
        if users.deleteAccount(base64.b64decode(request.cookies.get('user')).decode()):
            response = make_response(redirect(url_for('homePage')))
            response.delete_cookie('user')
            response.delete_cookie('alert')
            return response
        else:
            return "delete failed(unknown error)"
    else:
        #prompt out js alert window :"you are not login as our user, redirect to login page"
        response = make_response(redirect(url_for('homePage')))
        return response

if __name__ == '__main__':
    app.run(debug=True)