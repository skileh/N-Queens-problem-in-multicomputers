import socket, threading

def run(conn):
    while True:
        data = conn.recv(1024) # receber informacao
        if not data: # se o cliente tiver desligado
            conns.remove(conn)
            break
        for c in conns: # enviar mensagem para todos os outros clientes
            #if c is not conn: # excepto para o que a enviou 
                c.send(format(data.decode()).encode('utf-8'))

conns = set() # armazenar conxoes aqui
host, port = ('', 9940)
with socket.socket() as sock: # ligacao TCP
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # reutilizar endereco logo a seguir a fechar o servidor
    sock.bind((host, port))
    sock.listen(5) # servidor ativo
    print('Server started at {}:{}\n'.format(host, port))
    a=0
    while True:
        conn, addr = sock.accept() # esperar que alguem se conect
        a = a + 1
        conn.send(format(a).encode()) #avisa o numero do computador
        conns.add(conn) # adicionar conexao ao nosso set de coneccoes
        threading.Thread(target=run, args=(conn,)).start() # esta coneccao vai ser independente das outra a partir de agora, vamos correr a thread na funcao run
        print("isso é um teste")