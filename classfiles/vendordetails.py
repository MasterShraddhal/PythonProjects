from flask import Flask
from flask_sqlalchemy import SQLAlchemy

UPLOAD_FOLDER='C:\\Users\\shrad\\PycharmProjects\\PythonProjects\\shoppingapplication\\static'

app=Flask(__name__,template_folder='C:\\Users\\shrad\\PycharmProjects\\PythonProjects\\shoppingapplication\\templates')
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:shraddha@localhost/shoppingapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

db=SQLAlchemy(app)


class Token(db.Model):
    tokenid=db.Column("tokenid",db.Integer(),primary_key=True)
    tokenname=db.Column("tokenname",db.String(100))


class Vendor(db.Model):
    vid=db.Column("vid",db.Integer(),primary_key=True)
    vname=db.Column("vname",db.String(100))
    vemail=db.Column("vemail",db.String(100),unique=True)
    vpassword=db.Column("vpassword",db.String(100))
    vcompany=db.Column("vcompany",db.String(100))
    vtoken=db.Column("vtoken",db.String(100))
    products=db.relationship("Products",backref='vendor')

class Products(db.Model):
    prdid=db.Column("prdid",db.Integer(),primary_key=True)
    prdname=db.Column("prdname",db.String(100))
    prdprice=db.Column("prdprice",db.Float())
    prdqty=db.Column("prdqty",db.Integer())
    prdimage=db.Column("prdimage",db.String(50))
    prddesc=db.Column("prddesc",db.String(150))
    prdcategory=db.Column("prdcategory",db.String(100))
    prdsubcategory=db.Column("prdsubcategory",db.String(100))
    vid=db.Column("vid",db.ForeignKey('vendor.vid'),unique=False)


# if __name__ == '__main__':
#     db.create_all()