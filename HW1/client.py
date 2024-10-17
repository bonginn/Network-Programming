import socket
import time

HOST = ['140.113.235.151', '140.113.235.152', '140.113.235.153', '140.113.235.154']  
start_port = 10000  # 起始
end_port = 10050    # 結束

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(0.1) 

checkOpenMessage = b'isOpen?'

def listAllOpenPorts(checkHost):
    anyoneOpen = False
    for port in range(start_port, end_port + 1):
        server_addr = (checkHost, port)
        try:
            s.sendto(checkOpenMessage, server_addr)  
            indata, addr = s.recvfrom(1024)
            print(f'IP: {checkHost} Port {port} 正在等待遊戲邀請')
            anyoneOpen = True
        except socket.timeout:
            pass
    return anyoneOpen

def palyGameWithServer(tcp_socket):
    choices = ['paper', 'rock', 'scissors']

    # client choice
    while True:
        client_choice = input("你要出什麼? (paper、rock、scissors): ")
        if client_choice in choices:
            break
        else:
            print("無效的選擇，請重新輸入。")

    # 寄給server
    tcp_socket.send(client_choice.encode())
    print('等待對方出拳...')
    server_choice = tcp_socket.recv(1024).decode()
    print(f'對方出了{server_choice}')
    print(judge_winner(server_choice, client_choice))

def judge_winner(server_choice, client_choice):
    if server_choice == client_choice:
        return "平手"
    elif (server_choice == 'scissors' and client_choice == 'paper') or \
         (server_choice == 'rock' and client_choice == 'scissors') or \
         (server_choice == 'paper' and client_choice == 'rock'):
        return "你輸了！"
    else:
        return "你贏了！"

def sendInvite():
    # 輸入邀請對象
    server_ip = str(input("輸入你想邀請的對象IP: "))
    server_port = int(input("輸入你想邀請的對象Port: "))

    # 創建 UDP socket及姓名
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    name = input("輸入你的名字: ")

    # 發送邀請
    invite_message = f"{name} 想跟你玩遊戲！"
    udp_socket.sendto(invite_message.encode(), (server_ip, server_port))
    print('等待對方回應中...')
    
    # 接收回應
    response, _ = udp_socket.recvfrom(1024)
    response_message = response.decode()

    if response_message == 'yes':
        print('對方接受了你的邀請！')
        # 輸入自己的 TCP port
        client_port = int(input('輸入你的TCP port: '))
        udp_socket.sendto(str(client_port).encode(), (server_ip, server_port))
        udp_socket.close()

        # 建立 TCP 連接
        time.sleep(1)
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.connect((server_ip, client_port))
        print('成功連接！遊戲準備開始...')
        palyGameWithServer(tcp_socket)
        
    else:
        print('對方拒絕了你的邀請：（')
        udp_socket.close()

if __name__ == "__main__":
    anyOne = False
    for checkHost in HOST:
        anyOne = listAllOpenPorts(checkHost) or anyOne
    if not anyOne:
        print('目前沒有人想要玩遊戲')
    else:
        sendInvite()