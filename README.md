# Redes_Estufa

## Alunos:

* Bruno Mitsuo Homma - 9292625
* Danilo da Costa Telles Teo - 9293626

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

	
	//SENSOR -> GERENCIADOR 
	CONECTA_SENSOR: 
		id_sensor (obrigatório);
		flag_requisicao (obrigatório);

	//ATUADOR -> GERENCIADOR 
	CONECTA_ATUADOR: 
		id_atuador (obrigatório);
		flag_requisicao (obrigatório);

	//GERENCIADOR -> SENSOR/ATUADOR 
	CONECTA_GERENCIADOR: 
		id_sensor/id_atuador (obrigatório);
		flag_conectado (obrigatório);

	//SENSOR -> GERENCIADOR 
	SEND_REPORT: 
		id_sensor (obrigatório);
		val_medida(obrigatório);	

	//GERENCIADOR -> ATUADOR 
	ONOFF_ATUADOR: 
		id_atuador(obrigatório);
		liga/desliga(obrigatório).

	//GERENCIADOR -> CLIENTE 
	SEND_REPORT: 
		valor_co2 (obrigatório);
		valor_temperatura (obrigatório);
		valor_umidade (obrigatório).

	//CLIENTE -> GERENCIADOR 
	SET_PARS: 
		valor_temp_min (obrigatório);
		valor_temp_max (obrigatório);
		valor_umidade_min (obrigatório);
		valor_umidade_max (obrigatório);
		valor_co2_min (obrigatório);
		valor_co2_max (obrigatório).

	//CLIENTE -> GERENCIADOR
	REQUEST_REPORT:  
	flag_requisicao (obrigatório).




</pre>

## Header:
O Header tera um comprimento fixo, conhecido por todos os processos (HEADER_LENGTH) que sera de 8 bytes:

* Timestamp (4 bytes): iteracao na qual a mensagem enviada/recebida;
* Tipo (1 byte): tipo da mensagem que foi enviada/recebida;
* Tamanho do Payload (3 bytes): tamanho do corpo da mensagem enviada/recebida

## Observações:

### Timestamp:
É válido notar que o campo timestamp possui 4 possiveis interpretacoes. Existem 3 timestamps para os sensores (CO2, temperatura e umidade) e estes enviam este timestamp para seus respectivos atuadores. A unica interpretacao restante é o timestamp do Gerenciador que é o que é enviado ao cliente. Este campo foi usado, principalmente, para garantir que o envio das informações esta bem sincronizado e que as informações contidas nos relatórios eram confiáveis. No processo do Gerenciador podem ser vistos os 4 timestamps no seguinte formato: "(t_gerenciador): t_co2, t_temperatura, t_umidade"

No processo dos sensores serao exibidos os timestamps ao lado das medidas (geradas aleatoriamente) no seguinte formato: "t_co2: medida"
Nos atuadores o timestamp indicara o estado do atuador no timestamp definido, *lembrando que cada atuador segue o timestamp de seu respectivo sensor*.

### Nova Mensagem (SET_PARS):
Esta mensagem teve sua necessidade constatada apenas durante o desenvolvimento e por isso não constou no documento apresentado inicialmente. 

### Mudanças nas mensagens:
Algumas mensagens tiveram seus parametros e conteúdos alterados pois fez mais sentido dada a aplicação fazer essas mudanças (Ex.: sempre enviar o relatório de todos os sensores ao inves de apena um unico selecionado)

## Execução:
Para executar o projeto corretamente, é importante que se siga esses passos de acordo e em ordem, a fim de que nada funcione fora do esperado:
O projeto foi desenvolvido e testado nas seguintes especificações:

* *Sistema Operacional*: Ubuntu 18.04.2 LTS
* *Linguagem*: Python 3.7.1

#### Instruções:
1. Abra *8 terminais* dentro da pasta `code/` do projeto. Cada um destes será um componente do sistema e deve-se lembra qual é qual;
2. O primeiro código a ser executado é o Gerenciador. Em um terminal rode `python3 gerenciador.py`. Nada acontecerá ainda;
3. A seguir devem ser iniciados os Sensores. Inicie cada um em um terminal diferente na ordem: (1)`python3 sensor_co2.py`; (2)`python3 sensor_temp.py`; (3)`python3 sensor_umidade.py`. Será possível ver os timestamps aparecendo no Gerenciador assim como as medidas sendo geradas nos Sensores.
4. O próximo passo é iniciar os Atuadores. Da mesma maneira que os Sensores, execute cada um em um terminal diferente seguindo a ordem: (1)`python3 atuador_co2.py`; (2)`python3 atuador_aquece_resfria.py`; (3)`python3 atuador_irrigacao.py`. Logo que iniciarem, serão exibidos os estados dos atuadores.
5. Finalmente podemos iniciar o cliente! No último terminal execute `python3 cliente.py`. Serão requisitadas 6 medidas para determinar os parâmetros da estufa:Concentração Máxima de CO2; Concentração Mínima de CO2; Temperatura Máxima; Temperatura Mínima; Nível de Umidade Máximo; Nível de Umidade Mínimo. Para as entradas desses valores considere sempre preencher casas a direita. Por exemplo, 8.12 é entendido pelo sistema, mas 8.1 NÃO será interpretado como 8.10. Também não é necessário se preocupar com a inserção das unidades de medida.
6. Uma vez inseridas as medidas, serão oferecidas as opções de encerrar o programa Cliente ou de Receber o relatório de medidas, basta entrar com uma das opções.
7. Se deseja encerrar todas as janelas, basta pressionar Ctrl + C na janela do Gerenciador.