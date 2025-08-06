import socket
import threading

my_IP = socket.gethostname()
porta = 8080

clientes = []

def mensagem_cliente(mensagem, remetente):
    for cliente in clientes:
        if cliente != remetente:
            try:
                cliente.sendall(mensagem)
            except:
                cliente.close()
                if cliente in clientes:
                    clientes.remove(cliente)


def lado_cliente(conn, addr):
    print(f"Cliente conectado ao servidor: {addr}")
    clientes.append(conn)
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            
            print(f"Pessoa: {addr} falou -> {data.decode()}")
            mensagem_cliente(data, conn)
            # conn.sendall(data)
        except:
            break
    print(f'Cliente {addr} desconectado')
    conn.close()


servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((my_IP, porta))
servidor.listen()

print('Esperando conexão... ->')

while True:
    conn, addr = servidor.accept()
    thread = threading.Thread(target=lado_cliente, args=(conn, addr))
    thread.start()
    