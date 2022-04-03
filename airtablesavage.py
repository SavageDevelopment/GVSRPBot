from pyairtable import Table
from pyairtable.formulas import match
import json

table = Table('keyj8JMybj9QDuTd3', 'appFeOjUSppJHJNHo', 'Sessions')
regTable = Table('keyj8JMybj9QDuTd3', 'appFeOjUSppJHJNHo', 'Registration')
udTable = Table('keyj8JMybj9QDuTd3', 'appFeOjUSppJHJNHo', 'UserData')

def newsession(host, hostid):
    table.create({"hostid" : str(hostid),
    "host" : host,
    "status" : "0",
    "link" : ""})

def getsessioninfo(hostid):
    result = table.all(formula=match({"hostid" : str(hostid)}))
    data = result[0]
    id = data['id']
    return(id)

def updateplayerinfo(id, newdata):
    table.update(id, newdata)

def deletesession(id):
    table.delete(id)

def addlink(id, link):
    newdict = {"link" : link}
    table.update(id, newdict)

def setstatus(id, code):
    newdict = {"status" : str(code)}
    table.update(id, newdict)

def getlink(hostid):
    result = table.all(formula=match({"hostid" : str(hostid)}))
    data = result[0]
    link = data['fields']['link']
    return(link)

#REGISTRATION COMMANDS
def newreg(reg, owner, brand, make, year, color, type, platestate, slot):
    regTable.create({"reg" : reg,
    "owner" : str(owner),
    "brand" : brand,
    "make" : make,
    "year" : year,
    "color" : color,
    "type" : type,
    "platestate" : platestate})

    newdict = {str(slot) : reg}
    cardid = table.all(formula=match({"userid" : str(owner)}))
    data = cardid[0]
    id = data['id']
    table.update(id, newdict)

def newUserData(userid):
    udTable.create({"userid" : str(userid),
    "carslots" : '0',
    "1" : "",
    "2" : "",
    "3" : "",
    "4" : "",
    "5" : "",
    "5" : ""})

def cASlots(userid):
    try:
        result = udTable.all(formula=match({"userid" : str(userid)}))
        data = result[0]
        slots = data['fields']['carslots']
        return(int(slots))
    except:
        newUserData(userid)
        result = udTable.all(formula=match({"userid" : str(userid)}))
        data = result[0]
        slots = data['fields']['carslots']
        return(int(slots))

def addSlot(userid, slots):
    newslots = slots + 1
    newdict = {"carslots" : newslots}
    cardid = table.all(formula=match({"userid" : str(userid)}))
    data = cardid[0]
    id = data['id']
    table.update(id, newdict)

def removeSlot(userid, slots):
    newslots = slots - 1
    newdict = {"carslots" : newslots}
    cardid = table.all(formula=match({"userid" : str(userid)}))
    data = cardid[0]
    id = data['id']
    table.update(id, newdict)