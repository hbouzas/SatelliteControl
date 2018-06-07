# READ DATA COMING FROM MACDOPPLER VIA UDP
import socket
import requests
import urllib2
import httplib
import sys
from time import sleep

def changeSatellite(url_str):
   try:
      response = urllib2.urlopen(url_str)
      print url_str
      if response:
         html = response.read()
         print "Changing satellite ",name, " Azi: ", azi,  " Ele: ", ele
         return 1
   except urllib2.URLError as e:
      print("URLError. Error changing satellite on Autonomic Control, trying again... " )
      print(e.reason)
      return 0
   except urllib2.HTTPError as e:
      print("HTTPError. Error changing satellite on Autonomic Control, trying again... " )
      print(e.reason)
      return 0
   except httplib.BadStatusLine as e:
      print("BadStatusLine. Error changing satellite on Autonomic Control, trying again... " )
      print(e.reason)
      return 0
   except Exception:
      print("Unknown error. Error changing satellite on Autonomic Control, trying again... " )
      return 0
 

def set_name(old_name):
   new_name = 'moon'
   if old_name == 'AO-07':
      new_name = 'ao07'
   if old_name == 'AO-73':
      new_name = 'ao73'
   if old_name == 'AO-85':
      new_name = 'ao85'
   if old_name == 'AO-91':
      new_name = 'ao91'
   if old_name == 'AO-92':
      new_name = 'ao92'
   if old_name == 'CUBEBUG':
      new_name = 'cubebug-1'
   if old_name == 'CO-57':
      new_name = 'co57'
   if old_name == 'CO-55':
      new_name = 'co55'
   if old_name == 'EO-79':
      new_name = 'eo79'
   if old_name == 'EO-88':
      new_name = 'eo88'
   if old_name == 'FO-29':
      new_name = 'fo29'
   if old_name == 'LILACSAT-2':
      new_name = 'lilacsat-2'
   if old_name == 'NO-84':
      new_name = 'no84'
   if old_name == 'SO-50':
      new_name = 'so50'
   if old_name == 'TechnoSat':
      new_name = 'technosat'
   if old_name == 'UKUBE-1':
      new_name = 'ukube-1'
   if old_name == 'XW-2A':
      new_name = 'xw2a'
   if old_name == 'XW-2B':
      new_name = 'xw2b'
   if old_name == 'XW-2C':
      new_name = 'xw2c'
   if old_name == 'XW-2D':
      new_name = 'xw2d'
   if old_name == 'CAS-4A':
      new_name = 'cas4a'
   if old_name == 'CAS-4B':
      new_name = 'cas4b'
   if old_name == 'XW-2F':
      new_name = 'xw2f'
   if old_name == 'ISS':
      new_name = 'iss'
   return new_name

# Radio communication
host = '192.168.0.29'  #radio host name
port = 4992            # radio port
sat_cont_host = "192.168.0.119"
sat_cont_port = 9999
sat_socket = None

try:
    TCPsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPsocket.setblocking(1)
    TCPsocket.settimeout(5)
    TCPsocket.connect((host, port))
except socket.error, e:
    print '*** Connection to transceiver refused, continuing without it ***'

reading = True
curr_sat = ""
flex_msg_ind = 1
freq_set = 0
dfreq_last=''
dmode_last=''
ufreq_last=''
umode_last=''
sname_last=''
while reading == True:
   try:
      data = TCPsocket.recv(1024*4)
      print('Received', repr(data))
      data = TCPsocket.recv(1024*4)
      print('Received', repr(data))
      data = TCPsocket.recv(1024*4)
      print('Received', repr(data))
      data = TCPsocket.recv(1024*4)
      print('Received', repr(data))
      data = TCPsocket.recv(1024*4)
      print('Received', repr(data))
   except socket.error as msg:
      print msg
      print "done"
      reading = False

