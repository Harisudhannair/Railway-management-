from pymysql import*
from random import*
from datetime import*
from time import*


# --charges of the tickets--
sleeper_charge = int(1.5)
third_ac_charge = int(2)
second_ac_charge = int(3)
first_ac_charge = int(4)


# --checking the availability of trains--
def availabletrains():
    try:
        con = connect(host="localhost", user="root", password="harisudhan", db="railway", port=3306)
        c = con.cursor()
        print("Search by Entering the Station Code")
        start = input("From : ")
        final = input("To : ")
        query = ("SELECT Train_No, station_name, Source_Station_Name, Destination_Station_Name, Arrival_Time, Deapature_time FROM train_info WHERE Source_Station_Code=%s AND Destination_Station_Code=%s;")
        c.eiecute(query, (start, final))
        result = c.fetchall()
        head = ["Train_no","station_name","Source_Station_Name","Destination_Station_Name","Arrival_Time"," Deapature_time"]
        print(head)
        c=0
        for i in result:
            for j in i:
                print(j,end="\t")
            print()
            c=1
        if(c==0):
            print("Invalid source or destination station code..!")
        con.close()
    except FileNotFound as e:
        print(e)
        
        
# --checking fare--
def checkfare():
    try:
        con = connect(host="localhost", user="root", password="harisudhan", db="railway", port=3306)
        c = con.cursor()
        print("Search by Entering the Station Code!")
        header = ["Train_No", "Station_name", "Distance", "Sleeper","Third_AC", "Second_AC", "First_AC"]
        start = input("From: ")
        final = input("To: ")
        c.execute('SELECT Train_No, Station_name, Distance from train_info where Source_Station_Code="{}" AND Destination_Station_Code="{}";'.format(start, final))
        result_fare = c.fetchall()
        print(header)
        print(" ")
        for i in result_fare:
            print(i,"Rs.",int(i[2])*sleeper_charge,"Rs.",int(i[2])*third_ac_charge,"Rs.",int(i[2])*second_ac_charge,"Rs.",int(i[2])*first_ac_charge,end="\t ")
            print(" ")
        con.close()
    except Error as e:
        print(e)
        
        
# --booking ticket--        
def bookticket():
    con = pymysql.connect(host="localhost", user="root", password="harisudhan", db="railway", port=3306)
    c = con.cursor()
    
    print("")
    print("--Enter the train details--")
    while True:
        try:
            Train_no = input("Enter the train number : ")
        except ValueError:
            print("please enter the valid train number")
            continue
        else:
            break
    
    print("")
    print("--Enter passsenger details--")
    while True:
        Name = input("Enter your name : ")
        if len(Name)==0:
            print("please enter your name")
        elif len(Name) > 30:
            print("Entered name is too long..!")
        else:
            break
            
    while True:
        Gender = input("Enter your gender : ")
        if len(Gender)==0:
            print("Please enter your gender")
        elif len(Gender) > 15:
            print("Entered gender character is too long..!")
        else:
            break
    
    while True:
        try:
            age = int(input("Enter your age : "))    
        except ValueError:
            print("Enter valid age..!")
        else:   
            break
            
    while True:
        try:
            Mobile_no = int(input("Enter your phone number : "))
        except ValueError:
            print("please enter the valid phone number..!")
            continue
        else:
            if len(str(Mobile_no)) == 10:
                break
            elif len(str(Mobile_no)) > 10 or len(str(Mobile_no))<10:
                print("Please enter the valid 10 digit number")
            else:   
                print("Please enter the valid phone number :")
             
    Time_of_Booking = datetime.now()
    date = Time_of_Booking.strftime("%Y-%m-%d")
    print('Booking date : ',date)
    
    booking_id = randint(1,10000)
    c.execute("select booking_id from booking_info")
    result = c.fetchall()
    used_id = []
    for i in result:
        for j in i:
            used_id.append(j)
    while True:
        if booking_id in used_id:
            booking_id = randint(1,10000)
        else:
            break
            
    print(["1.sleeper" , "2.3rd-Ac" , "3.2nd-Ac" , "4.1st-Ac"])
    cs = None
    while True:
        a = int(input("Please enter a class from the one given number : "))
        if a == 1:
            cs = "sleeper"
            break
        elif a == 2:
            cs = "3rd-Ac"
            break
        elif a == 3:
            cs = "2nd-Ac"
            break
        elif a == 4:
            cs = "1st-Ac"
            break
        else:   
            print(["1.sleeper" , "2.3rd-Ac" , "3.2nd-Ac" , "4.1st-Ac"])
            print("choose an option from above.!")
            
    while True:
        b = input("are you sure you want to book (y/n): ")
        if b in ["Y","y"]:
            print("Booking..!")
            try:
                q = "insert into booking_info values({},'{}','{}','{}',{},{},'{}','{}')".format(booking_id, Train_no, Name, Gender, age, Mobile_no, date, cs)
                c.execute(q)
            except pymysql.DataError:
                print("Error in Booking")
            else:   
                print("Booked Successfully..!")
                con.commit()
                c.close()
                con.close()
                break
        elif b in ["N","n"]:
            print("Stop Booking..")
            sleep(0.5)
            break
        else:
            print("please enter y(yes) or n(no)")
            
            
# --showbookings--            
def showbookings():
    con = pymysql.connect(host="localhost", user="root", password="harisudhan", db="railway", port=3306)
    c = con.cursor()
    
    while True:
        try:
            Mobile_no = int(input('Enter your mobile number: '))
            if len(str(Mobile_no)) != 10:
                print("Please enter a valid 10-digit mobile number.")
        except ValueError:
            print("Please enter a valid mobile number.")
        else:
            break

    q = "select * from booking_info where mobile_no={}".format(Mobile_no)
    c.execute(q)
    result = c.fetchall()
    
    print("")
    if result:
        print("Here are your bookings:")
        print("booking_id, Train_no, Name, Gender, age, Mobile_no, date, cs")
        for row in result:
            print(row)
    else:
        print("No bookings found for this mobile number.")

    c.close()
    con.close()
    
    
# --cancel ticket--    
def cancelticket():
    con = pymysql.connect(host="localhost", user="root", password="harisudhan", db="railway", port=3306)
    c = con.cursor()
    
    print("Note down the booking_id to cancel the ticket..!")
    print("booking_id, Train_no, Name, Gender, age, Mobile_no, date, cs")
    
    q = "select * from booking_info"
    c.execute(q)
    result = c.fetchall()
    for row in result:
        print(row)
    
    print("")
    while True:
        try:
            booking_id = int(input("Enter the booking_id : "))
        except ValueError:
            print("Please enter the valid id..!")
        else:
            if booking_id < 1 or booking_id > 10000:
                print("Booking id is out of range..!")
            else:
                q = "select * from booking_info where booking_id={}".format(booking_id)
                c.execute(q)
                result = c.fetchall()
                if len(result) == 0:
                    print("No records found..!")
                    break
                print("booking_id, Train_no, Name, Gender, age, Mobile_no, date, cs")
                for i in result:
                    print(i)
                
                while True:
                    a = input("Are you sure you want to cancel this (Y/N): ")
                    if a in ["Y", "y"]:
                        q = "delete from booking_info where booking_id={}".format(booking_id)
                        c.execute(q)
                        print("Your ticket has been cancelled successfully..!")
                        con.commit()
                        c.close()
                        con.close()
                        break
                    elif a in ["N", "n"]:
                        print("your ticket cancellation process exited successfully..!")
                        break
                    else:
                        print("please enter either Y,y(yes) or N,n(No)")
                break