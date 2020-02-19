from flask import request,jsonify
from PythonProjects.shoppingapplication.classfiles.customerinfo import app,db,Cartdetails,Customer,Address,Orderdetails
from PythonProjects.shoppingapplication.classfiles.vendordetails import Products
from PythonProjects.shoppingapplication.vendor.restcontrollers.restproduct import get_clean_product_data
import json
import datetime


@app.route("/rest/user/getsingleproduct/<int:prdid>")
def getsingleproduct(prdid):
    pobj=Products.query.filter_by(prdid=prdid).first()
    pobj=get_clean_product_data(pobj)
    return json.dumps(pobj)


@app.route("/rest/user/product/<itemtype>/<userid>")
def getproducts(itemtype,userid):
    #print(itemtype)
    pobjs=Products.query.filter(Products.prdsubcategory==itemtype).all()
    productlist=[]
    for pobj in pobjs:
        productlist.append(get_clean_product_data(pobj))
    c = Cartdetails.query.filter(Cartdetails.cid == userid).count()
    return json.dumps({"products":productlist,"count":c})

@app.route("/rest/user/product/addtocart/",methods=["POST"])
def cartdetails():
    result=request.get_json()
    result=json.loads(result)
    cartobjs=Cartdetails.query.filter(Cartdetails.cid==result['userid'],Cartdetails.pid==result['prdid']).all()
    prdobj=Products.query.filter(Products.prdid == result['prdid']).first()
    prdobj=get_clean_product_data(prdobj)
    c=Cartdetails.query.filter(Cartdetails.cid == result['userid']).count()
    if cartobjs:
        if cartobjs[0].__dict__['pqty']<10:
            try:
                cartobjs[0].pqty=cartobjs[0].__dict__['pqty']+1
                print(cartobjs[0].__dict__['pqty'])
                db.session.commit()
                msg='Product added successfully to cart!!!'
                return json.dumps({"status":"success","count":c,"prdcategory":prdobj['prdsubcategory'],"msg":msg})
            except:
                msg='Unable to add product to cart..Please try after sometime..'
                return json.dumps({"status": "fail", "count": c, "prdcategory": prdobj['prdsubcategory'],"msg":msg})
        else:
            msg='Limit is exceeded for this product..'
            return json.dumps({"status": "fail", "count": c, "prdcategory": prdobj['prdsubcategory'], "msg": msg})
    else:
        try:
            cart=Cartdetails(cid=result['userid'],pid=result['prdid'],pqty=1)
            db.session.add(cart)
            db.session.commit()
            msg="product added to cart successfully!!"
            return json.dumps({"status": "success", "count": c, "prdcategory": prdobj['prdsubcategory'], "msg": msg})
        except:
            msg='Unable to add product to cart..'
            return json.dumps({"status": "fail", "count": c, "prdcategory": prdobj['prdsubcategory'], "msg": msg})


def getlistofdata(instance):
    d={}
    d['id']=instance.id
    d['pid']=instance.pid
    d['cid']=instance.cid
    d['pqty']=instance.pqty
    return d

@app.route("/rest/user/product/<int:userid>")
def usercartproducts(userid):
    cartprodlist=[]
    objs=db.session.query(Products,Cartdetails).filter(Products.prdid==Cartdetails.pid).filter(Cartdetails.cid==userid).all()
    for obj in objs:
        finaldetails={}
        prdobj=get_clean_product_data(obj[0])
        # cartobj=get_clean_product_data(obj[1])
        cartobj=getlistofdata(obj[1])
        finaldetails.update(prdobj)
        finaldetails.update(cartobj)
        if finaldetails['prdqty']==0:
            ca=Cartdetails.query.filter(Cartdetails.cid==userid, Cartdetails.pid==finaldetails['prdid']).first()
            ca.pqty=finaldetails['prdqty']
            db.session.commit()
            msg='Product out of stock..'
            finaldetails['pqty'] = 0
            finaldetails['msg']=msg
            cartprodlist.append(finaldetails)
        elif finaldetails['prdqty']<finaldetails['pqty']:
            ca=Cartdetails.query.filter(Cartdetails.cid==userid,Cartdetails.pid==finaldetails['prdid']).first()
            ca.pqty=finaldetails['prdqty']
            db.session.commit()
            #print(ca)
            msg="{} left in stock".format(finaldetails['prdqty'])
            finaldetails['msg'] = msg
            finaldetails['pqty']=finaldetails['prdqty']
            cartprodlist.append(finaldetails)
        else:
            msg=''
            finaldetails['msg'] = msg
            cartprodlist.append(finaldetails)

    return json.dumps({"data":cartprodlist})


@app.route("/rest/user/product/remove/",methods=["POST"])
def removeproductfromcart():
    res=request.get_json()
    result=json.loads(res)
    cobj=Cartdetails.query.filter(Cartdetails.cid==result['userid'],Cartdetails.pid==result['prdid']).first()
    db.session.delete(cobj)
    db.session.commit()
    return json.dumps({"status":"success"})


@app.route("/rest/user/address/<int:userid>")
def getalladdresses(userid):
    adrobjs=Address.query.filter(Address.custid==userid).all()
    listofadrs=[]
    for adr in adrobjs:
        listofadrs.append(get_clean_product_data(adr))
    return json.dumps(listofadrs)


@app.route("/rest/user/addaddress/",methods=["POST"])
def saveaddress():
    res=request.get_json()
    result=json.loads(res)
    try:
        adrobj=Address(**result)
        db.session.add(adrobj)
        db.session.commit()
        return {'status':'success'}
    except:
        return {'status':'fail'}

@app.route("/rest/user/finalplaceorder/",methods=["POST"])
def finalplaceorders():
    res=request.get_json()
    result=json.loads(res)
    for k,v in result['data'].items():
        try:
            pobj=Products.query.filter(Products.prdid==k).first()
            obj=Orderdetails(cid=result['userid'],pid=k,vid=pobj.__dict__['vid'],pqty=v,custadr=result['adrid'],orderstatus="Order Placed",dateoforder=datetime.date.today())
            db.session.add(obj)
            db.session.commit()
            try:
                prdobj = db.session.query(Products).filter(Products.prdid == k).first()
                prdobj.prdqty=(prdobj.prdqty-int(v))
                db.session.commit()
                try:
                    cobj=Cartdetails.query.filter(Cartdetails.cid==result['userid'],Cartdetails.pid==k).first()
                    if cobj:
                        db.session.delete(cobj)
                        db.session.commit()
                except:
                    return {'status':'fail'}
            except:
                return {'status': 'fail'}
        except:
            return {'status': 'fail'}
    return {'status':'success'}

@app.route("/rest/user/vieworders/<int:userid>")
def vieworders(userid):
    orders=Orderdetails.query.filter(Orderdetails.cid==userid).order_by(Orderdetails.oid.desc()).all()
    print(orders)
    listoforders=[]
    listofpobjs=[]
    listofcleanpobj = []
    for order in orders:
        listoforders.append(get_clean_product_data(order))
    for order in listoforders:
        pobj=db.session.query(Products).filter(Products.prdid==order['pid']).first()
        listofpobjs.append(pobj)
    for i in set(listofpobjs):
        listofcleanpobj.append(get_clean_product_data(i))
    #pmjk[hjphj[p
    return jsonify({'listoforders':listoforders,'listofpobjs':listofcleanpobj})



