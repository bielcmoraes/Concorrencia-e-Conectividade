
<h1 align="center">MI de Concorrencia e Conectividade</h1>
<h2 align="center">Problema 1</h2>
<h3 align="center">Aluno: Gabriel Cordeiro Moraes</h3>
<h3 align="center">Matrícula: 20111201</h3>

# 1. Introdução

<p style="text-align: justify;">
  A automação de supermercados representa uma evolução notável no setor de varejo, impulsionando a eficiência e proporcionando uma experiência de compra mais conveniente e ágil para os consumidores.
  A crescente tendência em direção à automação nesse contexto reflete o interesse em simplificar as operações e aprimorar a praticidade tanto para proprietários de supermercados quanto para os clientes.
  Além de nos oferece uma série de vantagens como: automação de processos de checkout, a eliminação das filas, gestão eficiente de estoques e personalização das recomendações de compras, a automação nos
  supermercados, associada à tecnologias como a Internet das Coisas (IoT) e a inteligência artificial podem permitir que os supermercados ofereçam uma experiência de compra mais intuitiva e personalizada.
</p>

<p style="text-align: justify;">
  Nesse contexto e aproveitando o cenário em constante evolução no setor de supermercados, um estabelecimento na cidade de Feira de Santana decidiu tomar a iniciativa de investir em um sistema moderno e eficiente para aprimorar seus negócios.
  Com o objetivo de possibilitar a leitura, a listagem e a compra de múltiplos produtos de maneira automatizada utilizando tecnologia de Radio Frequency Identification (RFID), os estudantes de Engenharia de Computação da Universidade Estadual
  de Feira de Santana (UEFS) foram desafiados implementar tal sistema.
</p>

<p style="text-align: justify;">
  Buscando viabilizar a implementação do sistema solicitado, atribuiu-se uma TAG exclusiva a cada produto disponível no supermercado, o que possibilitaria controles sobre os itens a serem vendidos.
  O sistema foi implementado utilizando a linguagem de programação Python na versão 3.10, com auxílio de bibliotecas internas e externas do módulo Python, como: mercury, threading, socket, http.server, requests, json, uuid e sys.
</p>

<p style="text-align: justify;">
  Para além, adotou-se uma arquitetura de rede baseada em TCP/IP com parte da comunicação sendo realizada via socket.
  Optou-se por um protocolo baseado em API REST com o objetivo de facilitar testes e escalonamento do sistema.
  A adoção de tais ferramentas e tecnologias permitiu a implementação de um sistema que atendesse aos requisitos do cliente.
</p>


# 2. Metodologia

<p style="text-align: justify;">
  Após algumas discussões com os demais alunos durante e após as seções PBL, decidiu-se uma arquitetura para o sitema que seria implementado. O design escolhido se assemelha com design dos demais integrantes da turma, porém apresenta suas particularidades, conforme a imagem abaixo:
</p>

![Arquitetura do sistema.](https://github.com/bielcmoraes/Concorrencia-e-Conectividade/blob/main/arquitetura_do_sistema.png)

<p style="text-align: justify;">
  É possivel visualizar através da imagem que o sistema inicia o processo de comunicação quando um um sensor RFID identifica uma ou mais tags RFID e envia essa(s) tags via socket para o caixa que está conectado ao leitor RFID. O caixa por sua vez, além de está conectado ao sensor RFID também está conectado a um servidor intermediário por meio de socket.
</p>

<p style="text-align: justify;">
  O servidor intermediário é responsável por gerenciar conexões, receber mensagens dos caixas e responder as mensagens de maneira coerente e eficaz, além de poder bloquear e desbloquer os caixas. Para isso, o servidor intermediário cria uma thread para cada conecxão gerenciada pelo mesmo, ou seja, cria uma thread para cada caixa conectado com ele. As threads recebem e respondem as mensagens do caixa conforme o solicitado e, para tal fazem requisições ao servidor HTTP responsável por armazenar todas as informações relevantes e persistentes do sistema. Os verbos HTTP implementados foram: GET, POST e PATCH e, são utilizados conforme as necessidades do servidor intermediário e dos caixas conectados.
</p>




