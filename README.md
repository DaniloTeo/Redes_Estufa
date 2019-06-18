# Redes_Estufa

## TO DO:
* Entender como empregar mais de um socket no server - um pra cada atuador, sensor e cliente (usar socket_list inserir na ordem do id de cada elemento) - DONE (usando select)
* Implementar tratamento Sensores - DONE
* Implementar tratamento Atuadores - DONE
* Implementar tratamento Clientes - DONE
* Corrigir erro: cancelar qualquer um dos processos faz com que a rede toda caia - DONE
* Pesquisar duvidas teoricas anotadas no gerenciador.py - !!!!


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

	
	CONECTA_SENSOR: //SENSOR -> GERENCIADOR - DONE
	id_sensor (obrigatório);
	flag_requisicao (obrigatório);

	CONECTA_ATUADOR: //ATUADOR -> GERENCIADOR - DONE
	id_atuador (obrigatório);
	flag_requisicao (obrigatório);

	CONECTA_GERENCIADOR: //GERENCIADOR -> SENSOR/ATUADOR - DONE
	id_sensor/id_atuador (obrigatório);
	flag_conectado (obrigatório);


	SEND_REPORT: //SENSOR -> GERENCIADOR - DONE
	id_sensor (obrigatório);
	val_medida(obrigatório);	

	ONOFF_ATUADOR: //GERENCIADOR -> ATUADOR - DONE
	id_atuador(obrigatório);
	liga/desliga(obrigatório).

	SEND_REPORT: //GERENCIADOR -> CLIENTE - DONE
	valor_co2;
	valor_temperatura;
	valor_umidade.

	SET_PARS: //CLIENTE -> GERENCIADOR - DONE
	valor_temp_min, valor_temp_max;
	valor_umidade_min, valor_umidade_max;
	valor_co2_min, valor_co2_max;

	REQUEST_REPORT: //CLIENTE -> GERENCIADOR - DONE
	all;




</pre>

## Header:
Identificara o timestamp da mensagem, o tipo da mensagem e o tamanho desta. Como as mensagens (e o seu header) sera passado como string, serao reservado 8 caracters (bytes) para o header sendo 4 para a o timestamp, um para o tipo da mensagem (de 0 a 7) e 3 caracters para o tamanho (se o tamanho for menor que 100 os caracteres faltantes sao preenchidos com '0' Ex.: '042')
