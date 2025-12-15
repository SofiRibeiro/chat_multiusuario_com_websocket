import asyncio # Permite executar tarefas concorrentes sem bloquear
import websockets
from commands import Commands
from utils import printc, bcolors

# Configurações
HOST = "localhost"
PORT = 5000

async def receive_messages(ws):
    # Task que fica ouvindo mensagens do servidor
    try:
        async for msg in ws:
            print(msg)
    except websockets.exceptions.ConnectionClosed:
        printc("Conexão encerrada pelo servidor.", bcolors.FAIL)

async def send_messages(ws):
    # Task que lê o input do usuário e envia
    loop = asyncio.get_event_loop()

    while True:
        msg = await loop.run_in_executor(None, input)

        if not msg:
            continue

        await ws.send(msg)

        if msg.strip() == Commands.DISCONNECT:
            break

async def main():
    uri = f"ws://{HOST}:{PORT}" # Uniform Resource Identifier (endereço completo do WebSocket para se conectar com o servidor)

    try:
        async with websockets.connect(uri) as ws:
            printc("Conectado ao servidor WebSocket!", bcolors.OKGREEN)
            printc("Use os comandos:", bcolors.HEADER)
            printc(" - CONNECT <nome>")
            printc(" - SEND <mensagem>")
            printc(" - DISCONNECT")

            # Roda envio e recebimento
            await asyncio.gather(
                receive_messages(ws),
                send_messages(ws)
            )

    except Exception as e:
        printc(f"Erro de conexão: {e}", bcolors.FAIL)

if __name__ == "__main__":
    asyncio.run(main())