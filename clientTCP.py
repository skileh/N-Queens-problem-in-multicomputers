import socket, threading, sys, select
import ctypes

libc = ctypes.cdll.LoadLibrary("./libc.so")
x=0
with socket.socket() as s:
    s.connect(('', 9942))
    while True:
        io_list = [sys.stdin, s]
        ready_to_read,ready_to_write,in_error = select.select(io_list , [], [])
        for io in ready_to_read:
            if io is s: # se tivermos recebido mensagem
                resp = s.recv(1024)
                if(int(format(resp.decode()))<=4):
                	x = int(format(resp.decode()))
                	print("PC Numero: ")
                	print(x)
                else:
	                number_solutions = libc.mainC(int(format(resp.decode())),x)
	                print(number_solutions)
	                if not resp:
	                    print('server shutdown')
	                    sys.exit()
	                #print(format(resp.decode()))
	                #print(int(format(resp.decode())))
            else:
                msg = sys.stdin.readline() # vamos enviar mensagem                
                s.send(msg.encode())
                sys.stdout.flush()