print "done"
# A UDP server
# Set up a UDP server
#MacDoppler communication
UDPSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# Listen on port 21567
# (to all IP addresses on this system)
listen_addr = ("",9932)
UDPSock.bind(listen_addr)
reading = True
print "reading"
# Report on all data packets received and
# where they came from in each case (as this is
# UDP, each may be from a different source and it's
# up to the server to sort this out!)
while reading == True:
#   data_xvr = TCPsocket.recv(8192)
#   print('Received from transceiver', repr(data_xvr))
# C1|slice t 3 145.222
   data,addr = UDPSock.recvfrom(1024)
   response = data.strip()
   indx_radio = response.find("Sat Radio Report",0)
   indx_rotor = response.find("AzEl Rotor Report",0)
   if (indx_radio != -1):  #process radio message
#      print "Found radio message"
      indx_dfreq = response.find("Down Mhz:",indx_radio)
      indx_dfreq_beg = indx_dfreq+9
      indx_dfreq_end = response.find(",",indx_dfreq_beg)
      indx_dmode = response.find("Down Mode:",indx_radio)
      indx_dmode_beg = indx_dmode+10
      indx_dmode_end = response.find(",",indx_dmode_beg)
      indx_ufreq = response.find("Up MHz:",indx_radio)
      indx_ufreq_beg = indx_ufreq+7
      indx_ufreq_end = response.find(",",indx_ufreq_beg)
      indx_umode = response.find("Up Mode:",indx_radio)
      indx_umode_beg = indx_umode+8
      indx_umode_end = response.find(",",indx_umode_beg)
      indx_tone = response.find("tone:",indx_radio)
      indx_tone_beg = indx_tone+5
      indx_tone_end = response.find(",",indx_tone_beg)
      indx_ctone = response.find("ctone:",indx_radio)
      indx_ctone_beg = indx_ctone+6
      indx_ctone_end = response.find(",",indx_ctone_beg)
      indx_sname = response.find("SatName:",indx_radio)
      indx_sname_beg = indx_sname+8
      indx_sname_end = response.find("]",indx_sname_beg)
      dfreq = response[indx_dfreq_beg:indx_dfreq_end]
      dmode = response[indx_dmode_beg:indx_dmode_end]
      ufreq = response[indx_ufreq_beg:indx_ufreq_end]
      umode = response[indx_umode_beg:indx_umode_end]
      tone = response[indx_tone_beg:indx_tone_end]
      ctone = response[indx_ctone_beg:indx_ctone_end]
      sname = response[indx_sname_beg:indx_sname_end]
      sname = set_name(sname)

#      print "Processing Xver Dlink: ",dfreq, " Dmode: ", dmode,  " Ulink: ", ufreq, " Umode: ",umode, " Tone: ", tone, " CTone: ", ctone,  " Satellite: ", sname
      if sname_last != sname:
          print( "Processing Xver Dlink: " + dfreq + " Dmode: " + dmode +  " Ulink: " + ufreq + " Umode: " + umode + " Tone: " + tone + " CTone: " + ctone +  " Satellite: " + sname)
          sname_last = sname
# update the transceiver dlink freq only first time through, slice A
          flex_str_d = b'C' + str(flex_msg_ind) + '|slice t 0 ' + dfreq + '\n'
#         print flex_str_d
          try:
             TCPsocket.sendall(flex_str_d)
             flex_msg_ind = flex_msg_ind+1
             flex_str_d = b'C' + str(flex_msg_ind) + '|slice s 0 active=1 mode=' + dmode + '\n'
#         print flex_str_d
             TCPsocket.sendall(flex_str_d)
#        TCPsocket.sendall(flex_str_d)
             flex_msg_ind = flex_msg_ind+1

# update the transceiver ulink freq only first time through, slice B
             flex_str_u = b'C' + str(flex_msg_ind) + '|slice t 1 ' + ufreq + '\n'
#         print flex_str_d
             TCPsocket.sendall(flex_str_u)
             flex_msg_ind = flex_msg_ind+1
             flex_str_u = b'C' + str(flex_msg_ind) + '|slice s 1 active=1 mode=' + umode + '\n'
#         print flex_str_d
             TCPsocket.sendall(flex_str_u)
