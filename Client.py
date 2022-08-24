import socket
import select
import errno
import sys
import threading

Header_Length=20

class Client_:
    def __init__(self):
        self.Host='192.168.1.3'
        self.Port=78
        self.encode_Type="utf-8"
        self.Username=input("Username: ").encode(self.encode_Type)
        self.Username_Header=f"{len(self.Username):<{Header_Length}}".encode(self.encode_Type)
        self.Client_Socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.Client_Socket.connect((self.Host,self.Port))
        self.Client_Socket.setblocking(False)
        self.Client_Socket.send(self.Username_Header+self.Username)


    def Main(self):
        while True:
            message=input("Messages: ")
            if message:
                try:
                    username_header = self.Client_Socket.recv(Header_Length)
                    if not len(self.Username_Header):
                        print("connection Closed by the server!")
                        sys.exit()
                    username_length = int(username_header.decode(self.encode_Type).strip())
                    username = self.Client_Socket.recv(username_length).decode(self.encode_Type)
                    message_header = self.Client_Socket.recv(Header_Length)
                    message_length = int(message_header.decode(self.encode_Type).strip())
                    message = self.Client_Socket.recv(message_length).decode(self.encode_Type)
                    print(f"{username}>{message}")
                except:pass
                #--------------------------------------------------------------------------------------------
                message=message.encode(self.encode_Type)
                message_header=f"{len(message):<{Header_Length}}".encode(self.encode_Type)
                self.Client_Socket.send(message_header+message)
            try:
                while True:
                    username_header=self.Client_Socket.recv(Header_Length)
                    if not len(self.Username_Header):
                        print("connection Closed by the server!")
                        sys.exit()
                    username_length=int(username_header.decode(self.encode_Type).strip())
                    username = self.Client_Socket.recv(username_length).decode(self.encode_Type)

                    message_header=self.Client_Socket.recv(Header_Length)
                    message_length=int(message_header.decode(self.encode_Type).strip())
                    message=self.Client_Socket.recv(message_length).decode(self.encode_Type)
                    print(f"{username}>{message }")
                    continue
            except IOError as e:
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print("Error Reading error:"+ str(e))
                    sys. exit()
            except Exception as e:
                print("General Error: "+str(e))
                sys.exit()
Client_().Main()