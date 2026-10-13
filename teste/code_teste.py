import asyncio
import os


rodando = True
pedidos = []

async def procces():
    global rodando

    with open("pedidos.txt", "a") as arquivo:
        while rodando:
            if pedidos:
                pedido = pedidos.pop(0)
                arquivo.write(pedido + "\n")
                arquivo.flush()  # Garante que o pedido seja escrito imediatamente
                print(f"Pedido '{pedido}' registrado no arquivo.")
            else:
                await asyncio.sleep(1)  # Espera um pouco antes de verificar novamente

    
async def get_orders():
    global rodando

    while rodando:
        # Usamos to_thread para que o input() não bloqueie o asyncio inteiro
        pedido = await asyncio.to_thread(input, "Ingrese un pedido (o 'sair' para terminar): ")
        
        if pedido.strip().lower() == 'sair':
            rodando = False
            print("\nEncerrando o sistema...")
            break
            
        if pedido.strip():
            pedidos.append(pedido.strip())

async def main():
    # Executa ambas as tarefas concorrentemente
    await asyncio.gather(get_orders(), procces())

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nPrograma interrompido pelo usuário.")
    except Exception as e:
        print(f"\nOcorreu um erro: {e}")