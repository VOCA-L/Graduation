#############################################
# 2022-05-01
# Insert data to database
##############################################
import socket
import sqlControler
from trainingAlgorithm import traingAlgorithm as tr

# 서버가 받을 Ip_addr, port
HOST = '192.168.0.17'
PORT = 1522

# 소켓 생성 및 바인딩
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))
print("Starting UDP server 4 ard")

# 메인 기능
def sendMode(mode):
    data = ''
    if mode == 0:
        last_step_per_finger = sqlControler.sqlControler.getLastStatus(mode)
        for step in last_step_per_finger:
            data= data + str(step)
            
    elif mode == 1:
        last_step = sqlControler.sqlControler.getLastStatus(mode)
        data = data + str(last_step)
    
    elif mode == 2:
        step_req = sqlControler.sqlControler.getLastStatus(mode)
        step = str(step_req[0]); req_cnt = str(step_req[1]); req_set = str(step_req[2])
        data = data + step + req_cnt + req_set
    return data
    
    
while True:
    # 아두이노로 부터 연결 수신
    msg, addr = sock.recvfrom(2048)
    print(msg.decode(), addr)

    ard_msg = msg.decode()

    # "p" 가장 최신 모드 반환
    if ard_msg == 'p':
        mode = sqlControler.sqlControler.getPreviousMode()
        print(f'mode is {mode}') # 최근 모드 확인
        data = 'm' + str(mode) + 's'
        data = data + sendMode(mode)
        sock.sendto(data.encode(), addr)
        print(f'send {data} message to ard')

    elif ard_msg[0] == 'c':
        mode = int(ard_msg[1])
        data = 'm' + str(mode) + 's'
        data = data + sendMode(mode)
        sock.sendto(data.encode(), addr)
        print(f'send {data} message to ard by ard req')
        
    else:
        # 데이터 삽입
        data = ard_msg.split('?')
        mode = data[0]
        print(data)
        if mode == '0':
            s1, s2, s3, s4, s5 = data[1], data[2], data[3], data[4], data[5]
            scc1, scc2, scc3, scc4, scc5 = data[6], data[7], data[8], data[9], data[10]
            ex_time = data[11]
            sqlControler.sqlControler.insertPssvData(mode, s1, s2, s3, s4, s5, scc1, scc2, scc3, scc4, scc5, ex_time)
        elif mode == '1':
            now_step, scc, ex_time = data[1], data[2], data[3]
            sqlControler.sqlControler.insertAutoData(mode, now_step=now_step, scc=scc, ex_time=ex_time)
        elif mode == '2':
            now_step, req_cnt, req_set = data[1], data[2], data[3]
            scc1, scc2, scc3, scc4 = data[4], data[5], data[6], data[7]
            stime1, stime2, stime3, stime4 = data[8], data[9], data[10], data[11]
            means, mean2, mean3, mean4 = data[12], data[13], data[14], data[15]
            for i in range(4):
                if (data[16 + i] == 99):
                    data[16 + i] = 0
            diff, diff2, diff3, diff4 = data[16], data[17], data[18], data[19]
            sqlControler.sqlControler.insertTrnData(mode, now_step, req_cnt, req_set, scc1, scc2, scc3, scc4,  stime1, stime2, stime3, stime4)
            sqlControler.sqlControler.insertAlgoData(means, mean2, mean3, mean4, diff, diff2, diff3, diff4)
            tr.cal()
            
            
            
