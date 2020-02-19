from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__,template_folder='C:\\Users\\shrad\\PycharmProjects\\PythonProjects\\shoppingapplication\\templates')
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:shraddha@localhost/shoppingapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY']='thesecretkey'
# app.config['SQLALCHEMY_ECHO']=True

db=SQLAlchemy(app)


def get_clean_data(instance):
    if instance.__dict__.__contains__('_sa_instance_state'):
        instance.__dict__.pop('_sa_instance_state')
    return instance


class Customer(db.Model):
    cid=db.Column("cust_id",db.Integer(),primary_key=True)
    cname=db.Column("cust_name",db.String(100))
    cpassword=db.Column("cust_password",db.String(100))
    cemail=db.Column("cust_email",db.String(100),unique=True)
    cmobile=db.Column("cust_mobile",db.Integer(),unique=True)
    adr=db.relationship("Address",backref='custref',uselist=True,lazy=True)

class Cartdetails(db.Model):
    id=db.Column("id",db.Integer(),primary_key=True)
    cid=db.Column("uid",db.Integer())
    pid=db.Column("pid",db.Integer())
    pqty=db.Column("pqty",db.Integer())


class Orderdetails(db.Model):
    oid=db.Column("oid",db.Integer(),primary_key=True)
    cid=db.Column("cid",db.Integer())
    pid=db.Column("pid",db.Integer())
    vid=db.Column("vid",db.Integer())
    orderstatus=db.Column("status",db.String(100))
    dateoforder=db.Column("dateoforder",db.Date())
    pqty=db.Column("pqty",db.Integer())
    custadr=db.Column("custadr",db.ForeignKey('address.adrid'))

class Address(db.Model):
    adrid=db.Column("adrid",db.Integer(),primary_key=True)
    pincode=db.Column('pincode',db.Integer())
    address=db.Column("address",db.String(100))
    locality=db.Column("locality",db.String(100))
    city=db.Column("city",db.String(50))
    state=db.Column("state",db.String(100))
    mobileno=db.Column("mobileno",db.String(100))
    name=db.Column("name",db.String(100))
    custid=db.Column("custid",db.ForeignKey('customer.cust_id'))
    orderid=db.relationship("Orderdetails",backref='adrref',lazy=True,uselist=True)

if __name__ == '__main__':
    db.create_all()
