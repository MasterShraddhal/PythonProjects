from PythonProjects.shoppingapplication.classfiles.vendordetails import *
from flask import request
import json

def get_product_id():
    while True:
        pid=1000
        productlist=get_all_products()
        if productlist:
            pid=productlist[-1].prdid
            print(pid)
            pid=pid+1
        else:
            pid=pid+1
        yield pid

gen = get_product_id()


def get_all_products():
    allproducts=Products.query.all()
    return allproducts


def get_clean_product_data(pobj):
    if pobj.__dict__.__contains__('_sa_instance_state'):
        del pobj.__dict__['_sa_instance_state']
    return pobj.__dict__


@app.route("/rest/product/add",methods=["POST"])
def addproduct():
    result=request.get_json()
    print(result)
    result['prdid']=next(gen)
    pobj=Products(**result)
    print(pobj.__dict__)
    try:
        db.session.add(pobj)
        db.session.commit()
        return {'status':'success'}
    except:
        return {'status':'fail'}

def get_limited_products(number):
    allproducts=Products.query.offset(number).limit(3).all()
    print(allproducts)
    return allproducts

@app.route("/rest/product/display/", defaults={'number':'0'})
@app.route("/rest/product/display/<int:number>")
def displayproducts(number):
    productlist=get_limited_products(number)
    cleanproductlist=[]
    for prd in productlist:
        cleanproductlist.append(get_clean_product_data(prd))
    return {'data': cleanproductlist}

@app.route("/rest/product/delete",methods=["DELETE"])
def deleteproduct():
    result=request.get_json()
    pobj=Products.query.filter_by(prdid=result['prdid']).first()
    try:
        db.session.delete(pobj)
        db.session.commit()
        return {'status':'success'}
    except:
        return {'status':'fail'}

@app.route("/rest/product/update",methods=["PUT","GET"])
def updateproduct():
    if request.method=="GET":
        result=request.get_json()
        result=json.loads(result)
        pobj=Products.query.filter_by(prdid=result['prdid']).first()
        pobj=get_clean_product_data(pobj)
        return json.dumps(pobj)
    elif request.method=="PUT":
        result=request.get_json()
        result=json.loads(result)
        pobj=Products.query.filter_by(prdid=result['prdid']).first()
        pobj.prdname=result['prdname']
        pobj.prdprice=result['prdprice']
        pobj.prdqty=result['prdqty']
        pobj.prddesc=result['prddesc']
        pobj.prdimage=result['prdimage']
        try:
            db.session.commit()
            return json.dumps({'status':'success'})
        except:
            return json.dumps({'status':'fail'})

@app.route("/rest/product/search")
def searchproductdata():
    result=request.get_json()
    result=json.loads(result)
    pattern=result['item']
    #print(pattern)
    listofproducts=[]
    pobj=Products.query.filter(db.or_(Products.prdname.like('%'+pattern+'%'),Products.prddesc.like('%'+pattern+'%'),Products.prdprice.like('%'+pattern+'%'),Products.prdqty.like('%'+pattern+'%'),Products.prdcategory.like(pattern),Products.prdsubcategory.like(pattern))).all()
    print(pobj)
    for obj in pobj:
        listofproducts.append(get_clean_product_data(obj))
    print(listofproducts)
    return json.dumps({'data':listofproducts})
