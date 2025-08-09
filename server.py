import socket
import threading

ip_sever = socket.gethostname()
porta = 8080

clientes = []

def exibir_lista_comandos():
    return "\nLista de opções de comandos:\n/comandos - Lista comandos\n/close - Fecha conexão"


def encerrar_conexao():
    return "Conexão encerrada pelo servidor."

palavras_chaves_opcoes = {
    "/comandos": exibir_lista_comandos,
    "/": exibir_lista_comandos,
    "/close": encerrar_conexao,
}


def broadcast(msg, remetente):
    for cliente in clientes:
        if cliente != remetente:
            cliente.sendall(msg.encode())


def verificar_conexao(ip):
    for ip in clientes:
        if ip not in clientes:
            try:
                clientes.append(ip)
            except:
                print(f'o ip {ip}, já foi adicionado')


def menssagem_verificacao(msg, conn):
    if isinstance(msg, bytes):
        msg = msg.decode()
   
    msg = msg.strip()

    if msg == '' or msg.lower() == 'close':
        return False
    

    if msg.startswith('/'):
        if msg in palavras_chaves_opcoes:
            func = palavras_chaves_opcoes[msg]
            print(func)
            resp_func = func() # executa função. 
            conn.sendall(resp_func.encode())
        else:
            print('Comando não foi uma função do sistema!')
        return True
    
    conn.sendall(msg.encode())
    return True



def tratamento_cliente(conn, addr):
    print(f'\nUser : {addr} | Conectado')
    clientes.append(conn)
    while conn:
        try:
            menssagem = conn.recv(1024)
            if not menssagem:
                break

            continuar = menssagem_verificacao(menssagem, conn)
            if not continuar:
                break
            
            broadcast(menssagem.decode(), conn)
            
        except Exception as e:
            print(f'Erro no cliente {conn}: {e}')            
            conn.close()
            clientes.remove(conn)
            print(f"User {addr} desconectado.")
            break

def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((ip_sever, porta))
    servidor.listen()
    print('Esperando Clientes....')
    print(clientes)

    while True:
        conn, addr = servidor.accept()
        threads = threading.Thread(target=tratamento_cliente, args=(conn, addr))
        threads.start()


iniciar_servidor()