# Redes_Estufa

## TO DO:
* Entender como empregar mais de um socket no server - um pra cada atuador, sensor e cliente (usar socket_list inserir na ordem do id de cada elemento)
* Implementar a maioria dos clientes...
* Pesquisar duvidas teoricas anotadas no gerenciador.py


## Aplicação:
Aplicação 01 - Estufa Inteligente: "Estufas são utilizadas no cultivo de plantas em condições controladas de temperatura,umidade, luminosidade, nível de CO2, entre outras variáveis.Nesta aplicação, as condições da estufa são configuradas, monitoradas e controladaspor um gerenciador, que se comunica com os sensores/atuadores dentro da estufa e podereceber configurações ou responder consultas de um cliente externo."

### Sensores:
* Temperatura Interna;
* Umidade do Solo;
* Nivel do CO2;
### Atuadores:
* Aquecedor (aumenta temperatura);
* Resfriador (diminui temperatura);
* Sistema de Irrigação (aumenta a umidade do solo);
* Injetor de CO2 (aumenta concentração do gás);

*Gerenciador*: server da aplicação
*Cliente*: configura parâmetros da estufa e requisitar valores de leituras dos sensores
*Principio de Operação*: O Gerenciador deve manter as leituras dos sensores entre os valores máximo e mínimo configurados.

## Mensagens:
<pre>

	CONECTA_SENSOR: //SENSOR -> GERENCIADOR
	id_sensor (obrigatório);
	flag_requisicao (obrigatório);

	CONECTA_ATUADOR: //ATUADOR -> GERENCIADOR
	id_atuador (obrigatório);
	flag_requisicao (obrigatório);

	CONECTA_GERENCIADOR: //GERENCIADOR -> SENSOR/ATUADOR
	id_sensor/id_atuador (obrigatório);
	flag_conectado (obrigatório);


	SEND_REPORT: //SENSOR -> GERENCIADOR
	id_sensor (obrigatório);
	val_medida(obrigatório);	

	ONOFF_ATUADOR: //GERENCIADOR -> ATUADOR
	id_atuador(obrigatório);
	liga/desliga(obrigatório).

	SEND_REPORT: //GERENCIADOR -> CLIENTE
	id_sensor/all;
	valor/valores.

	REQUEST_REPORT: //CLIENTE -> GERENCIADOR
	id_sensor/all;




</pre>

## Header:
Identificara o tipo da mensagem...
