import time
import random
import sys

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import xlrd
from xlrd import open_workbook
import xlutils
from xlutils.copy import copy

class Identity:
    def __init__(self, first_name, last_name, sex, birthday, age, email, username, password):
        self.first_name = first_name
        self.last_name = last_name
        self.sex = sex
        self.birthday = birthday
        self.age = age
        self.email = email
        self.username = username
        self.password = password

    def printIdentity(self):
        print(self.first_name)
        print(self.last_name)
        print(self.sex)
        print(self.birthday)
        print(self.age)
        print(self.email)
        print(self.username)
        print(self.password)

def startDriver():
    return webdriver.Firefox()

def getIdentity(driver):
    try:
        details_container = driver.find_element_by_id('details')

        full_name = details_container.find_element_by_class_name('address').find_element_by_tag_name('h3').text.split(' ')
        first_name = full_name[0]
        last_name = full_name[2]
        extras_array = details_container.find_element_by_class_name('extra').find_elements_by_class_name('dl-horizontal')
        birthday = extras_array[5].find_element_by_tag_name('dd').text.strip()
        age = extras_array[6].find_element_by_tag_name('dd').text.strip().split(' ')[0]
        email = extras_array[8].find_element_by_tag_name('dd').text.strip().split('\n')[0]
        username = extras_array[9].find_element_by_tag_name('dd').text.strip()
        password = extras_array[10].find_element_by_tag_name('dd').text.strip()
        return Identity(first_name, last_name, "sex", birthday, age, email, username, password)
    except:
        print "Error gathering identity.."
        time.sleep(2)
        getIdentity(driver)



def saveIdentity(identity,i):
    workbook = open_workbook("identities.xls")
    workbookWrite = copy(workbook)
    worksheetWrite = workbookWrite.get_sheet(0) if identity.sex == 'male' else workbookWrite.get_sheet(1)
    worksheetWrite.write(i,0,identity.first_name)
    worksheetWrite.write(i,1,identity.last_name)
    worksheetWrite.write(i,2,identity.sex)
    worksheetWrite.write(i,3,identity.birthday)
    worksheetWrite.write(i,4,identity.age)
    worksheetWrite.write(i,5,identity.email)
    worksheetWrite.write(i,6,identity.username)
    worksheetWrite.write(i,7,identity.password)
    workbookWrite.save('identities.xls')

def generateNewIdentity(driver,url):
    driver.get(url)

def setSex(sex):
    url = "http://www.fakenamegenerator.com/gen-male-us-us.php" if sex == 'male' else "http://www.fakenamegenerator.com/gen-female-us-us.php"
    return url

def getFirstOpenCell(sex):
    workbookRead = xlrd.open_workbook('identities.xls')
    worksheet = workbookRead.sheet_by_name('Males') if sex == 'male' else workbookRead.sheet_by_name('Females')
    i = 0
    try:
        while worksheet.cell(i,0).value != 0:
            i += 1
    except:
        print "Starting at cell: " + str(i)
    return i

def print_total_identities_gathered(current_total):
    sys.stdout.write('\r' + "Current total: " + str(current_total))
    sys.stdout.flush()
    time.sleep(1)

def clearPrint():
    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'
    print(ERASE_LINE + CURSOR_UP_ONE)

def main():
    sex = ['male','female']
    sex = sex[1]
    url = setSex(sex)
    start = getFirstOpenCell(sex)
    driver = startDriver()
    driver.get(url)
    count = 10
    for i in range(start,count):
        print_total_identities_gathered(i + 1)
        identity = getIdentity(driver)
        identity.sex = sex
        saveIdentity(identity,i)
        generateNewIdentity(driver,url)
        clearPrint()

    driver.quit()

if __name__ == "__main__":
	main()
