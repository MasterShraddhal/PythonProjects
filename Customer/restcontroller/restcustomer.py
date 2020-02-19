from PythonProjects.shoppingapplication.classfiles.customerinfo import db,app,Customer,get_clean_data
import requests
from flask import request
import json
import logging
from logging.handlers import RotatingFileHandler
import os

logging.basicConfig(level=logging.INFO)
fformatter=logging.Formatter('%(asctime)s -%(module)s- %(name)s -%(funcName)s- %(levelname)s - %(message)s')
rfh=RotatingFileHandler('customer.log','a',maxBytes=2048,backupCount=2)
rfh.setFormatter(fformatter)
rfh.setLevel(logging.INFO)
app.logger.addHandler(rfh)




@app.route("/rest/user/register",methods=["POST"])
def userregistration():
    app.logger.info("Json response received")
    res=request.get_json()
    print(res)
    try:
        result=json.loads(res)
        print(result)
        app.logger.info("Json data deserialized properly!!")
    except:
        app.logger.error("Problem during deserialization of json data")
        msg='problem while converting json data into python'
        return json.dumps({"msg":msg,"status":"fail"})
    cust=Customer(**result)
    try:
        db.session.add(cust)
        db.session.commit()
        app.logger.info("Customer added successfully!!")
        msg='User added successfully'
    except:
        app.logger.error("Exception occured while saving customer data",exc_info=True)
        msg='Unable to save customer'
        return json.dumps({"msg":msg,"status":"fail"})
    print(os.stat("C:\\Users\\shrad\\PycharmProjects\\PythonProjects\\shoppingapplication\\Customer\\restcontroller\\customer.log").st_size)
    return json.dumps({"msg":msg,"status":"success"})

@app.route("/rest/user/login",methods=["GET"])
def userlogin():
    result=request.get_json()
    res=json.loads(result)
    cust=Customer.query.filter(Customer.cemail==res['email']).first()
    if cust and (cust.cpassword==res['password']):
        app.logger.info("login details are {} and {}".format(res['email'],res['password']))
        cobj=get_clean_data(cust)
        return json.dumps({"status":"success","data":cobj.__dict__})
    else:
        app.logger.info("login details are incorrect..")
        return json.dumps({"status":"fail"})


if __name__ == '__main__':
    app.run(debug=True,port=5001)

