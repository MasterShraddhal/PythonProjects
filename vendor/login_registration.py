from PythonProjects.shoppingapplication.classfiles.vendordetails import db,app,Token
import requests
from flask import render_template,request,session,redirect
from PythonProjects.shoppingapplication.classfiles.vendorinfo import Vendorinfo

app.config['SECRET_KEY']='mysecretkey'

TOKEN_VALIDATION='http://localhost:5001/rest/token/'
VENDOR_REG='http://localhost:5001/rest/vendor/registration/'
VENDOR_LOGIN='http://localhost:5001/rest/vendor/login/'


@app.route("/vendor/loginlink")
def v_loginlink():
    return render_template("login.html")

@app.route("/vendor/login",methods=["POST"])
def v_login():
    email=request.form['email']
    password=request.form['password']
    res=requests.post(VENDOR_LOGIN,json={'email':email,'password':password})
    result=res.json()
    if result['status']=='success':
        session['vendorid']=result['vid']
        #msg='Login successful!!!'
        return redirect('http://localhost:5000/vendor/displayproducts')
    else:
        msg='Email or Password is Incorrect!!'
        return render_template("login.html",msg=msg)

@app.route("/vendor/registrationlink")
def v_registrationlink():
    return render_template("register.html")

@app.route("/vendor/registration",methods=["POST"])
def v_registration():
    name=request.form['name']
    email=request.form['email']
    password=request.form['password']
    repassword=request.form['repassword']
    company=request.form['company']
    token=request.form['token']
    res=requests.post(TOKEN_VALIDATION,json={'token':token})
    result=res.json()
    if result['status']=='success':
        if password==repassword:
            vobj=Vendorinfo(name=name,email=email,password=password,company=company,token=token)
            res=requests.post(VENDOR_REG,json=vobj.__dict__)
            r=res.json()
            if r['status']=='success':
                msg='User added successfully!!!'
            else:
                msg='Unable to add User. Try after sometime..'
                return render_template("register.html",msg=msg)
        else:
            msg='Password Mismatch!!!'
            return render_template("register.html",msg=msg)
    else:
        msg='Token is Invalid!!'
        return render_template("register.html",msg=msg)

    return render_template("login.html",msg=msg)


# if __name__ == '__main__':
#     app.run(debug=True)
