from __future__ import print_function
import requests
import time
import subprocess
import os
import datetime
import RPi.GPIO as GPIO
import DHT11_Python.dht11 as dht11
import mysql.connector as mysqli
from mysql.connector import errorcode
import json
import urllib.request

config = {
    'user': 'root',
    'password': 'ffuswgwy',
    'host': '127.0.0.1',
    'database':'hydropony'
    }

#cnx = mysqli.connect(**config)


DELAY = 2
TOKEN = "467860725:AAGCBLz3X-Zi33WQQ-g40obk_27JZHk2JRQ"
URL="https://api.telegram.org/bot"
FURL = " https://api.telegram.org/file/bot" 
ADMIN_ID = 89813737
offset = 0

def check_updates():
 
  global offset
  data = {'offset':offset+1,'limit':5,'timeout':0}

  try:
    request = requests.post(URL+TOKEN+'/getUpdates',data=data)
  except:
    log_event('Error getting updates')
    return False
  if not request.status_code == 200: return False
  if not request.json()['ok'] : return False
  for update in request.json()['result']:
    offset = update['update_id']
   
    #print(request.json())

    #if not 'message' in update or not 'text' in update['message']:
    #  log_event('Uncnown update : %s' % update)
    #  continue
    
    from_id = update['message']['chat']['id']
    name = update['message']['chat']['username']
    firstname = update['message']['chat']['first_name']

    if from_id != ADMIN_ID:
        send_text("You are not autorized to use me!",from_id)
        log_event('Unautorized : %s' % update)
        continue
    
    if 'text' in update['message']:
        message = update['message']['text']
    else:
        message = 'no message'
    parameters = (offset,name,from_id,message,firstname,update)  
    log_event('Message (id%s) from %s (id%s): "%s%s" %s ' % parameters)

    run_command(*parameters)

def run_command(offset,name,from_id,cmd,fname,req):
    print(req,"\n")
    #print((req['message']['document'] ==  None),"\n")
    
    #send_text(from_id,cmd)
    #update = req.json()['result']
    if cmd=='/start':
        send_text(from_id,fname+" You're an Petia")
    elif cmd=='/state':
        #send_text(from_id,"Привет!!!")
        state = ("SELECT * FROM hydrostats WHERE 1 ORDER BY id DESC")
        cnx = mysqli.connect(user='root', password='ffuswgwy',database='hydropony',host='127.0.0.1')
        cursor = cnx.cursor()
        cursor.execute(state)
        row = cursor.fetchone()

        if row is not None:

            send_text(from_id,"%s \nТемпература=%0.1f \nВлажность=%0.1f \nСвет=%d \nУвлажнитель=%d" % (row[1].isoformat(),row[2],row[3],row[4],row[5]))

        #cursor.close()
        cnx.close()
    elif cmd=="/test":
        send_text(from_id,"%s LOX" % (fname))
    elif 'document' in req['message']:
        send_text(from_id,'you send a document')
        link = getDocumentLink(req['message']['document']['file_id'])
        downloadDocument(link)
    elif 'photo' in req['message']:
        send_text(from_id,'you send a photo')
        try:
            photocnt = len(req['message']['photo'])
        except:
            photocnt = 0
        link = getDocumentLink(req['message']['photo'][photocnt-1]['file_id'])
        downloadDocument(link)
 
def downloadDocument(link):
    path = FURL+TOKEN+'/'+link.json()['result']['file_path']
    print(path+'\n\n')
    #print(link.json()+'\n\n')
    f = urllib.request.urlopen(path).read()
    fl = open('/var/www/html/'+link.json()['result']['file_path'],'wb')
    fl.write(f)
    fl.close()

def getDocumentLink(file_id):
    data = {'file_id' : file_id}
    try:
        request = requests.post(URL+TOKEN+'/getFile',data=data)
    except:
        log_event('Error getting updates')
        return False
    if not request.status_code == 200: return False
    if not request.json()['ok'] : return False
    return request

def send_text(chat_id,text):
  log_event('Sending to %s: %s' % (chat_id, text))
  data = {'chat_id': chat_id, 'text': text} 
  request = requests.post(URL + TOKEN + '/sendMessage', data=data)
  if not request.status_code == 200: 
      return False 
  return request.json()['ok'] 

def log_event(text):
    event = '%s >> %s' % (time.ctime(), text)
    #print(event)


while True:
      try:
          check_updates()
          time.sleep(DELAY)
      except KeyboardInterrupt:
          print('Прервано пользователем..')
          break
