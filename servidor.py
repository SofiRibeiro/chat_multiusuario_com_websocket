import asyncio # Permite executar tarefas concorrentes sem bloquear
import websockets
from collections import deque
from commands import Commands
from utils import printc, bcolors

# Configurações
HOST = "localhost"
PORT = 5000
HISTORY_SIZE = 100 # Histórico armazena até 100 mensagens

# Estruturas globais
clients = {}  # { websocket : username }
message_history = deque(maxlen=HISTORY_SIZE)

async def broadcast_except(message, excluded_ws):
    # Envia a mensagem para todos os clientes menos quem enviou
    for ws in list(clients.keys()):
        if ws != excluded_ws:
            try:
                await ws.send(message)
            except:
                pass

async def handle_client(websocket):
    # Lida com a conexão e a lógica de mensagens
    printc("Novo cliente conectado (WebSocket)", bcolors.OKCYAN)
    username = None

    try:
        async for msg in websocket:
            parts = msg.split(" ", 1)
            command = parts[0]
            content = parts[1] if len(parts) > 1 else ""

            # Comando CONNECT
            if command == Commands.CONNECT:
                username = content
                clients[websocket] = username

                printc(f"Usuário registrado: {username}", bcolors.OKGREEN)

                # Envia histórico para quem entrou
                if message_history:
                    hist = "\n--- Histórico das últimas mensagens --- \n"
                    for m in message_history:
                        hist += m + "\n"
                    await websocket.send(hist)

                # Avisar os outros usuários
                await broadcast_except(
                    f"Servidor: {username} entrou no chat.",
                    websocket
                )

            # Comando SEND
            elif command == Commands.SEND:
                if not username:
                    await websocket.send(
                        f"{bcolors.WARNING}Servidor: use CONNECT antes de enviar mensagens.{bcolors.ENDC}"
                    )
                    continue

                final_msg = f"{username}: {content}"

                # Salva no histórico
                message_history.append(final_msg)

                # Envia apenas para demais usuários
                await broadcast_except(final_msg, websocket)

                print(final_msg)

            # Comando DISCONNECT
            elif command == Commands.DISCONNECT:
                break

    except websockets.exceptions.ConnectionClosed:
        pass

    finally:
        if websocket in clients:
            name = clients[websocket]
            del clients[websocket]

            printc(f"{name} desconectou", bcolors.WARNING)

            # Avisar os usuários da desconexão
            await broadcast_except(
                f"Servidor: {name} saiu do chat.",
                websocket
            )

async def main():
    async with websockets.serve(handle_client, HOST, PORT):
        printc(
            f"Servidor WebSocket rodando em {HOST}:{PORT}",
            bcolors.HEADER
        )
        printc(
            f"Histórico configurado para {HISTORY_SIZE} mensagens",
            bcolors.OKBLUE
        )
        await asyncio.Future()  

if __name__ == "__main__":
    asyncio.run(main())