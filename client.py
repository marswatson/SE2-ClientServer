#client server
from socket import *
import struct
import fileinput

#client information
HOST = 'localhost'
PORT = 5230
BUF_SIZE = 2048
ADDR = (HOST, PORT)
TcpCliSock = socket(AF_INET, SOCK_STREAM)
TcpCliSock.connect(ADDR)
FILEINFO_SIZE=struct.calcsize('128s32sI8s')

while 1:
    data = raw_input('>')#input data
    if not data:
        break
    data_type = data.split(':')
    #select correct input format
    if data_type[0] != 'GET' and data_type[0] != 'BOUNCE'and data_type[0] != 'EXIT':
        print 'You must input the standard command!'
        continue
    #send command
    TcpCliSock.send(data)
    if data_type[0]=='EXIT':
        break
    #receive file
    if data_type[0]=='GET':
        FILEINFO_SIZE=struct.calcsize('128s32sI8s')
        fhead = TcpCliSock.recv(FILEINFO_SIZE)
        filename,temp1,filesize,temp2=struct.unpack('128s32sI8s',fhead)
        print filename,len(filename),type(filename)
        print filesize
        filename = 'new_'+filename.strip('\00') #...
        fp = open(filename,'wb')
        restsize = filesize
        print "Receiving file... ",
        while 1:
            if restsize > BUF_SIZE:
                filedata = TcpCliSock.recv(BUF_SIZE)
            else:
                filedata = TcpCliSock.recv(restsize)
            if not filedata: break
            fp.write(filedata)
            restsize = restsize-len(filedata)
            if restsize == 0:
             break
        print "Received file..."
        print "Display file:"
        fp.close()
        #display file
        for line in fileinput.input(filename):
            print line,
        restsize = filesize
    #Bounce operation
    else:
        if data_type[0] == 'BOUNCE':
            data_rec = TcpCliSock.recv(BUF_SIZE)
            print data_rec
TcpCliSock.close()