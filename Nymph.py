# -*- coding: utf-8 -*-
import socket
import struct
from threading import Thread ,Event
import signal



class nymphdata(object): #balant bilgilerini tutan snf
    def __init__(self,NAME,HOST='',PORT=8089):
        self.NAME=NAME
        self.HOST=HOST
        self.PORT=PORT


class DataLineProtocol(object): #bir yazının aktarımından sorumlu sınıf

    def __init__(self,conn):
        self.CONN=conn

    def send(self,data):
        dataLength=len(data)
        self.CONN.sendall(struct.pack("!I",dataLength))
        self.CONN.sendall(data)

    def recv(self):
        lengthData=""
        count=4
        while count:
            coming=self.CONN.recv(1)
            lengthData += coming
            count -= len(coming)
        dataLength=struct.unpack("!I",lengthData)
        dataLength=dataLength[0]
        data=""
        while dataLength:
            coming=self.CONN.recv(dataLength)
            data += coming
            dataLength -= len(coming)

        return data


class nymph(object): # server ve client özellikleri olan node sınıfı
    nTc=[]
    error=""
    def __init__(self,nymphData):
        self.myN=nymphData
        self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.bind(('',self.myN.PORT))
        self.s.listen(1)
        print('start...')
        self.nT=Thread(target = self.server )
        self.nT.start()
        signal.signal(signal.SIGINT, self.signal_handler)
        self.otN=None
        self.otN_s=None


    def server(self):
        while 1:
            #print ('wait for client')
            conn, addr = self.s.accept()
            #print 'Connected by', addr
            self.newThread(conn,addr) #her bağlantı yeni bir threade aktarılarak serverın müsait olması sağlanır


    def newThread(self,conn,addr):
        thready=Thread(target = self.acceptConns ,args = (conn,addr))
        self.nTc.append(thready)
        thready.start()


    def acceptConns(self,c,a): # bağlantıların işlendiği fonksiyon
        while 1:
            DLP=DataLineProtocol(c)
            words=DLP.recv()
            self.listen(words)

    def listen(self,words):#listen bir procedure
        print(words)

    def talkWith(self,nymphData): # hangi node un clientı olarak davranacağını belirler
        self.otN=nymphData
        if self.otN_s!=None:
            self.otN_s.close()
        self.otN_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if(0==self.otN_s.connect_ex((self.otN.HOST, self.otN.PORT))):
            pass #self.otN_s.connect((self.otN.HOST, self.otN.PORT))
        else:
            self.error="offline node"
            print("offline node")
            self.otN=None
        return self

    def say(self,word): # server node a veri gönderir
        if(self.otN!=None):
            otDLP=DataLineProtocol(self.otN_s)
            otDLP.send(self.sayFormat(word))
        else:
            self.error="node not connect with anynode"
            print("node not connect with anynode")

    def sayFormat(self,words):
        return words
    
    def signal_handler(self, signal, frame):
        import os
        print '\nGood bye mortal :)'
        self.__del__()
        pid = os.getpid()
        os.kill(pid,1)

    def __del__(self):
        #self.s.shutdown(socket.SHUT_RDWR)
        self.s.close()
        for thread in self.nTc:
            thread.exit()
        #self.nT.exit()