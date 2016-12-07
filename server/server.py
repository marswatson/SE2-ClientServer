#!usr/bin/python
#server program
from socket import *
import os
import struct

#set host and port to create a socket in server
HOST = 'localhost'
PORT = 5230
BUF_SIZE = 2048
ADDR = (HOST, PORT)
TcpSerSock = socket(AF_INET, SOCK_STREAM)
TcpSerSock.bind(ADDR)
TcpSerSock.listen(2)
FILEINFO_SIZE=struct.calcsize('128s32sI8s')
while 1:
    #connect to the client
    print 'Waiting for connection...'
    TcpCliSock, addr = TcpSerSock.accept()
    print '...Connect from:', addr

    while 1:
        data = TcpCliSock.recv(BUF_SIZE)
        if not data:
            break
        data_type = data.split(':')
        send_information = ''
        #three standard command
        #GET request
        if data_type[0]=='GET':
            #print 'get'
            #data_type[1] = 'F:\\Notes\\Rutgers\\2016_spring\\SE2\\HW6\\server\\' + data_type[1]
            if os.path.isfile(data_type[1]):
                print data
                fhead=struct.pack('128s11I',data_type[1],0,0,0,0,0,0,0,0,os.stat(data_type[1]).st_size,0,0)
                TcpCliSock.send(fhead)
                fp = open(data_type[1],'rb')
                while 1:
                    filedata = fp.read(BUF_SIZE)
                    print filedata
                    if not filedata: break
                    TcpCliSock.send(filedata)
                print "Files have already send..."
                fp.close()
            else:
                print("no such file\n")
                TcpCliSock.send("ERROR: no such file\n")
        #BOUNCE request
        else:
            if data_type[0]=='BOUNCE':
                print data
                if len(data_type)>1:
                    print data_type[1]
                    TcpCliSock.send('%s'%data_type[1])
                else:
                    TcpCliSock.send('You must input standard request')
            #EXIT request
            else:
                if data_type[0]== 'EXIT':
                    if len(data_type) == 1:
                        print 'Normal Exit'
                    else:
                        print data_type[1]
    TcpCliSock.close()
TcpSerSock.close()