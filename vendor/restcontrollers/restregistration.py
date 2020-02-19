from PythonProjects.shoppingapplication.classfiles.vendordetails import db,app,Token,Vendor
from flask import request


def get_vendor_id():
    vid=100
    vendorlist=get_all_vendors()
    if vendorlist:
        vid=vendorlist[-1].vid
        vid=vid+1
    else:
        vid=vid+1
    yield vid

gen = get_vendor_id()


def get_all_vendors():
    allvendors=Vendor.query.all()
    return allvendors


@app.route("/rest/token/",methods=["POST"])
def validate_token():
    result=request.get_json()
    newtoken=Token.query.filter(Token.tokenname==result['token']).first()
    if newtoken:
        return {'status':'success'}
    else:
        return {'status':'fail'}


@app.route("/rest/vendor/registration/",methods=["POST"])
def vendor_register():
    result=request.get_json()
    vobj=Vendor(vid=next(gen),vname=result['name'],vemail=result['email'],vpassword=result['password'],vcompany=result['company'],vtoken=result['token'])
    try:
        db.session.add(vobj)
        db.session.commit()
        return {'status':'success'}
    except:
        return {'status':'fail'}

@app.route("/rest/vendor/login/",methods=["POST"])
def vendor_login():
    result=request.get_json()
    vobj=Vendor.query.filter(Vendor.vemail==result['email']).first()
    if vobj:
        if vobj.vpassword==result['password']:
            vid=vobj.vid
            return {'status':'success','vid':vid}
        else:
            return {'status':'fail'}
    else:
        return {'status':'fail'}



if __name__ == '__main__':
    app.run(debug=True,port=5001)





