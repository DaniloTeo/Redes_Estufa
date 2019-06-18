import socket
import select
import random
import time

# 1 byte para o tipo da mensagem e mais 3 para o tamanho
HEADER_LENGTH = 4 

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

flag_relatorio = 0

while True:
	print("Insira os valores no seguinte formato: X.XX; Ex.: 4.20\Coloque os zeros a direita, nos cuidamos dos zeros a esquerda :)")
	co2_max = input("Insira a concentracao maxima de CO2: ")
	co2_min = input("Insira a concentracao minima de CO2: ")
	temp_max = input("Insira a temperatura maxima: ")
	temp_min = input("Insira a temperatura minima: ")
	umidade_max = input("Insira a umidade maxima: ")
	umidade_min = input("Insira a umidade minima: ")

	msg_content = co2_max.zfill(5) + co2_min.zfill(5) + temp_max.zfill(5) + temp_min.zfill(5) + umidade_max.zfill(5) + umidade_min.zfill(5)
	msg_header = str(SET_PARS) + str(len(msg_content)).zfill(3)
	msg = (msg_header + msg_content).encode('utf-8')
	client_socket.send(msg)

	flag_relatorio = input("Deseja Receber relatorios dos sensores a cada 10s?\n(Nao - digite 0\tSim - digite 1): ")


	if int(flag_relatorio) == 1:
		while True:

			# Envia mensagem pedindo relatorios temporizados
			msg_content = str(CLIENTE) + flag_relatorio # flag de requisicao de relatorio
			msg_header = str(REQUEST_REPORT) + str(len(msg_content)).zfill(3)
			print(f"Header: {msg_header}; Content:{msg_content}")
			msg = (msg_header + msg_content).encode('utf-8')
			client_socket.send(msg)

			# Recebe o relatorio e exibe na tela
			header = client_socket.recv(HEADER_LENGTH)
			if not len(header):
				print('Deu ruim no header')
				sys.exit()

			header = header.decode('utf-8').strip()
			msg_type = int(header[0])
			msg_tam = int(header[1:4])
			message = client_socket.recv(msg_tam).decode('utf-8').strip()

			val_co2 = message[0:6]
			val_temp = message[6:15]
			val_umidade = message[15:]

			print(f"Relatorios de Medidas:\n\tConcentracao CO2: {val_co2}\n\tTemperatura:{val_temp}\n\tUmidade: {val_umidade}")

			time.sleep(10)

