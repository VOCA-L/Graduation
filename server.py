#############################################
# 2022-05-04 server
# using sqlControler
# fin
##############################################
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import csv
import socket
import urllib.parse as urlparser
from urllib.parse import unquote
from sqlControler import sqlControler
from koreanNLP import kNLP

JSONTYPE = 'Application/json'
HOST = '192.168.0.17' # Open IP_ADDR
PORT = 2017           # Open PORT 

class requestHandler(BaseHTTPRequestHandler):
        
    f = open('order.csv', 'r', encoding='utf-8')
    dict_reader= csv.reader(f)
    dict_msg = { rows[0]: rows[1] for rows in dict_reader }
    dict_msg['0'] = 'error'
    
    def _set_headers(self):
        self.send_response(200) # 200 OK
        self.send_header('Content-Type', JSONTYPE) # content type
        self.end_headers() # header finish
        
    def _sendMode(self, mode):
        dt = ''
        if mode == 'manual' or mode == 2:
            mode = '0'
            dt = mode + 's'
            each_step = sqlControler.getLastStatus(0)
            print(each_step)
            for i in each_step:
                dt = dt + str(i)
        elif mode == 'auto' or mode == 1:
            mode = '1'
            dt = mode + 's'
            step = sqlControler.getLastStatus(1)
            print(step)
            dt = dt + str(step)
        elif mode == 'train' or mode == 3:
            mode = '2'
            dt = mode + 's'
            step_req = sqlControler.getLastStatus(2)
            print(step_req)
            step = str(step_req[0]); req_cnt = str(step_req[1]); req_set = str(step_req[2])
            dt = dt + step + req_cnt + req_set
        return dt
    
        
    def do_GET(self):
        querypath = urlparser.urlparse(self.path)
        path = querypath.path  
        print(f'Total path: {path}')
        user_path = path.split('/')[1]
        print(f'User path: {user_path}')
        
        if user_path == 'get': # Return 10 latest data for that mode
            if path.endswith('/passive'):
                body = { 'total': sqlControler.getManual() }
            elif path.endswith('/auto'):
                body = { 'total': sqlControler.getAutomatic() }
            elif path.endswith('/training'):
                body = { 'total': sqlControler.getTraining() }
            body = json.dumps(body, indent=4, sort_keys=True, default=str)
            self._set_headers()
            self.wfile.write(body.encode())
            print(f'Complete send 10 data {user_path}')
        
        elif user_path == 'set': # Adjust the tension on the finger       
            finger, tension = path.split('/')[2], path.split('/')[3]
            data = 's' + finger + tension
            print(data)
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(data.encode(), ("192.168.0.130", 2390))
            sock.close()
            self._set_headers()
            print(f'Complete {user_path} {data}')
        
        elif user_path == 'chmode': # Change mode
            mode = path.split('/')[2]
            data = 'm'
            dt = self._sendMode(mode)
            print(dt)
            data = data + dt
            print(data)
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(data.encode(), ("192.168.0.130", 2390))
            sock.close()
            self._set_headers()
            print(f'Complete {user_path}')
            
        elif user_path == 'voice':
            korean = path.split('/')[2]
            decoded_korean = unquote(korean, encoding='utf-8') # e.g. 엄지+손가락+3단계
            decoded_korean = decoded_korean.split('+')         # e.g. (엄지, 손가락, 3단계)
            decoded_korean = ''.join(decoded_korean)           # e.g. 엄지손가락3단계
            print(decoded_korean)
            dict_num = {
                '1': '일', 
                '2': '이', 
                '3': '삼',
                '4': '사', 
                '5': '오', 
                '6': '육',
                '7': '칠', 
                '8': '팔',   
                '9': '구',
                '10': '십'
            }
            for key in dict_num:
                if (decoded_korean.find(key)):
                    decoded_korean = decoded_korean.replace(key, dict_num[key])
            print(decoded_korean)
            msg = kNLP(decoded_korean)
            print(msg)
            if (msg == 1 or msg == 2 or msg == 3):
                data = 'm'
                dt = self._sendMode(msg)
                data = data + dt
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto(data.encode(), ("192.168.0.130", 2390))
                sock.close()
                self._set_headers()
                print(f'Complete NLP')
            elif (msg == 0 or msg == 4 or msg == 5):
                print("Error")
                self.send_response(400) # 400 Bad Request
                self.send_header('Content-Type', JSONTYPE) # content type
                self.end_headers() # header finish
            else:
                msg = str(msg)
                print(msg)
                data = requestHandler.dict_msg[msg]
                finger, tension = data[0], data[1]
                data = 's' + finger + tension
                print(data)
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto(data.encode(), ("192.168.0.130", 2390))
                sock.close()
                self._set_headers()
                print(f'Complete NLP finger tension')
                
                      
        elif user_path == 'start':
            sqlControler.iniTrn()
            step, req_count, req_set = sqlControler.getNext()
            if req_count == 9:
                req_count = '1'
            elif req_count == 12:
                req_count = '2'
            elif req_count == 15:
                req_count = '3'
            data = 'm' + '2' + 's' + str(step) + req_count + str(req_set)
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(data.encode(), ("192.168.0.130", 2390))
            sock.close()
            self._set_headers()
            print(f"Success:: step: {step}, r_cnt: {req_count}, r_set: {req_set}")
                
                            
try:            
    print("Starting HTTP server....")
    HTTPServer((HOST, PORT), requestHandler).serve_forever()
except KeyboardInterrupt:
    print("Closed HTTP Server!!! Thank you.")
