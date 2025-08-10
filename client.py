import socket
import threading
import time

conctado_no_servidor = True

def receber_mensagem(conexao_servidor):
    global conctado_no_servidor
    while conctado_no_servidor:
        try:
            dados = conexao_servidor.recv(1024)
            if not dados:
                print("Servidor encerrou a conexão.")
                conctado_no_servidor = False
                break

            dados_decotificacao = dados.decode()

            if dados_decotificacao == 'ENCERRAR_CONEXÃO':
                print("Servidor solicitou encerramento da conexão.")
                conexao_servidor.close()
                conctado_no_servidor = False
                break
            else:
                print(f'\nMenssagem: {dados.decode()}')
        except:
            print('Error: Mensagem não recebida!')
            conctado_no_servidor = False
            break

def iniciar_conexao():
    ip_cliente = socket.gethostname()
    porta = 8080

    conexao_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conexao_servidor.connect((ip_cliente, porta))
    
    thread = threading.Thread(target=receber_mensagem, args=(conexao_servidor,))
    thread.start()

    global conctado_no_servidor
    while conctado_no_servidor:
        time.sleep(1)
        try:
            messagem = input('\nDigite a Mensagem: ')
            conexao_servidor.sendall(messagem.encode())
        except Exception as e:
            print(f'Erro ao enviar mensagem : {e}')
            conctado_no_servidor = False
            break
        
iniciar_conexao()