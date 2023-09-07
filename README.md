
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

![Arquitetura do sistema.](https://github.com/bielcmoraes/Concorrencia-e-Conectividade/blob/main/images_README/arquitetura_do_sistema.png)

<p style="text-align: justify;">
  É possivel visualizar através da imagem que o sistema inicia o processo de comunicação quando um um sensor RFID identifica uma ou mais tags RFID e envia essa(s) tags via socket para o caixa que está conectado ao leitor RFID. O caixa por sua vez, além de está conectado ao sensor RFID também está conectado a um servidor intermediário por meio de socket.
</p>

<p style="text-align: justify;">
  O servidor intermediário é responsável por gerenciar conexões, receber mensagens dos caixas e responder as mensagens de maneira coerente e eficaz, além de poder bloquear e desbloquer os caixas. Para isso, o servidor intermediário cria uma thread para cada conecxão gerenciada pelo mesmo, ou seja, cria uma thread para cada caixa conectado com ele. As threads recebem e respondem as mensagens do caixa conforme o solicitado e, para tal fazem requisições ao servidor HTTP responsável por armazenar todas as informações relevantes e persistentes do sistema. Os verbos HTTP implementados foram: GET, POST e PATCH e, são utilizados conforme as necessidades do servidor intermediário e dos caixas conectados.
</p>

<p style="text-align: justify;">
  No servidor HTTP são mantidos três dicionários Python: o primeiro contendo os dados de cada produto, o segundo com as informações de IP, porta e status (bloqueado ou não) de cada caixa que se conectou ao sistema e o terceiro com o histórico das compras que foram realizadas no sistema. Para resolver o problema de concorrência relacionado ao acesso desses dicionários compartilhados foram implementados "threads lock" nas operações que alterassem o conteúdo desses recursos compartilhados, ou seja, principíos de "zona crítica" foram adotados e implementados utilizando a biblioteca "threading". Assim foi possível garantir que apenas um processo (caixa) por vez tivesse acesso ao recurso, evitando erros.
</p>

<p style="text-align: justify;">
  As requisições HTTP através dos respectivos verbos HTTP desempenham um papel muito importante no sistema, pois fazem a comunicação do servidor intermediário com o servidor HTTP que é o encarregado de armazenar as informações persistentes. Além disso, por meio das requisições HTTP é possível testar e utilizar funcionalidades dos sistema sem utilizar o terminal. Todas as rotas válidas para a aplicação serão disponibilizadas a seguir:
</p>

<p style="text-align: justify;">
  <ol>
    <li>
      <h3>GET:</h3>
      <ul>
        <li> "/" - Lista todos os produtos existentes.</li>
        <li> "/:idProduto" - Consulta um produto específico.</li>
        <li> "/client/:idClient" - Consulta um cliente (caixa) específico.</li>
        <li> "/history/client/:idClient" - Consulta o histórico de compras de um cliente (caixa) específico.</li>
      </ul>
    </li>
    <li>
      <h3>POST:</h3>
      <ul>
        <li> "/:idCliente" - Adiciona um produto ao carrinho de um cliente (caixa) específico.</li>
        <li> "/checkout" - Finaliza uma compra e cadastra a compra no histórico de compras.</li>
        <li> "/client/:idClient" - Cadastra um client (caixa) no sistema.</li>
      </ul>
    </li>
    <li>
      <h3>PATCH:</h3>
      <ul>
        <li> "/:idCliente" - Atualiza o carrinho de compras de um cliente (caixa) específico.</li>
        <li> "client/:idCliente" - Atualiza o status de um cliente (caixa) específico.</li>
        <li> "clear/:idCliente" - Limpa um carrinho de compras de um cliente (caixa) específico.</li>
      </ul>
    </li>
  </ol>
</p>

<p style="text-align: justify;">
  Todas as rotas criadas desempenham um papel fundamental para o funcionamento do sistema, porém nem todas interagem diretamente com o servidor socket, ou seja, nem todas são chamadas explicitamente por esse componente do sistema.
  Por exemplo, a rota "clear/:idCliente" só deve ser chamada em caso de erro no servidor socket durante uma compra, especificamente, quando o servidor socket "cair" e o carrinho contenha produtos de uma compra não finalizada.
  Dessa forma, a rota servirá para limpar o carrinho após a correção do erro, evitando que os produtos da compra que não foi finalizada entrem na próxima compra.
</p>

# 3. Resultados

<p style="text-align: justify;">
  Para o devido funcionamento do sistema pelo usuário final, é necessário executar de maneira sequencial os componentes principais do sistema: "http_server", "socket_server", sensor RFID ("rfid_reader") e caixas ("socket_client").
  No caixa é necessário digitar via terminal o endereço IP no qual o socket_server foi inicializado, após inserir o endereço do servidor é possível acessar uma interface que possibilita ao usuário iniciar uma compra ou sair do sistema, conforme a imagem abaixo:
</p>

![Menu inicial do caixa.](https://github.com/bielcmoraes/Concorrencia-e-Conectividade/blob/main/images_README/menu_inical_client.png)

<p style="text-align: justify;">
  Ao escolher iniciar uma compra é possível acessar o menu de compras onde o usuário deve escolher entre digitar o código de um produto manualmente, ler os produtos utilizandos as TAGS RFID atraves do sensor ou finalizar a compra e retornar ao menu anterior, conforme a imagem:
</p>
