class Vendorinfo:
    def __init__(self,name,email,password,company,token):
        self.name=name
        self.email=email
        self.password=password
        self.company=company
        self.token=token

    def __str__(self):
        return f'''
            Name : {self.name}
            Email : {self.email}
            '''
    def __repr__(self):
        return str(self)

class Productinfo:
    def __init__(self,prdname,prdprice,prdqty,prddesc,prdimage):
        self.prdname=prdname
        self.prdprice=prdprice
        self.prdqty=prdqty
        self.prddesc=prddesc
        self.prdimage=prdimage

    def __str__(self):
        return f'''
            Name : {self.prdname}
            Price : {self.prdprice}
        '''

    def __repr__(self):
        return str(self)