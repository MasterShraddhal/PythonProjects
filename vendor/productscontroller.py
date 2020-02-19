from PythonProjects.shoppingapplication.classfiles.vendordetails import *
import requests
from flask import render_template,request,session,redirect,url_for
from PythonProjects.shoppingapplication.classfiles.vendorinfo import *
import os
import json

ADD_PRODUCT='http://localhost:5001/rest/product/add'
DISPLAY_PRODUCT='http://localhost:5001/rest/product/display'
DELETE_PRODUCT='http://localhost:5001/rest/product/delete'
UPDATE_PRODUCT='http://localhost:5001/rest/product/update'
SEARCH_DATA='http://localhost:5001/rest/product/search'

pagination=0

# def getLimitedProducts(number = 0)

@app.route("/vendor/displayproducts")
def displayproducts():
    res=requests.get(DISPLAY_PRODUCT)
    result=res.json()
    #print(result)
    return render_template("displayproducts.html",products=result,pagination=pagination)


@app.route("/vendor/addproductlink")
def addproductslink():
    return render_template("addproduct.html")

@app.route("/vendor/addproduct",methods=["POST"])
def addproduct():
    prdname=request.form['prdname']
    prdprice=request.form['prdprice']
    prddesc=request.form['prddesc']
    prdqty=request.form['prdqty']
    prdcategory=request.form['categories']
    prdsubcategory=request.form['subcategories']
    f=request.files['prdimage']
    prdimage=f.filename
    f.save(os.path.join(app.config['UPLOAD_FOLDER'],f.filename))
    pobj=Productinfo(prdname,prdprice,prdqty,prddesc,prdimage)
    pobj.__dict__['prdcategory']=prdcategory
    pobj.__dict__['prdsubcategory']=prdsubcategory
    pobj.__dict__['vid']=session['vendorid']
    print(pobj.__dict__)
    res=requests.post(ADD_PRODUCT,json=pobj.__dict__)
    result=res.json()
    print(result)
    if result['status']=='success':
        msg='Product added successfully!!!'
        return redirect(url_for('displayproducts'))
    else:
        msg='Unable to add Product..Please try again..'
        return redirect(url_for('displayproducts'))


@app.route("/vendor/deleteproduct/<int:prdid>/<prdimage>")
def deleteproduct(prdid,prdimage):
    global pagination
    res=requests.delete(DELETE_PRODUCT,json={'prdid': prdid})
    result=res.json()
    if result['status']=='success':
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'],prdimage))
            #pagination-=1
            res=requests.get(DISPLAY_PRODUCT + "/" + str(pagination))
            print(res.json())
            result=res.json()
        except:
            print("unable to delete")
    return render_template("displayproducts.html",products=result,pagination=pagination)

@app.route("/vendor/updateproduct/<int:prdid>",methods=["GET","POST"])
def editproduct(prdid):
    if request.method=="GET":
        r=json.dumps({'prdid':prdid})
        res=requests.get(UPDATE_PRODUCT,json=r)
        result=res.json()
        return render_template("updateproduct.html",product=result)
    elif request.method=="POST":
        r=json.dumps({'prdid': prdid})
        res=requests.get(UPDATE_PRODUCT, json=r)
        result=res.json()
        file=request.files['prdimage']
        print(result)
        if file.filename!='':
            prdname=request.form['prdname']
            prdprice=request.form['prdprice']
            prdqty=request.form['prdqty']
            prddesc=request.form['prddesc']
            f=request.files['prdimage']
            prdimage = f.filename
            pobj=Productinfo(prdname, prdprice, prdqty, prddesc, prdimage)
            pobj.__dict__['prdid']=prdid
            jsonpobj=json.dumps(pobj.__dict__)
            res=requests.put(UPDATE_PRODUCT, json=jsonpobj)
            updatedresult=res.json()
            if updatedresult['status']=='success':
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], result['prdimage']))
                f.save(os.path.join(app.config['UPLOAD_FOLDER'],prdimage))
            return redirect(url_for('displayproducts'))
        else:
            prdname=request.form['prdname']
            prdprice=request.form['prdprice']
            prdqty=request.form['prdqty']
            prddesc=request.form['prddesc']
            prdimage=result['prdimage']
            pobj = Productinfo(prdname, prdprice, prdqty, prddesc, prdimage)
            pobj.__dict__['prdid'] = prdid
            jsonpobj = json.dumps(pobj.__dict__)
            res = requests.put(UPDATE_PRODUCT, json=jsonpobj)
            updatedresult = res.json()
            if updatedresult['status'] == 'success':
                return redirect(url_for('displayproducts'))
            else:
                return redirect(url_for('displayproducts'))


@app.route("/vendor/product/next")
def nextproducts():
    global pagination
    pagination+=3
    res=requests.get(DISPLAY_PRODUCT+"/"+str(pagination))
    print(res.json())
    result=res.json()
    return render_template("displayproducts.html",products=result,pagination=pagination)

@app.route("/vendor/product/previous")
def previousproducts():
    global pagination
    pagination-=3
    if pagination<0:
        return redirect(url_for('displayproducts'))
    res = requests.get(DISPLAY_PRODUCT + "/" + str(pagination))
    result = res.json()
    return render_template("displayproducts.html",products=result,pagination=pagination)



@app.route("/vendor/search", methods=["POST"])
def searchdata():
    searchitem=request.form['searchitem']
    result=json.dumps({'item':searchitem})
    print(result)
    res=requests.get(SEARCH_DATA,json=result)
    resofproducts=res.json()
    print(resofproducts)
    return render_template("displayproducts.html",products=resofproducts,pagination=pagination)