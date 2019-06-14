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

# Configurar porta para cada elemento cliente...
SENSOR_PORT = 1234

TEST_PORT = 1235
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


# Funcao que cria o socket, set o sockopt, faz o bind a porta certa e seta o listen
# para cada socket separado
def socket_set_up(this_socket, ip, host):
	pass

# End of aux functions


# Configura socket para utilizar protocolo TCP e STREAM???
sensor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Ver oq isso faz???
sensor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind do socket a porta e ao IP
sensor_socket.bind((IP, SENSOR_PORT))


#############################33


test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Ver oq isso faz???
test_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind do socket a porta e ao IP
test_socket.bind((IP, TEST_PORT))

# Seta o socket para aguardar conexoes
test_socket.listen()

sockets_list = [test_socket]

clients = {}

while True:
	full_msg = ''

	client_socket, addr = test_socket.accept()
	print(f"Connection from {addr} has been established.")

	test_client, ad = 

	msg = receive_message(client_socket)
	print(msg)
	if msg['type'] == CONECTA_SENSOR:
		# Obtem o id do sensor/atuador que enviou
		id_sender = int(msg['msg'][0])

		#obtem a flag de requisicao (1, pedindo para conectar)
		flag_req = int(msg['msg'][1])
		print(flag_req)
		if flag_req != 1:
			out_msg_content = str(id_sender) + str(0) # n conectou
		else:
			out_msg_content = str(id_sender) + str(1) # conectou

		out_msg_header = str(CONECTA_GERENCIADOR) + str(len(out_msg_content)).zfill(3)
		out_msg = (out_msg_header + out_msg_content).encode('utf-8')	
		client_socket.send(out_msg)