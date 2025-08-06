import socket
import threading

my_IP = socket.gethostname()
port = 8080


def receber_menssagens(cliente):
    while True:
        try:
            dados = cliente.recv(1024)
            print(f'\n{cliente}: {dados.decode()}')
        except:
            break



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((my_IP, port))
    threading.Thread(target=receber_menssagens, args=(s,), daemon=True).start()

    while True:
        menssage = input('\nEnive uma mensagem para o Chat: ')
        if not menssage or menssage == 'close':
            break
        s.sendall(menssage.encode())
        print(f'\nMenssagem do servidor: {s.recv(1024)}')
        
    s.close()

