import socket, threading, json, random, time, sys, math

players = []
player_scores = {}
answered = {}
lock = threading.Lock()
player_ready = threading.Event()
player_start_time = {}
player_end_time ={}

with open("questions.json", "r") as f:
    all_questions = json.load(f)

def send_question(q):
    time.sleep(3)
    Text = (q["question"]+"\n"+"\n".join(q["options"])+"\n" + "test")
    for conn, name in players:
        conn.send(Text.encode())         

def quiz():
    for q in questions:
        with lock:
            answered.clear()
            
        send_question(q)
        quest_start_time = time.time()#nick
        print(f"Sent question: {q['question']}")
        time_start = time.time()
        
        while True:
            with lock:
                if len(answered) == len(players):
                    break
                
            if time.time() - time_start > 15:
                break
            
            time.sleep(0.1)
            
        with lock:
            for conn, name in players:
                if name not in answered:
                    answered[name] = "x"
                    player_end_time[name] = time.time()
                    
        with lock:
            for connection, name in players:
                ans = answered.get(name, "")
                duration = math.ceil(player_end_time[name] - quest_start_time)#nick
                
                if duration == 0:
                    scored = 1
                
                else:
                    scored = int(1 * (100/duration))#nick
                
                if ans == q["answer"]:
                    player_scores[name] += scored
                    connection.send(b"correct!\n")
                    connection.send(f'you scored: {scored} points'.encode())
                
                elif ans == "x":
                    connection.send(b"You didn't answer in time.\n")
                    connection.send(b"You scored: 0 points\n")
                
                else:
                    connection.send(b"wrong\n")
                    connection.send(f'you scored: 0 points'.encode())

    shutdown_server()
    
        
def clients(connection, address):
    print(f"Connected to {address}")
    connection.send(b"enter your player name: ")
    name = connection.recv(1024).decode().strip()    
    connection.send(f'Welcome, {name}!\n'.encode())
    
    with lock:
        players.append((connection, name))
        player_scores[name] = 0
    
        if len(players) >= expected_player_count:
            player_ready.set()
    
    while True:
        try:
            answer = connection.recv(1024).decode().strip()
    
            with lock:
                if name not in answered:
                    player_end_time[name] = time.time()#nick
                    
                    answered[name] = answer                
        except:
            break

server = socket.socket()
server.bind(('localhost', 12345))

server.listen()
print("server is waiting for connection")
questions = random.sample(all_questions, len(all_questions))
expected_player_count = 2

def accept_players():
    accepted = 0

    while accepted < expected_player_count:
        connection, address = server.accept()
        print(f"Accepted connection from {address}")
        thread = threading.Thread(target=clients, args=(connection, address))
        thread.start()
        accepted += 1

def shutdown_server():
    for conn, name in players:
        score = player_scores[name]

        try:
            conn.send(f"Game over! Your score: {score}\n".encode())
        except:
            pass

    time.sleep(1)  # Give clients time to receive the message

    for conn, _ in players:
        conn.close()

    server.close()
    print("Server shut down.")

accept_players()
player_ready.wait()

for conn, _ in players:
    conn.send(b"All players connected! Quiz starting...\n")

time.sleep(1)
quiz()