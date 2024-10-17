import socket

PORT = int(input('輸入你的port(10000-10050): '))

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

IPName = socket.gethostname()

IPName = IPName + '.cs.nycu.edu.tw'
IP = socket.gethostbyname(IPName)
s.bind((IP, PORT))

print('server start at: %s:%s' % (IP, PORT))
print('等待連接')

def cutName(message):
    name = ''
    for i in range(len(message)):
        if message[i] == ' ':
            break
        name += message[i]
    return name

def playGameWithClient(conn):
    choices = ['paper', 'rock', 'scissors']
    # server choice
    while True:
        server_choice = input("你要出什麼? (paper、rock、scissors): ")
        if server_choice in choices:
            break
        else:
            print("無效的選擇，請重新輸入。")

    # 寄給client
    conn.send(server_choice.encode())
    print('等待對方出拳...')
    client_choice = conn.recv(1024).decode()
    print(f'對方出了{client_choice}')
    print(judge_winner(server_choice, client_choice))

def judge_winner(server_choice, client_choice):
    if server_choice == client_choice:
        return "平手"
    elif (server_choice == 'scissors' and client_choice == 'paper') or \
         (server_choice == 'rock' and client_choice == 'scissors') or \
         (server_choice == 'paper' and client_choice == 'rock'):
        return "你贏了！"
    else:
        return "你輸了！"

while True:
    indata, addr = s.recvfrom(1024)
    message = indata.decode()
    if message == 'isOpen?':
        outdata = 'echo ' + indata.decode()
        s.sendto(outdata.encode(), addr)
        continue
    
    name = cutName(message)
    if message == f"{name} 想跟你玩遊戲！":
        print(f"收到來自 {name} 的邀請")
        response = input('是否接受邀請？(yes/no): ').lower()
        if response == 'yes':
            s.sendto('yes'.encode(), addr)
            client_port_data, _ = s.recvfrom(1024)
            client_port = int(client_port_data.decode())
            print(f"收到 client 的 TCP port: {client_port}")
            s.close()
            tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            tcp_socket.bind((IP, client_port))
            tcp_socket.listen(5)
            print(f"TCP 伺服器已啟動，等待來自 {name} 的連接...")
            conn, addr = tcp_socket.accept()
            
            playGameWithClient(conn)
            break

        else:
            s.sendto('no'.encode(), addr)
            continue

s.close()


