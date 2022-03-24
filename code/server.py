from plistlib import UID
import time
from time import sleep
import socket
import threading as td
import sys
from pysql import mysqls as ms

sql = ms.MySql()
ADMIN_PORT = 9999
broadcast = '<broadcast>'  # ใช้สำหรับติดต่อไปยังผู้ใช้ทุกคนใน server
my_ip = 'localhost'
PORT = 5050
PORT2 = 5000
BUFFSIZE = 10100

clientlist = []  # เก็บผู้ใช้ที่ connect เข้ามา

# print(type(clientlist))


def say(s):
    print(s+" is second input")


def send_to_all():
    msg = 'Hello this is message from Admin.'.encode("utf-8")
    dest = (broadcast, PORT2)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    for i in range(5):
        s.sendto(msg, dest)
    print('='*15+' Sending '+'='*15)


def client_handler(client, addr):  # รองรับผู้ใช้หลายคน
    # login = False
    while True:
        try:
            data = client.recv(BUFFSIZE).decode('utf-8')
            if data == '1':
                client.send(('Welcome to Login').encode('utf-8'))
                client.send(('Enter your Username').encode('utf-8'))
                username = client.recv(BUFFSIZE).decode('utf-8')
                client.send(('Enter your Password').encode('utf-8'))
                password = client.recv(BUFFSIZE).decode('utf-8')
                login = loginClient(username, password)
                if login == True:
                     client.send(("Welcome You are logged!!").encode('utf-8'))
                else:
                    client.send(
                        ("Error Invalid Username & Password\n").encode('utf-8'))
            elif data == '2':
                client.send(('Welcome to Register').encode('utf-8'))
                client.send(('Enter your Username').encode('utf-8'))
                username = client.recv(BUFFSIZE).decode('utf-8')
                client.send(('Enter your Password').encode('utf-8'))
                password = client.recv(BUFFSIZE).decode('utf-8')
                client.send(('Enter your Address').encode('utf-8'))
                address = client.recv(BUFFSIZE).decode('utf-8')
                regis = registerClient(username, password, address)
                if regis == True:
                    client.send(('You are registered!').encode('utf-8'))
                else:
                    client.send(('Please try again').encode('utf-8'))
                # client.send((uid,username).encode('utf-8'))
            elif data == '3':
                if login == True:
                    client.send(('Welcome to Bill History').encode('utf-8'))
                    client.send((getBilUser()).endcode('utf-8'))
                else:
                    client.send(('You must be logged').encode('utf-8'))
            elif data == '4':
                if login == True:
                    client.send(('Welcome to Order Food').encode('utf-8'))
                    #####################################################
                    ##### Function Order Food ##########################
                    ####################################################
                else:
                    client.send(('You must be logged').encode('utf-8'))
            ##########################
            # เรียกใช้ฟังชั่น login ตรงนี้  #
            ##########################
        except:
            clientlist.remove(client)
            break
        # exit funtion
        if(not data) or (data == 'q'):
            clientlist.remove(client)
            print('USER OUT : ', addr)
            break
        masage = str(addr) + ' >>> ' + data
        print('Masage from User : ', masage)
        ##############ตอบกลับ###########
        # client.send(("we recive "+data).encode('utf-8'))
        # client.send(("we recive2 "+data).encode('utf-8'))
        ############################################################################
        ###         ส่งข้อความหาผู้ใช้หลายครั้งได้โดยไม่ต้องรอผู้ใช้ตอบกลับ                  ###
        # for i in range(5):
        #     print(i)
        #     client.send("Masage from server: testing{}".format(i).encode('utf-8'))
        ############################################################################

    # user exit
    client.close()
    sys.exit()


def client_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind((my_ip, PORT))
    server.listen(5)

    while True:
        print('Waiting for client... PORT for Client: ', PORT)
        client, addr = server.accept()
        clientlist.append(client)
        print('connet form: ', addr)

        task = td.Thread(target=client_handler, args=(client, addr))
        task.start()


