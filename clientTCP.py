import socket, threading, sys, select
import ctypes, pickle

libc = ctypes.cdll.LoadLibrary("./libc.so")
x=0
with socket.socket() as s:
    s.connect(('', 9940))
    computer = s.recv(1024)
    if(int(format(computer.decode()))==1):
        print("Você está no computador mestre, digite o valor para calculo:")
    
    while True:
        io_list = [sys.stdin, s]
        ready_to_read,ready_to_write,in_error = select.select(io_list , [], [])
        for io in ready_to_read:
            if io is s: # se tivermos recebido mensagem
                data = s.recv(4096)
                resp = pickle.loads(data)
                #print(resp)
                if(int(resp[0])<=4):
                    x = int(resp[0])
                    if(len(resp)==2):
                        print("Computando a parte: ",x)
                        number_solutions = libc.mainC(int(resp[1]),x)
                        s.send(format(number_solutions).encode())
                    else:
                        resultado = int(resp[2])
                        print("O resultado total é: ", resultado)
                        print("\nInsira um novo valor para calculo:")
                    #print(number_solutions)
                if not resp:
                    print('server shutdown')
                    sys.exit()
	                #print(format(resp.decode()))
	                #print(int(format(resp.decode())))
            else:
                if(int(format(computer.decode()).encode('utf-8'))==1):
                    msg = sys.stdin.readline() # vamos enviar mensagem     
                    s.send(msg.encode())
                    sys.stdout.flush()
