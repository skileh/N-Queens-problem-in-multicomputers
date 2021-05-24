import socket, threading, pickle

a=1
def run(conn, a, saidas,computer):
    total_solution = 0
    verif_1_entrada = True #primeira entrada na thread
    while computer==1: #somente a thread mestre.
        #aux = a
        if(verif_1_entrada): #verifica se é a primeira vez que entra na thread mestre
            data = conn.recv(1024) # receber informacao
            verif_1_entrada = False
            saidas[a-1]=False
        if(a<=4):
            if not data: # se o cliente tiver desligado
                conns.remove(conn)
                break
            for c in conns: # enviar mensagem para todos os outros clientes
                data_a = (format(a).encode(),format(data.decode()).encode('utf-8'))
                data_string = pickle.dumps(data_a)
                c.send(data_string)
                a = a + 1
            for c in conns:
                solution = c.recv(1024) #espera a solucao parcial
                if not solution: # se o cliente tiver desligado
                    conns.remove(c)
                    break
                total_solution += int(solution)
        elif(a>4): #caso já tenha finalizado todas 4 etapas
            verif_1_entrada = True 
            a=1
            print("Quantidade de soluções encontradas: ", total_solution)

            data_a = (format(a).encode(),format(data.decode()).encode('utf-8'),format(total_solution).encode())
            data_string = pickle.dumps(data_a)
            total_solution=0
            c.send(data_string) #envia ao servidor o resultado encontrado
    

conns = set() # armazenar conxoes aqui
host, port = ('', 9940)
with socket.socket() as sock: # ligacao TCP
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # reutilizar endereco logo a seguir a fechar o servidor
    sock.bind((host, port))
    sock.listen(5) # servidor ativo
    print('Server started at {}:{}\n'.format(host, port))
    saidas=[True,True,True,True]
    computer=0
    while True:
        conn, addr = sock.accept() # esperar que alguem se conect
        print('\nCOMPUTER {} CONECTED'.format(addr).encode())
        data_a = [a]
        computer+=1
        if(computer==1):
            conn.send(format(computer).encode()) #avisa o numero do computador
        else:
            conn.send(format(0).encode())
        data_string = pickle.dumps(data_a)
        conns.add(conn) # adicionar conexao ao nosso set de coneccoes
        threading.Thread(target=run, args=(conn,a,saidas,computer)).start() # esta coneccao vai ser independente das outra a partir de agora, vamos correr a thread na funcao run
       # print("isso é um teste")