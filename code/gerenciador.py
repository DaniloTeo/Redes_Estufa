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

# Configurar porta para cada elemento cliente...
SENSOR_PORT = 1234
# Start of aux functions

def receive_message(client_socket):
	try:
		#print("entrou no try")
		header = client_socket.recv(HEADER_LENGTH)

		if not len(header):
			#print("entrou no if ruim")
			return False

		header = header.decode('utf-8').strip()
		msg_type = int(header[0])
		msg_tam = int(header[1:4])
		msg = client_socket.recv(msg_tam).decode('utf-8')
		
		return {'type': msg_type, 'tam': msg_tam, 'msg': msg}

	except:
		#print("entrou no except")
		return False




# End of aux functions


# Configura socket para utilizar protocolo TCP e STREAM???
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Ver oq isso faz???
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind do socket a porta e ao IP
server_socket.bind((IP, SENSOR_PORT))

server_socket.listen()

# Lista de sockets ativos,a principio apenas com o do server
sockets_list = [server_socket]

# Dicionario para gerar o relatorio de medidas a ser enviado para o cliente caso requisitado
relatorio = {
	'co2': '31.00',
	'temperatura': '28.55',
	'umidade': '31.00'
}

# Dicionario para guardar os parametros enviados pelo cliente 
medidas = {
	'co2_max': '30.00',
	'co2_min': '04.00',
	'temp_max': '47.31',
	'temp_min': '28.56',
	'umidade_max': '33.58',
	'umidade_min': '30.00'
}


