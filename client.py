import socket   
import threading

host = str(input("Enter ip from server: "))

username = input("Enter your username: ")


port = 55555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))


def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')

            if message == "@username":
                client.send(username.encode("utf-8"))
            else:
                print("\n", message,"\n")
        except:
            print("An error Ocurred")
            client.close
            break

def write_messages():
    while True:
        message = f"{username}: {input('')}\n"
        #message = input('')
        client.send(message.encode('utf-8'))

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

write_thread = threading.Thread(target=write_messages)
write_thread.start()