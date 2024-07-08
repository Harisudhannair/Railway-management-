from pymsql import*
from main import*

def signup():
    name = input("Enter the username : ")
    password = input("Enter the password : ")
    age = input("Enter your age : ")
    gender = input("Enter your gender : ")
    phone_no = int(input("Enter your phone number : "))
    con = connect(host="localhost",user="root",password="harisudhan",database="railway",port=3306)
    q = "insert into user_info values ('{0}','{1}',{2},'{3}',{4})".format(name,password,age,gender,phone_no)
    