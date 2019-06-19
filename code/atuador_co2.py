'''
Codigo para simular o gerenciamento de um Injetor de CO2 baseado nas
medidas estabelecidas pelo usuario como delimitantes.
O programa estabelece conexao com o Gerenciador e a partir de entao aguarda o envio de
requisicoes de ligar/desligar deste.

Bruno Mitsuo Homma 	9292625
Danilo da Costa Telles Teo 	9293626


'''

import socket

# 4 bytes para o timestamp, 1 byte para o tipo da mensagem e mais 3 para o tamanho
HEADER_LENGTH = 8 

#Sensores e atuadores (global)
SENSOR_CO2 = 0
SENSOR_TEMP = 1
SENSOR_UM = 2

ATUADOR_CO2 = 3
AQUECEDOR_RESFRIADOR = 4
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

# Definicao do uso dos protocolos IPv4 e TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Prepara para conexão do tipo bloqueante
client_socket.connect((IP, PORT))
client_socket.setblocking(True)

# Estado do atuador
estado = ''


while True:
	# Envia requisicao de conexao
	message = str(ATUADOR_CO2) + str(1)
	header = str(0).zfill(4) + str(CONECTA_ATUADOR) + str(len(message)).zfill(3)
	full_msg = (header + message).encode('utf-8')
	client_socket.send(full_msg)

	# Recebe negacao ou aceitacao de conexao
	header = client_socket.recv(HEADER_LENGTH)				
	if not len(header):
		# se houver problema com o header, o programa eh encerrado
		break
	
	# Recebe e decodifica o header
	header = header.decode('utf-8').strip()
	
	# Extrai o timestamp
	msg_it = int(header[0:4])
	
	# Extrai o tipo da mensagem
	msg_type = int(header[4])

	# Extrai o tamanho do corpo da mensagem
	msg_tam = int(header[5:])

	# Recebe e decodifica a mensagem baseado no tamanho
	msg = client_socket.recv(msg_tam).decode('utf-8').strip()
	print(f"Tipo: {msg_type}\nTamanho: {msg_tam}\nMensagem: {msg}")

	while True:
		# Laco para receber o comando ON ou OFF para o atuador
		
		header = client_socket.recv(HEADER_LENGTH)

		if not len(header):
			break

		header = header.decode('utf-8').strip()
		msg_it = int(header[0:4])
		msg_type = int(header[4])
		msg_tam = int(header[5:])
		msg = client_socket.recv(msg_tam).decode('utf-8').strip()
		
		estado = msg[1:]
		
		# Imprime o estado do atuador e a iteracao da medida que o afetou
		print(f"{msg_it}:\n\tEstado do Injetor de CO2: {estado}")
	break
client_socket.close()