#        TCPsocket.sendall(flex_str_d)
             flex_msg_ind = flex_msg_ind+1

#      TCPsocket.sendall(b'C1|slice t 0 145.330')
#      C21|slice create 10.0 ANT1 usb
          except socket.error, e:
             print '*** Cannot communicate with transceiver, skipping update ***'

# UPDATE THE  xverter
          if float(dfreq) < 200.000 and float(ufreq) < 200.00:
             url_str = "http://184.64.129.192:81/vhf"
          elif float(dfreq) < 200.000 and float(ufreq) > 200.00:
             url_str = "http://184.64.129.192:81/vuf"
          elif float(dfreq) > 200.000 and float(ufreq) < 200.00:
             url_str = "http://184.64.129.192:81/uvf"
          elif float(dfreq) > 200.000 and float(ufreq) > 200.00:
             url_str = "http://184.64.129.192:81/uhf"
          try:
             response = urllib2.urlopen(url_str)
             if response:
                html = response.read()
                print "Trasnverter control changed ", url_str
          except urllib2.URLError as e:
             print("URLError connecting to Trasnverter Control ")
             print(e.reason)
          except urllib2.HTTPError as e:
             print("HTTPError connecting to Trasnverter Control ")
             print(e.reason)
          except httplib.BadStatusLine as e:
             print("BadStatusLine connecting to Trasnverter Control ")
             print(e.reason)
          except Exception:
             print("Unknown error. Error changing satellite on Autonomic Control, trying again... " )
             print(e.reason)

# UPDATE THE preamplifier
          if float(dfreq) < 200.000 :
             url_str = "http://184.64.129.192:82/vhf"
          elif float(dfreq) > 200.000 :
             url_str = "http://184.64.129.192:82/uhf"
          try:
             response = urllib2.urlopen(url_str)
             if response:
                html = response.read()
                print "Pre-amplifier control changed ", url_str
          except urllib2.URLError as e:
             print("URLError connecting to Pre-amplifier Control ")
             print(e.reason)
          except urllib2.HTTPError as e:
             print("HTTPError connecting to Pre-amplifier Control ")
             print(e.reason)
          except httplib.BadStatusLine as e:
             print("BadStatusLine connecting to Pre-amplifier Control ")
             print(e.reason)
          except Exception:
             print("Unknown error. Error changing satellite on Autonomic Control, trying again... " )
             print(e.reason)

   if (indx_rotor != -1):  #process roto message
      indx_azi = response.find("Azimuth:",indx_rotor)
      indx_azi_beg = indx_azi+8
      indx_azi_end = response.find(",",indx_azi_beg)
      indx_ele = response.find("Elevation:",indx_rotor)
      indx_ele_beg = indx_ele+10
      indx_ele_end = response.find(",",indx_ele_beg)
      indx_name = response.find("SatName:",indx_rotor)
      indx_name_beg = indx_name+8
      indx_name_end = response.find("]",indx_name_beg)
      azi = response[indx_azi_beg:indx_azi_end]
      ele = response[indx_ele_beg:indx_ele_end]
      name = response[indx_name_beg:indx_name_end]
      name = set_name(name)

#      changeSatellite(url_str, success):
      success = 0
      if curr_sat != name:
         sleep_time = 1
         fcount = 1
         while success == 0:
            if sleep_time == 1 and fcount < 20:
               curr_sat = name
               url_str = "http://" + sat_cont_host + ":" + str (sat_cont_port) + "/?name=" + name + '&lat=51&lon=-114&ele=1050'
               success = changeSatellite(url_str)
               if success == 0:
                  print("Failed to change to satellite " + name + " attempt " + str(fcount))
               elif success == 1:
                  print("Successfully changed satellite, now following " + name)
               fcount = fcount + 1
               sleep(sleep_time)
            elif fcount == 20:
               sleep_time = 20
               print "Too many failed attempts to change satellite, taking a break..."
               sleep(sleep_time)
               sleep_time = 1
               fcount = 1
   

