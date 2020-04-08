import pymysql
import yaml 
import os

def insert_form_data(name,fname,dob,card_number,mobile,email,address):
    # db = pymysql.connect(host="localhost",  # your host, usually localhost
    #                      user="phpmyadminuser",  # your username
    #                      passwd="password",  # your password
    #                      db="e-KYC")
    #
    query = """INSERT INTO `form_details`(`Name`, `Father_Name`, `Pan_Number`, `Date_of_Birth`, `Mobile`, `Email`, `Address`) \
                VALUES (%s, %s, %s, %s, %s, %s, %s) """
    # args = ("name","fname","card_number","dob","mobile","email","address")
    args = (name, fname, card_number, dob, mobile, email, address)
    # cursor = db.cursor()

    yml_file = os.path.join(os.getcwd(),'src/database_operations/config.yml')
    with open(yml_file, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    # db = pymysql.connect(host="localhost",  # your host, usually localhost
    #                      user="root",  # your username
    #                      passwd="",  # your password
    #                      db="e-KYC")

    db = pymysql.connect(host=cfg['mysql']['host'],  # your host, usually localhost
                         user=cfg['mysql']['user'],  # your username
                         passwd=cfg['mysql']['passwd'],  # your password
                         db=cfg['mysql']['db'])
    cursor = db.cursor()
    cursor.execute(query, args)

    db.commit()

    cursor.close()
    db.close()



    # # print all the first cell of all the rows
    # for row in cur.fetchall():
    #     if row[1] == password:
    #         return True
    #     else:
    #         return False



