<div align="center">
  <h1>
      Relatório do problema 1: Supermercado inteligente
  </h1>

  <h3>
    Gabriel Cordeiro Moraes
  </h3>

  <p>
    Engenharia de Computação – Universidade Estadual de Feira de Santana (UEFS)
    Av. Transnordestina, s/n, Novo Horizonte
    Feira de Santana – BA, Brasil – 44036-900
  </p>

  <center>gcmorais66@gmail.com</center>

</div>

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
  É possivel visualizar através da imagem que o sistema inicia o processo de comunicação quando um um sensor RFID identifica uma ou mais TAGs RFID e envia essa(s) TAGs via socket para o caixa que está conectado ao leitor RFID. O caixa por sua vez, além de está conectado ao sensor RFID também está conectado a um servidor intermediário por meio de socket.
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
  O fluxo operacional destinado ao cliente inclui: digitar via terminal o endereço IP no qual o socket_server foi inicializado, após inserir o endereço do servidor é possível acessar uma interface que possibilita ao usuário iniciar uma compra ou sair do sistema, conforme a imagem abaixo:
</p>

![Menu inicial do caixa.](https://github.com/bielcmoraes/Concorrencia-e-Conectividade/blob/main/images_README/menu_inical_client.png)

<p style="text-align: justify;">
  Ao escolher iniciar uma compra é possível acessar o menu de compras onde o usuário deve escolher entre digitar o código de um produto manualmente, ler os produtos utilizandos as TAGs RFID atraves do sensor ou finalizar a compra e retornar ao menu anterior, conforme a imagem:
</p>

![Menu de compra do caixa.](https://github.com/bielcmoraes/Concorrencia-e-Conectividade/blob/main/images_README/menu_compra_client.png)

<p style="text-align: justify;">
  Para o administrador/gerente do sistema as funcionalidades estão disponíveis utilizando requisições HTTP que podem ser feitas utilizando softwares como Postman e Insomnia.
  Disponibilizar as funcionalidades via requisições HTTP elimina a necessidade de uma interface exclusiva para para gerenciamento do sistema e possibilita aos administrador acessar informações e detalhes sobre cada caixa como o IP e o status (bloqueado ou desbloqueado), o histórico de compras de cada caixa e o estoque de produtos do sistema, podendo visualizar o estoque de todos os produtos ou de um produto específico por meio de seu código.
  Para além, é possível bloquear e desbloquear os caixas a qualquer momento e limpar um carrinho da compra em andamento.
</p>

<p style="text-align: justify;">
  Entretanto, no terminal do administrador do sistema, adicionalmente, foi desenvolvida uma interface que possibilita ao gerente do sistema bloquear um caixa através do seu endereço IP, visualizar todas as mensagens trocados pelo servidor com todos os caixas, visualizar as mensagens trocadas com um caixa específico, além de encerrar o servidor socket, conforme a imagem abaixo: 
</p>

![Menu de compra do caixa.](https://github.com/bielcmoraes/Concorrencia-e-Conectividade/blob/main/images_README/menu_server_socket.png)

<p style="text-align: justify;">
  É importante salientar que o sistema oferece o controle automático de estoque dos produtos comprados não permitindo a compra de produtos que não estejam em estoque ou estajam esgotados.
  Além disso, erros e inconsistências são tratados de maneira adequada, oferecendo feedback aos usuários nas diferentes camadas do sistemas (caixas e administrador).
  Toda a comunicação entre as partes do sistema é feita utilizando JavaScript Object Notation (JSON) o que possibilita a escalabilidade do sistema e a facilita a comunicação com outras interfaces e outros sistemas caso necessário.
  Oferecendo segurança, robustez e interfaces amigáveis e escaláveis, o sistema permite aos clientes (usuários dos caixas) realizarem compras com facilidade ao mesmo tempo que oferece várias ferramentas para os gerentes do sistema admistrarem as operações dos vários caixas de maneira eficientes. 
</p>

# 4. Conclusão

<p style="text-align: justify;">
  Com a finalização do projeto foi possível identificar e explorar os conceitos básicos envolvidos na comunicação entre computadores em uma rede local por meio da tecnologia de comunicação via socket.
  Ao trabalhar com a tecnologia de RFID utilizando a Raspberry Pi ficaram claros o poder e a importância dos mini-computadores, além de aumentar a compreensão sobre tecnologias e soluções emergentes para problemas relacionados a Internet das Coisas (IoT) e rede de computadores.
  Para além, foram ampliados conhecimentos sobre tecnologias bastante importantes para o cenário atual e futuro da computação, a exemplo do Docker que além de facilita o controle do comportamento de aplicações em diferentes sistemas operacionais, visto que, tem a capacidade de empacotar todas as dependências do aplicativo desenvolvido em um único contêiner.
</p>

<p style="text-align: justify;">
  Todos os os requisitos do sistema foram cumpridos: por parte dos clientes (usuários do caixa) é possível realizar compras utilizando o sensor e as TAGs RFID. Por parte dos administradores/gerentes do sistema é possivel bloquear caixas, acompanhar compras em tempo real, consultar o historico de compras e visualizar informações detalhadas de cada caixa.
</p>

<p style="text-align: justify;">
  As possíveis melhorias que podem ser implementadas no sistema perpassam por duas das camadas implementadas no sistema: na camada do cliente é sugerível implementar um sensor RFID exclusivo para cada caixa, aumentando o fluxo de compras e melhorando a experiência dos usuários. Já na camada do servidor socket é interessante avaliar cuidadosamente a abordagem adotada para o servidos, pois a implementação atual cria uma thread para cada caixa conectado ao sistema e a quantidade de caixas conectados e o desempenho do servidor passa a depender da capacidade de hardware do mesmo, entretanto avaliou-se a possibilidade de implementar um buffer de solicitações para os caixas, que a depender do hardware poderia fazer o servidor perder desempenho mas garantiria que todas as solicitações seriam atendidas, além de fornecer um controle melhor da quantidade de threas que estariam gerenciando as solicitações dos caixas.
</p>

# Referências

<p style="text-align: justify;">
  Introdução a Sockets em Python. Disponível em: https://medium.com/@urapython.community/introdu%C3%A7%C3%A3o-a-sockets-em-python-44d3d55c60d0. Acesso em: 22 de agosto de 2023.
</p>

<p style="text-align: justify;">
  threading — Thread-based parallelism.  Python Software Foundation. 2023. Disponível em: https://docs.python.org/3/library/threading.html. Acesso em: 22 de agosto de 2023.
</p>

<p style="text-align: justify;">
  ANDRADE, Thiago. Programação Concorrente Utilizando Múltiplas Threads em Python. Revelo Community. 2023. Disponível em: https://community.revelo.com.br/programacao-concorrente-utilizando-multiplas-threads-em-python/. Acesso em: 22 de agosto de 2023.
</p>

<p style="text-align: justify;">
  http.server — HTTP servers.  Python Software Foundation. 2023. Disponível em: https://docs.python.org/3/library/http.server.html. Acesso em: 23 de agosto de 2023.
</p>

<p style="text-align: justify;">
  Guia de início rápido.  Kenneth Reitz. 2013. Disponível em: https://requests.readthedocs.io/projects/pt/pt_BR/latest/user/quickstart.html. Acesso em: 23 de agosto de 2023.
</p>
