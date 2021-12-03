import socket   
import threading


host = '0.0.0.0'
port = 55555

fmt = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))
server.listen()
print(f"Server running on {host}:{port}")


clients = []
usernames = []

el_user = []

def broadcast(message, _client):
    mensage = message.decode(fmt)
    
    if mensage.__contains__('@bot-'):
        _client.send("Chatbot: hola soy un chatbot".encode("utf-8"))
   
    if mensage.__contains__('@user'):
        sears = mensage.remplase('@user ', "")
        for eso in el_user :
          if eso.__contains__(sears):
             print(eso[sears])
        
        _client.send("Chatbot: hola soy un chatbot".encode("utf-8"))
    
    elif mensage.__contains__('@bot help'):
        _client.send("Chatbot: hola soy un chatbot pero todavía solo tengo un comando".encode("utf-8"))
        
    elif mensage.__contains__('@server users'):
        _client.send(f"[SERVER] Estos son los usuarios:\n {usernames}".encode("utf-8"))
     
    elif mensage.__contains__('@server clients'):
        _client.send(f"[SERVER] Estos son los clientes:\n {clients}".encode("utf-8"))
     
    elif mensage.__contains__('@server client'):
        _client.send(f"[SERVER] Estos son los clientes:\n {clients[0]}".encode("utf-8"))
     
    else:
      for client in clients:
        print('el cliente', client)
        if client != _client:
            client.send(message)
            print('memsage enviado', client, 'lo otro', _client)

def handle_messages(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message, client)
           
            print('mensage', message.decode(fmt), 'client', client)
        except:
            index = clients.index(client)
            username = usernames[index]
            broadcast(f"ChatBot: {username} disconnected".encode('utf-8'), client)
            clients.remove(client)
            usernames.remove(username)
            client.close()
            break


def receive_connections():
    while True:
        client, address = server.accept()

        client.send("@username".encode("utf-8"))
        username = client.recv(1024).decode('utf-8')
        
        print('el_username', username)
        
        los_users = { username : client}
        
        el_user.append(los_users)
        
        clients.append(client)
        usernames.append(username)

        print(f"{username} is connected with {str(address)}")

        message = f"ChatBot: {username} joined the chat!".encode("utf-8")
        broadcast(message, client)
        client.send("Connected to server".encode("utf-8"))

        thread = threading.Thread(target=handle_messages, args=(client,))
        thread.start()

receive_connections()