def addmin_server():
    server2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server2.bind((my_ip, ADMIN_PORT))
    server2.listen(1)

    print('Waiting for Admin... PORT for Admin: ', ADMIN_PORT)
    admin, addr = server2.accept()

    print('Admin is connect form: ', addr)
    login = False
    while True:
        try:
            data = admin.recv(BUFFSIZE).decode('utf-8')
            if data == '1':
                ################################################
                ##  Username : admin , Password : admin ########
                ################################################
                admin.send(('Welcome to Login').encode('utf-8'))
                admin.send(('Enter your Username').encode('utf-8'))
                username = admin.recv(BUFFSIZE).decode('utf-8')
                admin.send(('Enter your Password').encode('utf-8'))
                password = admin.recv(BUFFSIZE).decode('utf-8')
                login = loginAdmin(username, password)
                if login == True:
                     admin.send(("Welcome You are logged!!").encode('utf-8'))
                else:
                    admin.send(
                        ("Error Invalid Username & Password\n").encode('utf-8'))

            elif data == '2':
                if login == True:
                    admin.send(('Get All User').encode('utf-8'))
                    admin.send((sql.getAllUser()).encode('utf-8'))
                else:
                    admin.send(('You must be logged').encode('utf-8'))

            elif data == '3':
                if login == True:
                    admin.send(('Delete User').encode('utf-8'))
                    admin.send(('Enter UID').encode('utf-8'))
                    UIDs = admin.recv(BUFFSIZE).decode('utf-8')
                    admin.send(('Enter Username').encode('utf-8'))
                    username = admin.recv(BUFFSIZE).decode('utf-8')
                    deleteuser = DeleteUser(UIDs, username)
                    if deleteuser == True:
                        admin.send(('User was droped ').encode('utf-8'))
                    else:
                        admin.send(('Can not drop user').encode('utf-8'))
                else:
                    admin.send(('You must be logged').encode('utf-8'))

            elif data == '4':
                if login == True:
                    admin.send(('Get All Bill').encode('utf-8'))
                    admin.send((sql.getAllBill()).encode('utf-8'))
                else:
                    admin.send(('You must be logged').encode('utf-8'))

            elif data == '5':
                if login == True:
                    admin.send(('Add Food').encode('utf-8'))
                    admin.send(('Enter Foodname').encode('utf-8'))
                    name = admin.recv(BUFFSIZE).decode('utf-8')
                    admin.send(('Enter Price').encode('utf-8'))
                    price = admin.recv(BUFFSIZE).decode('utf-8')
                    addfood = addFood(name, price)
                    if addfood == True:
                        admin.send(('Succeed Food was added ').encode('utf-8'))
                    else:
                        admin.send(('There is already a food with this name').encode('utf-8'))
                else:
                    admin.send(('You must be logged').encode('utf-8'))

            elif data == '6':
                if login == True:
                    admin.send(('Delete Food').encode('utf-8'))
                    admin.send(('Enter FID').encode('utf-8'))
                    fid = admin.recv(BUFFSIZE).decode('utf-8')
                    admin.send(('Enter Foodname').encode('utf-8'))
                    fname = admin.recv(BUFFSIZE).decode('utf-8')
                    deletefood = sql.deleteFoods(fid, fname)
                    if deletefood == True:
                        admin.send(('Succeed Food was deleted ').encode('utf-8'))
                    else:
                        admin.send(('Please try againt').encode('utf-8'))
                else:
                    admin.send(('You must be logged').encode('utf-8'))

            elif data == '7':
                if login == True:
                    admin.send(('Get All Food').encode('utf-8'))
                    admin.send((sql.getAllFood()).encode('utf-8'))
                else:
                    admin.send(('You must be logged').encode('utf-8'))

            elif data == '8':
                if login == True:
                    admin.send(('Top Sell Food').encode('utf-8'))
                    admin.send((sql.topsell()).encode('utf-8'))
                else:
                    admin.send(('You must be logged').encode('utf-8'))
            ##########################
            # เรียกใช้ฟังชั่น login ตรงนี้  #
            ##########################

        except:
            break
        # exit funtion
        if data == 'q':
            print('USER OUT : ', addr)
            break
        elif not data:
            print("You must be logged")
            break

        masage = 'Admin >>> ' + data
        print('Masage from User : ', masage)
        ##########Addmin เรียกใช้ sende_to_all#############
        if (data == "sta"):
            send_to_all()
        mstr = ""
        # admin.send(("we recive "+data+" first").encode('utf-8'))

        ########## การรับคำสั่งจากผู้ใช้หลายครั้ง #############
        if (data == "say"):
            admin.send((" input massage for say ").encode('utf-8'))
            # ------<<<<<<<<<รอรับ input จากผู้ใช้เป็นครั้งที่ 2>>>>>>>>
            mstr = admin.recv(BUFFSIZE).decode('utf-8')
            say(mstr)
            admin.send(("we recive "+mstr+" second").encode('utf-8'))

    admin.close()
    sys.exit()

def DeleteUser(UIDs,username):
    print("Admin Drop User")
    dluser = sql.dropUser(UIDs,username)
    if dluser == True:
        return True

def Getfood(foodname):
    print("Admin get food")
    getf = sql.getFoods(foodname)
    if getf == True:
        return True

def loginClient(username,password):
    print("User Login")
    log = sql.login(username,password)
    if log == True:
        return True
    
def loginAdmin(username,password):
    print("Admin Login")
    log = sql.loginAd(username,password)
    if log == True:
        return True

def registerClient(username,password,address):
    print("User Register")
    res = sql.createUser(username, password, address)
    if res == True:
        return True

def getBilUser():
    print("Bill History")
    sql.getbillUserDetail("","")

def addFood(foodname,price):
    print("Admin Add Food")
    adfood = sql.addFoods(foodname,price)
    if adfood == True:
        return True

def Deletefood(FID,foodname):
    print("Admin Delete Food")
    dlfood = sql.deleteFoods(FID,foodname)
    if dlfood == True:
        return True
######################################################
############# รัน server รัน Code ที่นี่ ##################
#####################################################
if __name__ == '__main__':
    task1 = td.Thread(target=client_server)
    task1.start()
    time.sleep(0.25) # รอให้เซิร์ฟเวอร์แรกรันเสร็จก่อน
    task2 = td.Thread(target=addmin_server)
    task2.start()
