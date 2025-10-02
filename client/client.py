import socket, msvcrt
client = socket.socket()
client.connect(('localhost', 12345))

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
        question = question[:-4]
        print(question)
        print("press the corresponding letter on your keyboard!\n\n")
        while True:
            key = msvcrt.getch().decode().upper()
            if key in ['A','B','C','D']:
                client.send(key.encode())
                print(f"you have chosen {key}")
                break
        feedback = client.recv(1024).decode()
        print(feedback)
        
    else:
        print(question)



