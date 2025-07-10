import socket
import threading
import pickle

clients = []
def handle_client(client_socket):
    while 1:
        try:
            msg = client_socket.recv(1024)
            if not msg:
                break
            for cl in clients:
                if cl != client_socket:
                    cl.send(msg)
            print(msg.decode())
        except:
            break

    client_socket.close()
    clients.remove(client_socket)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 12345))
server.listen()
print("Server execute")

while 1:
    client_socket, addr = server.accept()
    clients.append(client_socket)
    threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()
    print(f"{addr}")