import socket, msvcrt, time, os

client = socket.socket()
client.connect(('localhost', 12345))
os.system('cls')

prompt = client.recv(1024).decode()

while True: #Namira
    player_name = input(prompt)
    
    if not player_name.isalpha():
        print("Deze naam is niet geldig, alleen letters zijn toegestaan.")
    
    elif not 2<= len(player_name) <= 15:
        print("Deze naam is te kort het moet tussen 2 en 15 letters zijn.")
    
    else:
        break

client.send(player_name.encode())
print("")
print("")

while True:
    try:
        question = client.recv(1024).decode()

    except ConnectionResetError:
        print("Connection lost. Server may have closed.")
        break
    
    if "END" in question or "Game over" in question:
        print(question)
        break

    elif "test" in question:
        os.system('cls')
        question = question[:-4]
        print(question)
        
        start_time = time.time()
        timeout = 15 # in seconden 

        while True:
            elapsed = time.time() - start_time
            remaining_time = int(timeout - elapsed)
            print(f'\rTime left: {remaining_time: 2d} seconds | press one of the answer keys', end='', flush=True)

            if msvcrt.kbhit():
                key = msvcrt.getch().decode().upper()

                if key in ['A','B','C','D']:
                    client.send(key.encode())
                    print(f"\nyou have chosen {key}")
                    break

            if elapsed > timeout:
                client.send(b"x")                
                break

            time.sleep(0.1)

        feedback = client.recv(1024).decode()
        print(feedback)
        
    elif not "All players connected" in question:
        print(question)
  
    elif "All players connected" in question:
        time.sleep(2)
        os.system('cls')
        print(question)