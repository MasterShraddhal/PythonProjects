from flask import request,render_template,session,redirect,url_for
from PythonProjects.shoppingapplication.classfiles.customerinfo import app
import requests
import json



SEARCH_DATA='http://localhost:5001/rest/user/product/'
CART_DATA='http://localhost:5001/rest/user/product/addtocart/'
DISPLAY_CART_PRODUCTS='http://localhost:5001/rest/user/product/'
REMOVE_PROD='http://localhost:5001/rest/user/product/remove/'
CUST_ADRS='http://localhost:5001/rest/user/address/'
ADD_CUST_ADDRESS='http://localhost:5001/rest/user/addaddress/'
PLACE_ORDER='http://localhost:5001/rest/user/finalplaceorder/'
GET_SINGLE_PROD='http://localhost:5001/rest/user/getsingleproduct/'
VIEW_ORDERS='http://localhost:5001/rest/user/vieworders/'

# hi master shraddha djfhkj
#atuuuuuuuuuuuu;llllllllllllllllllllll
#bfhjfhjdsgfhjfhjdsgfhjsdgfhf

@app.route("/user/search/product/<itemtype>", methods=["GET"])
def searchdata(itemtype):
    userid=session['userid']
    print(itemtype)
    print(SEARCH_DATA+itemtype)
    res=requests.get(SEARCH_DATA+itemtype+"/"+str(userid))
    resofproducts=res.json()
    print(resofproducts)
    return render_template("userdisplayproducts.html",products=resofproducts['products'],userid=userid,count=resofproducts['count'])

@app.route("/user/product/addtocart/<int:prdid>")
def addtocart(prdid):
    userid=session['userid']
    data=json.dumps({"prdid":prdid,"userid":userid})
    res=requests.post(CART_DATA,json=data)
    result=res.json()
    if result['status']=='success':
        return redirect("http://localhost:5000/user/search/product/"+result['prdcategory'])
    else:
        return redirect("http://localhost:5000/user/search/product/"+result['prdcategory'])

@app.route("/user/product/cart/<int:userid>")
def userproductcart(userid):
    flag=True
    res=requests.get(DISPLAY_CART_PRODUCTS+str(userid))
    result=res.json()
    productdetail=result['data']
    #print(productdetail)
    prodtotal=0
    for prod in productdetail:
        if prod['pqty']==0:
            flag=False
        prodtotal=prodtotal+prod['pqty']*prod['prdprice']
    return render_template("displaycartproducts.html",products=productdetail,totalamount=prodtotal,flag=flag)

@app.route("/user/product/remove/<int:prdid>")
def removeproduct(prdid):
    jsonobj=json.dumps({"userid":session['userid'],"prdid":prdid})
    res=requests.post(REMOVE_PROD,json=jsonobj)
    result=res.json()
    if result['status']=='success':
        return redirect("http://localhost:5000/user/product/cart/"+str(session['userid']))



@app.route("/user/product/addaddress",methods=["GET","POST"])
def addaddressofcust():
    if request.method=="GET":
        return render_template("addnewaddress.html")
    else:
        name=request.form['name']
        mobileno=request.form['mobileno']
        pincode=request.form['pincode']
        address=request.form['address']
        locality=request.form['locality']
        city=request.form['city']
        state=request.form['state']
        custid=session['userid']
        data={'name':name,'mobileno':mobileno,'pincode':pincode,'address':address,'locality':locality,'city':city,'state':state,'custid':custid}
        res=requests.post(ADD_CUST_ADDRESS,json=json.dumps(data))
        result=res.json()
        if result['status']=='success':
            res=requests.get(CUST_ADRS + str(session['userid']))
            result=res.json()
            return render_template("address.html", listofadrs=result)


@app.route("/user/product/placeorder",methods=['POST'])
def placeorder():
    orders=dict(request.form)
    session['data'] = orders
    # orders['userid']=session['userid']
    res=requests.get(CUST_ADRS+str(session['userid']))
    result=res.json()
    return render_template("address.html",listofadrs=result)


@app.route("/user/product/finalplaceorder",methods=['POST'])
def finalplaceorder():
    adrid=request.form['address']
    jsonobj=json.dumps({'data':session['data'],'userid':session['userid'],'adrid':adrid})
    res=requests.post(PLACE_ORDER,json=jsonobj)
    result=res.json()
    if result['status']=='success':
        return render_template("success.html",msg='Order Placed Successfully!!.. Thank You for shopping with us..')
    else:
        return render_template("success.html", msg='Unable to Place order at this moment..')



@app.route("/user/product/buynow/<int:prdid>")
def productbuynow(prdid):
    res=requests.get(CUST_ADRS+str(session['userid']))
    result=res.json()
    prodres=requests.get(GET_SINGLE_PROD+str(prdid))
    prodresult=prodres.json()
    prodinfo={'prdname':prodresult['prdname'],'prdimage':prodresult['prdimage'],'prdqty':prodresult['prdqty'],'prdprice':prodresult['prdprice'],'prdid':prodresult['prdid']}
    # print(result)
    # print(prodresult)
    return render_template("buynow.html",adrs=result,prdinfo=prodinfo)

@app.route("/user/product/buynow/placeorder",methods=['POST'])
def placeorderbuynow():
    adrid=request.form['address']
    data=dict(request.form)
    prd=data.pop('address')
    jsonobj = json.dumps({'data': data , 'userid': session['userid'], 'adrid': adrid})
    res = requests.post(PLACE_ORDER, json=jsonobj)
    result = res.json()
    if result['status'] == 'success':
        return render_template("success.html", msg='Order Placed Successfully!!.. Thank You for shopping with us..')
    else:
        return render_template("success.html", msg='Unable to Place order at this moment..')


@app.route("/user/product/vieworders")
def vieworders():
    res=requests.get(VIEW_ORDERS+str(session['userid']))
    result=res.json()
    print(result)
    ordlist=[]
    for order in result['listoforders']:
        for prd in result['listofpobjs']:
            if order['pid']==prd['prdid']:
                order['prdname']=prd['prdname']
                order['prddesc']=prd['prddesc']
                order['prdimage']=prd['prdimage']
                ordlist.append(order)
    print(ordlist)
    return render_template("vieworders.html",ordlist=ordlist)

