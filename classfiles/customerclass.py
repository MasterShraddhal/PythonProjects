class customer:
    def __init__(self,cname,cemail,cpassword,cmobile):
        self.cname=cname
        self.cemail=cemail
        self.cpassword=cpassword
        self.cmobile=cmobile

    def __str__(self):
        return f'''
            CustomerName: {self.cname}
            CustomerEmail : {self.cemail}
        '''

    def __repr__(self):
        return str(self)


