import socket
import threading

def receber_mensagem(conexao_servidor):
    while True:
        try:
            dados = conexao_servidor.recv(1024)
            print(f'\nMenssagem: {dados.decode()}')
        except:
            print('Error: Mensagem não recebida!')
            break

def iniciar_conexao():
    ip_cliente = socket.gethostname()
    porta = 8080

    conexao_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conexao_servidor.connect((ip_cliente, porta))
    
    thread = threading.Thread(target=receber_mensagem, args=(conexao_servidor,))
    thread.start()

    while True:
        messagem = input('\nDigite a Mensagem: ')
        conexao_servidor.sendall(messagem.encode())

iniciar_conexao()