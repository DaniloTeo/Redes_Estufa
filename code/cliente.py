'''
Codigo para simular o funcinamento de uma aplicação na qual o usuário pode definir os
parâmetros de uma estufa inteligente e receber relatórios dos sensores quando desejar.

Bruno Mitsuo Homma 	9292625
Danilo da Costa Telles Teo 	9293626


'''

import socket

# 4 bytes para timestamp, 1 byte para o tipo da mensagem e mais 3 para o tamanho
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

# Define o uso dos protocolos IPv4 e TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Prepara para conexão do tipo bloqueante
client_socket.connect((IP, PORT))
client_socket.setblocking(True)

while True:
	# Laco inicial para insercao dos valores limitantes da estufa

	print("Insira os valores no seguinte formato: X.XX; Ex.: 4.20\Coloque os zeros a direita, nos cuidamos dos zeros a esquerda :)")
	co2_max = input("Insira a concentracao maxima de CO2: ")
	co2_min = input("Insira a concentracao minima de CO2: ")
	temp_max = input("Insira a temperatura maxima: ")
	temp_min = input("Insira a temperatura minima: ")
	umidade_max = input("Insira a umidade maxima: ")
	umidade_min = input("Insira a umidade minima: ")

	# Prepara as medidas, garantindo que estejam na ordem certa e que possuam 5 bytes
	msg_content = co2_max.zfill(5) + co2_min.zfill(5) + temp_max.zfill(5) + temp_min.zfill(5) + umidade_max.zfill(5) + umidade_min.zfill(5)

	# Prepara o header da mensagem
	msg_header =  str(0).zfill(4) + str(SET_PARS) + str(len(msg_content)).zfill(3)
	
	# Codifica a mensagem e tenta enviar. Se nao conseguir, encerra a execução
	msg = (msg_header + msg_content).encode('utf-8')
	try:
		client_socket.send(msg)
	except:
		break

	# variavel da opcao de relatorio
	opt = -1
	
	while True:
		# Laco para recebimento dos relatorios ou encerramento do programa

		opt = input("Digite 1 para receber o relatorio (ou 0 para sair): ")

		if int(opt) != 0:
			# Envia mensagem pedindo relatorios 
			msg_content = str(CLIENTE) + str(1) # flag de requisicao de relatorio
			msg_header =  str(0).zfill(4) + str(REQUEST_REPORT) + str(len(msg_content)).zfill(3)
			msg = (msg_header + msg_content).encode('utf-8')
			try:
				client_socket.send(msg)
			except:
				break

			# Recebe o relatorio
			header = client_socket.recv(HEADER_LENGTH)

			if not len(header):
				# se houver problema com o header, o programa eh encerrado
				break
			# Recebe o header e decodifica
			header = header.decode('utf-8').strip()
			
			# Extrai o timestamp
			msg_it = int(header[0:4])

			# Extrai o tipo da mensagem
			msg_type = int(header[4])

			# Extrai o tamanho do corpo da mensagem
			msg_tam = int(header[5:])

			# Recebe a mensagem baseado no tamanho
			message = client_socket.recv(msg_tam).decode('utf-8').strip()
			
			# Organiza os valores do relatorio 
			val_co2 = message[0:6]
			val_temp = message[6:15]
			val_umidade = message[15:]
		else:
			# Se a opcao for 0, encerra o programa
			print("Programa Encerrado")
			break
		
		# Impressao do relatorio com timestamp
		print(f"Relatorios de Medidas({msg_it}):\n\tConcentracao CO2: {val_co2}\n\tTemperatura:{val_temp}\n\tUmidade: {val_umidade}")
	break
client_socket.close()

