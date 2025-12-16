# Chat Multiusuário com WebSockets (Equipe 11)
Este projeto consiste na implementação de um sistema de chat cliente-servidor utilizando **WebSockets**. O sistema permite que múltiplos clientes troquem mensagens em uma sala única e que cada novo participante receba o histórico recente de conversas ao entrar.

Desenvolvido para a disciplina CIN0143 - Introdução aos Sistemas Distribuídos e Redes de Computadores.

## 📋 Funcionalidades
- **Comunicação via WebSocket:** O WebSocket permite comunicação bidirecional persistente entre cliente e servidor, facilitando o envio e o recebimento de mensagens em tempo real.
- **Broadcast de Mensagens:** Sempre que o servidor recebe uma mensagem de um cliente, ele retransmite (broadcast) a todos os demais clientes ativos.
- **Histórico de Mensagens:** O servidor mantém em memória as últimas N mensagens enviadas.
Quando um cliente envia o comando de conexão (`CONNECT <nome>`), o servidor envia esse histórico completo para ele antes de transmitir novas mensagens.
- **Protocolo de Aplicação Manual:** O sistema implementa um protocolo textual simples com três comandos (`CONNECT <nome>`, `SEND <mensagem>`, `DISCONNECT`). Cada comando é enviado via WebSocket para o servidor.

## 📂 Estrutura do Projeto
- `servidor.py:` Cria o servidor WebSocket, recebe mensagens, mantém o histórico e faz broadcast para os clientes conhecidos.
- `cliente.py:` Interface que envia comandos via WebSocket e recebe mensagens do servidor de forma contínua.
- `commands.py:` Constantes do protocolo de aplicação.
- `utils.py:` Utilitários para formatação e uso de cores no terminal.

## 🚀 Como Executar
### Pré-requisito
- Python 3 instalado.
- Biblioteca `websockets` instalada:
  ```
  pip install websockets
  ```

Obs: Aconselho utilizar *venv* para evitar conflitos.

### 🖥️ Iniciando o Servidor
No terminal execute:

```
python3 servidor.py
```

O servidor iniciará na porta padrão 5000 e ficará aguardando conexões WebSocket dos clientes.

### 👤 Iniciando um Cliente
Abra outro terminal (um para cada usuário) e execute:

```
python3 cliente.py
```

Após iniciar, o cliente poderá enviar comandos ao servidor.

### 📡 Uso do Protocolo
O chat funciona por meio de comandos textuais, que o usuário deve digitar exatamente desta forma:
- **Entrar no chat:** `CONNECT <seu_nome>` -> Registra o cliente no servidor e recebe o histórico recente.
- **Enviar mensagem:** `SEND <mensagem>` -> Envia uma mensagem para todos os participantes.
- **Sair:** `DISCONNECT` -> Remove o cliente da lista e encerra o programa localmente.

**Exemplo:**

```
CONNECT Sofia
SEND Olá, pessoal!
DISCONNECT
```
### ⚙️ Configurações
No arquivo servidor.py, é possível ajustar:
- **HOST:** Endereço IP do servidor (padrão: 'localhost')
- **PORT:** Porta WebSocket (padrão: 5000)
- **HISTORY_SIZE:** Quantidade de mensagens mantidas no histórico (padrão: 100)

### Interface Gráfica

Como um bônus, implementamos uma página html interativa para não ficarmos apenas no terminal. Usamos WebSockets com JavaScript embutido no html. Nada de outro mundo, só seguimos o mesmo fluxo do que escrevemos em python, transferindo toda as regras de comunicação(Ex: Comandos de SEND, CONNECT, DISCONNECT) para o script python. Usamos o JS apenas para abrir comunicação com o servidor.py.

### Como rodar a interface?

Execute o servidor normalmente

```
python3 servidor.py
```

Em seguida, sirva o html com os dados do servidor:

```
python3 -m http.server 8000 -d frontend
```

Caso a porta 8000 esteja em utilização, pode trocar para uma disponível.

## 👥 Autores — Equipe 11
Jorge Guilherme

José Janailson

Kleberson de Araujo

Lucas dos Santos

Sofia Ribeiro
