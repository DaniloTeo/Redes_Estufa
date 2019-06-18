import socket
import select
import random
import time

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

N = 0

while True:
	# Envia mensagem de requisicao de conexao
	message = str(SENSOR_TEMP) + str(1)
	header = str(0).zfill(4) + str(CONECTA_SENSOR) + str(len(message)).zfill(3)
	full_msg = (header + message).encode('utf-8')
	client_socket.send(full_msg)

	# Recebe autorizacao ou negacao de conexao
	header = client_socket.recv(HEADER_LENGTH)				
	if not len(header):
		#print("deu ruim no header")
		break
	
	header = header.decode('utf-8').strip()
	msg_it = int(header[0:4])
	msg_type = int(header[4])
	msg_tam = int(header[5:])
	msg = client_socket.recv(msg_tam).decode('utf-8').strip() # recebe a mensagem baseado no tamanho
	print(f"Tipo: {msg_type}\nTamanho: {msg_tam}\nMensagem: {msg}")

	while True:
		# Laco para gerar os valores dos sensores e envia-los ao gerenciador

		# gera valores aleatorios para mock do sensor
		val = random.uniform(25.0, 40.0)
		#print(f"Numerico: {val}")
		
		# Obtem apenas ate as duas primeiras casas decimais do numero
		val = str(val)[:5] + 'gr C'
		print(f"{N}: {val}")
		
		message = str(SENSOR_TEMP) + val
		header = str(N).zfill(4) + str(SENSOR_SEND_REPORT) + str(len(message)).zfill(3)
		full_msg = (header + message).encode('utf-8')
		try:
			client_socket.send(full_msg)
		except:
			break
		
		N += 1

		# espera um segundo e repete o processo
		time.sleep(1)
	break

client_socket.close()