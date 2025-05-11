import socket
import threading

HOST = '0.0.0.0'
PORT = 1238

# Create a socket object (IPv4 + TCP)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the server to the specified address and port
server.bind((HOST, PORT))

# Listen for incoming connections (maximum of 5 clients in queue)
server.listen(5)

clients = []

# Broadcast message to all clients
def broadcast_message(message):
    for client in clients:
        try:
            client.sendall(message.encode('utf-8'))
        except:
            clients.remove(client)

# Handle communication with each client
def handle_client(client_socket, addr):
    print(f"New connection from {addr}")
    username = client_socket.recv(1024).decode('utf-8')
    print(f"Username received: {username}")

    # Notify others that a new user has joined
    broadcast_message(f"[SERVER] {username} has joined the chat! We hope you brought pizza.")

    while True:
        try:
            message = client_socket.recv(2048).decode('utf-8')
            if message:
                # Broadcast the message to all clients
                formatted_message = f"[{username}] {message}"
                print(formatted_message)
                broadcast_message(formatted_message)
            else:
                break
        except:
            break

    # Remove client on disconnection
    clients.remove(client_socket)
    client_socket.close()
    broadcast_message(f"[SERVER] {username} has left the chat! Maybe they'll come back?")

# Accept incoming client connections
print(f"Server started on {HOST}:{PORT}")

while True:
    client_socket, addr = server.accept()
    clients.append(client_socket)
    threading.Thread(target=handle_client, args=(client_socket, addr)).start()
