# from PythonProjects.shoppingapplication.vendor.restcontrollers import restregistration
# from PythonProjects.shoppingapplication.vendor.restcontrollers import restproduct
from PythonProjects.shoppingapplication.Customer.restcontroller.restcustomer import *
from PythonProjects.shoppingapplication.Customer.restcontroller.restcustomerproducts import *
# from PythonProjects.shoppingapplication.vendor.login_registration import app


if __name__ == '__main__':
    app.run(debug=True, port=5001)