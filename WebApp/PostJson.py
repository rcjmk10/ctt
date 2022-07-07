from codecs import latin_1_decode
import modulefinder
from flask import Flask, render_template, request, redirect, \
url_for, flash, make_response, session, jsonify
from flask import render_template
import json

template = 'INSERT INTO public.ctt_tickets(\nticket_id, \"TowerID\",\
\"TowerStreet\", \"ModuleID\", \"ErrorCode\", \"ErrorDetails\", \"ErrorDateTime\",\
\"AssignedUser_ID\", \"AssignedDateTime\", \"Ticket_Status\", \"CompletedDateTime\",\
\"Longitude\", \"Latitude\", geom)\nVALUES (gen_random_uuid(),\
\'{0}\', \'{1}\',\
\'{2}\', \'\', \'{3}\',\
\'{4}\', \'\', \'{4}\', \'0\',\
\'{4}\', \'{5}\', \'{6}\',\
\'POINT'+"({5} {6})"+'\' );'

def space_delimiter(Str, Select):
    '''
    returns either the portion of the string before the first " " in the string or everything after
    depending on Selector

    space_delimiter: Str, Str => Str
    '''
    str1 = ""
    str2 = ""
    bool = False
    for letter in Str:
        if bool == True:
            str2 = str2+letter
        elif letter == " ":
            bool = True
        else:
            str1 = str1+letter
    if Select == "Back":
        return str2
    elif Select == "Front":
        return str1
    else:
        return "Invalid Select in space_delimiter in ticket_parse.py"

def parsejson(filename_in):
    '''
    Turns json file from cell tower into sql insert command according to
    csv format from messages.csv

    parsejson: Str => None

    Effects:
        Reads in file
        Writes to file
    '''
    fin = open(filename_in, "r")
    #Message,Equipment,Tower,RegDate,TowerLatitude,TowerLongtitude
    ticket = json.loads(fin)
    insertcommand = ""
    towerid = space_delimiter(ticket["Tower"], "Front")
    towerstreet = space_delimiter(ticket["Tower"], "Back")
    moduleid = ticket["Equipment"]
    #errorcode = ""
    errordetails = ticket["Message"]
    errordatetime = ticket["RegDate"]
    #assigneduserid = ""
    #assigneddatetime = ticket["RegDate"]
    #ticketstatus = "0"
    #completeddatetime = ticket["RegDate"]
    long = ticket["TowerLongitude"]
    lat = ticket["TowerLatitude"]
    insertcommand = template.format(towerid, towerstreet, moduleid, errordetails, errordatetime, long, lat)
    fin.close()
    fout = open("D:\Actual program files lol\\repo\ctt\Webapp\\output\TicketInsert.txt", "w")
    fout.write(insertcommand)
    fout.close()
    return None
    