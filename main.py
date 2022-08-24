import socket
import select


class Server:
    def __init__(self):
        self.Type_encode = "utf-8"
        self.Header_length = 20
        self.Host = "192.168.1.3"
        self.Port = 78
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.Host, self.Port))
        self.server_socket.listen()
        self.sockets_list = [self.server_socket]
        self.clients = {}
        self.Message_Board = []

    def receive_message(self, client_socket):
        message_header = client_socket.recv(self.Header_length)
        if not len(message_header):
            return False
        message_length = int(message_header.decode(self.Type_encode))
        return {"header": message_header, "data": client_socket.recv(message_length)}

    def Main(self):
        while True:
            read_sockets, _, exception_sockets = select.select(self.sockets_list, [], self.sockets_list)
            for notified_socket in read_sockets:
                if notified_socket == self.server_socket:
                    client_socket, client_address = self.server_socket.accept()
                    user = self.receive_message(client_socket)
                    if user is False:
                        continue
                    self.sockets_list.append(client_socket)
                    self.clients[client_socket] = user
                    print(
                        f"Accepted New connection From {client_address[0]}:{client_address[1]} Username:{user['data'].decode(self.Type_encode)}")
                else:
                    message = self.receive_message(notified_socket)
                    if message is False:
                        print(
                            f"Close connection from {self.clients[notified_socket]['data'].decode(self.Type_encode)}!")
                        self.sockets_list.remove(notified_socket)
                        del self.clients[notified_socket]
                        continue

                    user = self.clients[notified_socket]
                    self.Message_Board.append({f"{user['data'].decode(self.Type_encode)}":f"{message['data'].decode(self.Type_encode)}"})
                    print(
                        f"Received Message from {user['data'].decode(self.Type_encode)} : {message['data'].decode(self.Type_encode)}")
                    for client_socket in self.clients:
                        if client_socket != notified_socket:
                            client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])


Server().Main()
# -----------------------------------------------------------------------------------------------------------------------


# protocol = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# protocol.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# protocol.bind((socket.gethostname(), 78))
# protocol.listen()
# socket_list = [protocol]
# clients = {}
#
#
# def receive_message(client_socket, HEADER_LENGTH=None):
#     try:
#         message_header = client_socket.recv(HEADER_LENGTH)
#         if not len(message_header):
#             return False
#         message_length = int(message_header.decode('utf-8'))
#         return {"header": message_header, "data": client_socket.recv(message_length)}
#     except:
#         return False
#
#
# while True:
#     read_sockets, _, exception_socket = select.select(socket_list, [], socket_list)
#     for notified_socket in read_sockets:
#         if notified_socket == protocol:
#             client_socket, client_address = protocol.accept()
#             user = receive_message(client_socket)
#             if user is False:
#                 continue
#             socket_list.append(client_socket)
#             clients[client_socket] = user
#             username = user['data'].decode('utf-8')
#             print(f"Accepted New Connection! form {client_address[0]} Username:{username}")
#         else:
#             message = receive_message(notified_socket)
#             if message is False:
#                 print(f"Closed connection from {clients[notified_socket]}")
#                 socket_list.remove(notified_socket)
#                 del clients[notified_socket]
#                 continue
#             user = clients[notified_socket]
#             print(f'Received Message form {user["data"].decode("utf-8")}')
#             for client_socket in clients:
#                 if client_socket != notified_socket:
#                     client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
#     for notified_socket in exception_socket:
#         socket_list.remove(notified_socket)
#         del clients[notified_socket]