while True:
	# Salva todos os sockets prontos para leitura em read_sockets
	read_sockets, _, _ = select.select(sockets_list, [], [])
	
	# Para cada socket faca
	for notified_socket in read_sockets:
			if notified_socket == server_socket: # se for uma nova conexao a ser estabelecida, ela eh aceita
					client_socket, client_address = server_socket.accept()
					sockets_list.append(client_socket)
					print(f"Accepted new connection from {client_address[0]}:{client_address[1]}")
			else:

				# Se nao for uma nova conexao recebe a mensagem do socket
				msg = receive_message(notified_socket)
				#print("Conteudo da msg: " + str(msg))
			
				if msg['type'] == CONECTA_SENSOR or msg['type'] == CONECTA_ATUADOR:
					# Obtem o id do sensor/atuador que enviou
					id_sender = int(msg['msg'][0])

					#obtem a flag de requisicao (1, pedindo para conectar)
					flag_req = int(msg['msg'][1])
					#print(flag_req)
					
					if flag_req != 1:
						out_msg_content = str(id_sender) + str(0) # n conectou
					else:
						out_msg_content = str(id_sender) + str(1) # conectou

					# Depois que o payload foi montado, eh a vez do header
					out_msg_header = str(CONECTA_GERENCIADOR) + str(len(out_msg_content)).zfill(3)
					
					# Composicao da mensagem por completo e codificao para bytes 
					out_msg = (out_msg_header + out_msg_content).encode('utf-8')	
					
					# Envio da mensagem
					notified_socket.send(out_msg)

				elif msg['type'] == SENSOR_SEND_REPORT:
					# Obtem a origem do envio do relatorio assim como o valor da medida
					id_sender = int(msg['msg'][0])
					val = msg['msg'][1:]

					# atualiza o relatorio de medidas a ser enviado para o cliente
					if id_sender == SENSOR_TEMP:
						relatorio['temperatura'] = val
					
					elif id_sender == SENSOR_CO2:
						relatorio['co2'] = val
					
					elif id_sender == SENSOR_UM:
						relatorio['umidade'] = val

					print(medidas)
					print(relatorio)
				elif msg['type'] == SET_PARS:
					pass
					# medidas['co2_max'] = msg['msg'][0:5]
					# medidas['co2_min'] = msg['msg'][5:10]
					# medidas['temp_max'] = msg['msg'][10:15]
					# medidas['temp_min'] = msg['msg'][15:20]
					# medidas['umidade_max'] = msg['msg'][20:25]
					# medidas['umidade_min'] = msg['msg'][25:30]

				elif msg['type'] == REQUEST_REPORT:
					pass

				if float(medidas['co2_max']) <= float(relatorio['co2'][0:5]):
					# Se o maximo definido for menor que o atual -> desliga
					out_msg_content = str(ATUADOR_CO2) + 'OFF'
					out_msg_header = str(ONOFF_ATUADOR) + str(len(out_msg_content)).zfill(3)
					out_msg = (out_msg_header + out_msg_content).encode('utf-8')
					
					# Se a lista ja possuir o socket do atuador em questao, envia a mensagem
					if len(sockets_list) > ATUADOR_CO2+1:
						sockets_list[ATUADOR_CO2+1].send(out_msg)
				
				elif float(medidas['co2_min']) >= float(relatorio['co2'][0:5]):
					# Se o minimo definido for maior que o atual -> liga
					out_msg_content = str(ATUADOR_CO2) + 'ON '
					out_msg_header = str(ONOFF_ATUADOR) + str(len(out_msg_content)).zfill(3)
					out_msg = (out_msg_header + out_msg_content).encode('utf-8')
					
					# Se a lista ja possuir o socket do atuador em questao, envia a mensagem
					if len(sockets_list) > ATUADOR_CO2+1:
						sockets_list[ATUADOR_CO2+1].send(out_msg)
				
				if float(medidas['temp_max']) <= float(relatorio['temperatura'][0:5]):
					# Se o maximo definido for menor que o atual -> desliga aquecedor e liga resfriador
					out_msg_content = str(AQUECEDOR_RESFRIADOR) + 'OFFON '
					out_msg_header = str(ONOFF_ATUADOR) + str(len(out_msg_content)).zfill(3)
					out_msg = (out_msg_header + out_msg_content).encode('utf-8')
					
					# Se a lista ja possuir o socket do atuador em questao, envia a mensagem
					if len(sockets_list) > AQUECEDOR_RESFRIADOR+1:
						sockets_list[AQUECEDOR_RESFRIADOR+1].send(out_msg)
				
				elif float(medidas['temp_min']) >= float(relatorio['temperatura'][0:5]):
					# Se o minimo definido for maior que o atual -> liga aquecedor e desliga resfriador
					out_msg_content = str(AQUECEDOR_RESFRIADOR) + 'ON OFF'
					out_msg_header = str(ONOFF_ATUADOR) + str(len(out_msg_content)).zfill(3)
					out_msg = (out_msg_header + out_msg_content).encode('utf-8')
					
					# Se a lista ja possuir o socket do atuador em questao, envia a mensagem
					if len(sockets_list) > AQUECEDOR_RESFRIADOR+1:
						sockets_list[AQUECEDOR_RESFRIADOR+1].send(out_msg)
				
				if float(medidas['umidade_max']) <= float(relatorio['umidade'][0:5]):
					# Se o maximo definido for menor que o atual -> desliga
					out_msg_content = str(IRRIGADOR) + 'OFF'
					out_msg_header = str(ONOFF_ATUADOR) + str(len(out_msg_content)).zfill(3)
					out_msg = (out_msg_header + out_msg_content).encode('utf-8')
					
					# Se a lista ja possuir o socket do atuador em questao, envia a mensagem
					if len(sockets_list) > IRRIGADOR+1:
						sockets_list[IRRIGADOR+1].send(out_msg)
				
				elif float(medidas['umidade_min']) >= float(relatorio['umidade'][0:5]):
					# Se o minimo definido for maior que o atual -> liga
					out_msg_content = str(IRRIGADOR) + 'ON '
					out_msg_header = str(ONOFF_ATUADOR) + str(len(out_msg_content)).zfill(3)
					out_msg = (out_msg_header + out_msg_content).encode('utf-8')
					
					# Se a lista ja possuir o socket do atuador em questao, envia a mensagem
					if len(sockets_list) > IRRIGADOR+1:
						sockets_list[IRRIGADOR+1].send(out_msg)

				
