import socket
import select
import random
import time
import sys

# 1 byte para o tipo da mensagem e mais 3 para o tamanho
HEADER_LENGTH = 8

#Sensores e atuadores (global)
SENSOR_CO2 = 0
SENSOR_TEMP = 1
SENSOR_UM = 2

ATUADOR_CO2 = 3
AQUECEDOR_RESFRIADOR = 4
#RESFRIADOR = 5
IRRIGADOR = 5

CLIENTE = 6

# Mensagens (global)
CONECTA_SENSOR = 0
CONECTA_ATUADOR = 1
CONECTA_GERENCIADOR = 2
SENSOR_SEND_REPORT = 3
ONOFF_ATUADOR = 4
GERENCIADOR_SEND_REPORT = 5
REQUEST_REPORT = 6
SET_PARS = 7




# Definicao de porta e IP a serem utilizados
IP = "127.0.0.1"
PORT = 1234

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(True)

estado = ''



while True:
	# Envia mensagem de requsicao de conexao
	message = str(IRRIGADOR) + str(1)
	header = str(0).zfill(4) + str(CONECTA_ATUADOR) + str(len(message)).zfill(3)
	full_msg = (header + message).encode('utf-8')
	client_socket.send(full_msg)

	# Recebe aceitacao ou negacao de conexao
	header = client_socket.recv(HEADER_LENGTH)				
	if not len(header):
		#print("deu ruim no header")
		break
	
	header = header.decode('utf-8').strip()
	msg_it = int(header[0:4])
	msg_type = int(header[4])
	msg_tam = int(header[5:])
	msg = client_socket.recv(msg_tam).decode('utf-8').strip()
	print(f"Tipo: {msg_type}\nTamanho: {msg_tam}\nMensagem: {msg}")

	while True:
		# Laco para receber o comando de ON ou OFF no atuador
		
		header = client_socket.recv(HEADER_LENGTH)

		if not len(header):
			#print("deu ruim no header")
			break

		header = header.decode('utf-8').strip()
		print(header)

		msg_it = int(header[0:4])
		msg_type = int(header[4])
		msg_tam = int(header[5:])
		msg = client_socket.recv(msg_tam).decode('utf-8').strip()
		#print(msg)
		
		estado = msg[1:]
		
		print(f"{msg_it}:\n\tEstado do Irrigador: {estado}")
	break
client_socket.close()
