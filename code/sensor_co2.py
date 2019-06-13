import socket
import select
import errno
import sys

# 1 byte para o tipo da mensagem e mais 3 para o tamanho
HEADER_LENGTH = 4 

#Sensores e atuadores (global)
SENSOR_CO2 = 0
SENSOR_TEMP = 1
SENSOR_UM = 2

ATUADOR_CO2 = 3
AQUECEDOR = 4
RESFRIADOR = 5

# Mensagens (global)
CONECTA_SENSOR = 0
CONECTA_ATUADOR = 1
CONECTA_GERENCIADOR = 2
SENSOR_SEND_REPORT = 3
ONOFF_ATUADOR = 4
GERENCIADOR_SEND_REPORT = 5
REQUEST_REPORT = 6




# Definicao de porta e IP a serem utilizados
IP = "127.0.0.1"
PORT = 1234

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
#client_socket.setblocking(False)



while True:
	message = str(SENSOR_CO2) + str(1)
	header = str(CONECTA_SENSOR) + str(len(message)).zfill(3)
	full_msg = (header + message).encode('utf-8')
	client_socket.send(full_msg)

	while True:
		# Receive messages
			header = client_socket.recv(HEADER_LENGTH)				
			if not len(header):
				print("deu ruim no header")
				sys.exit()
			header = header.decode('utf-8').strip()
			msg_type = int(header[0])
			msg_tam = int(header[1:4])

			msg = client_socket.recv(msg_tam).decode('utf-8').strip()

			print(f"Tipo: {msg_type}\nTamanho: {msg_tam}\nMensagem: {msg}")
