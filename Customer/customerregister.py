from PythonProjects.shoppingapplication.classfiles.customerinfo import *
from flask import render_template,request,session
import requests
from PythonProjects.shoppingapplication.classfiles.customerclass import customer
import json
import logging
from logging.handlers import RotatingFileHandler
from flask.logging import default_handler

logging.basicConfig(level=logging.INFO)
fformatter=logging.Formatter('%(asctime)s -%(module)s- %(name)s -%(funcName)s- %(levelname)s - %(message)s')
rfh=RotatingFileHandler('customerinfo.log','a',maxBytes=2048,backupCount=2)
rfh.setFormatter(fformatter)
rfh.setLevel(logging.INFO)
app.logger.addHandler(rfh)



mylogger=logging.getLogger("mylogger")
mylogger.setLevel(logging.INFO)
rfh1=RotatingFileHandler('restresopnse.log','a',maxBytes=2048,backupCount=3)
rfh1.setFormatter(fformatter)
rfh1.setLevel(logging.INFO)
mylogger.addHandler(rfh1)


USER_REG='http://localhost:5001/rest/user/register'
USER_LOGIN='http://localhost:5001/rest/user/login'

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/user/register",methods=["GET","POST"])
def userregistration():
    if request.method=="POST":
        cname=request.form['cname']
        cemail=request.form['cemail']
        cpassword=request.form['cpassword']
        cpasswordre=request.form['cpasswordre']
        cmobile=request.form['cmobile']
        if cpassword==cpasswordre:
            cust=customer(cname,cemail,cpassword,cmobile)
            cust=json.dumps(cust.__dict__)
            res=requests.post(USER_REG,json=cust)
            mylogger.info("Resonpse received successfully!!!")
            result=res.json()
            print(result)
            if result['status']=='success':
                msg='customer added successfully!!!'
                return render_template("userlogin.html",msg=msg)
            else:
                msg='Unable to add Customer'
                return render_template("userreg.html",msg=msg)
        else:
            msg="Password does not match!!"
            return render_template("userreg.html", msg=msg)
    return render_template("userreg.html")



@app.route("/user/login",methods=["GET","POST"])
def userlogin():
    msg=''
    if request.method=="POST":
        email=request.form['email']
        password=request.form['password']
        userlogin=json.dumps({"email":email,"password":password})
        res=requests.get(USER_LOGIN,json=userlogin)
        result=res.json()
        if result['status']=='success':
            session['userid']=result['data']['cid']
            msg=''
            return render_template("userdisplayproductcategory.html",msg=msg)
        else:
            msg='login details are incorrect!!'
            return render_template("userlogin.html",msg=msg)
    return render_template("userlogin.html",msg=msg)




if __name__ == '__main__':
    app.run(debug=True)