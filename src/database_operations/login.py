import pymysql
from passlib.apps import custom_app_context as pwd_context
import yaml 
import os

def validate_login(username,password):
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

    cur = db.cursor()
    query = "select * from login where  username = '{}'".format(username)
    cur.execute(query)
    db.close()
    # print all the first cell of all the rows
    for row in cur.fetchall():
        return verify_password(password,row[1])
        # if row[1] == password:
        #     return True
        # else:
        #     return False

def verify_password(password,password_hash):
    return pwd_context.verify(password, password_hash)

