import pymysql
import pymysql.cursors

connection = pymysql.connect(host='localhost', user='test_root', password='20171522',
                            db='test_tb', charset='utf8', cursorclass=pymysql.cursors.DictCursor) # connenct db
cursor = connection.cursor()

class sqlControler():
    def __init__(self):
        print("Making sql controler")
        
    ## 애플리케이션 (viewer) 데이터 요청시
    def getManual():
        sql = "SELECT * FROM _intergration WHERE mode = 0 ORDER BY date_time  DESC LIMIT 10;"
        cursor.execute(sql) # send sql line to db server 
        data = cursor.fetchall()
        return data
    def getAutomatic():
        sql = "SELECT * FROM _intergration WHERE mode = 1 ORDER BY date_time  DESC LIMIT 10;"
        cursor.execute(sql) # send sql line to db server 
        data = cursor.fetchall()
        return data
    def getTraining():
        sql = "SELECT * FROM _intergration WHERE mode = 2 ORDER BY date_time  DESC LIMIT 10;"
        cursor.execute(sql) # send sql line to db server 
        data = cursor.fetchall()
        return data

    ## 아두이노 직전 모드 요청시
    def getPreviousMode():
        sql = "SELECT mode FROM _intergration ORDER BY date_time DESC LIMIT 1"
        cursor.execute(sql)
        data = cursor.fetchone()
        mode = data["mode"]
        return mode
    
    ## 아두이노 혹은 애플리케이션 모드 전환시 바꾼 모드의 최신 상태 반환
    def getLastStatus(mode):
        if mode == 0:
            sql = "SELECT s1, s2, s3, s4, s5 FROM _intergration WHERE mode = 0 ORDER BY date_time DESC LIMIT 1"
            cursor.execute(sql)
            data = cursor.fetchone()
            step = data["s1"], data["s2"], data["s3"], data["s4"], data["s5"]
            return step
        elif mode == 1:
            sql = "SELECT now_step FROM _intergration WHERE mode = 1 ORDER BY date_time DESC LIMIT 1"
            cursor.execute(sql)
            data = cursor.fetchone()
            step = data["now_step"]
            return step
        elif mode == 2:
            sql = "SELECT step, req_count, req_set FROM _next ORDER BY date_time DESC LIMIT 1"
            cursor.execute(sql)
            data = cursor.fetchone()
            dt = data['req_count']
            if (dt == 9):
                dt = 1
            elif (dt == 12):
                dt = 2
            elif (dt == 15):
                dt = 3
            step = data["step"], dt, data["req_set"]
            return step
    
        
               
    ## 아두이노의 (viewer)데이터 삽입
    # 수동 모드 데이터 추가
    def insertPssvData(mode, s1, s2, s3, s4, s5, scc1, scc2, scc3, scc4, scc5, ex_time): # 수동 모드
        print(mode, s1, s2, s3 ,s4 ,s5, ex_time)
        sql = "INSERT INTO _intergration(mode, date_time, s1, s2, s3, s4, s5, scc1, scc2, scc3, scc4, scc5, ex_time) \
            VALUES(%s, now(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (mode, s1, s2, s3, s4, s5, scc1, scc2, scc3, scc4, scc5, ex_time))
        connection.commit() 
        print(f"Success {mode}: {s1}, {s2}, {s3}, {s4}, {s5}, {scc1}, {ex_time}")
    
    # 자동 모드 데이터 추가
    def insertAutoData(mode, now_step, scc, ex_time): # 자동 모드
        sql = "INSERT INTO _intergration(mode, date_time, scc, now_step, ex_time) \
            VALUES(%s, now(), %s, %s, %s)"
        cursor.execute(sql, (mode, scc, now_step, ex_time))
        connection.commit()
        print(f"Success {mode}: {scc}, {now_step}, {ex_time}")
    
    # 트레이닝모드 데이터 추가
    def insertTrnData(mode, now_step, req_count, req_set, scc1, scc2, scc3, scc4, set_time1, set_time2, set_time3, set_time4): # 트레이닝 모드
        sql = "INSERT INTO _intergration(mode, date_time, now_step, req_count, req_set, scc, scc1, scc2, scc3, scc4, set_time1, set_time2, set_time3, set_time4, ex_time) \
            VALUES(%s, now(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        ex_time = int(set_time1) + int(set_time2) + int(set_time3) + int(set_time4)
        scc = int(scc1) + int(scc2) + int(scc3) + int(scc4)
        cursor.execute(sql, (mode, now_step, req_count, req_set, scc, scc1, scc2, scc3, scc4, set_time1, set_time2, set_time3, set_time4, ex_time))
        connection.commit()
        print(f"Success {mode}: {now_step}, {ex_time}")
        
    # 트레이닝 알고리즘의 데이터 읽기
    def readDataForTR(): 
        sql = "SELECT * FROM _trndata ORDER BY date_time DESC LIMIT 1"
        cursor.execute(sql)
        data = cursor.fetchone()
        return data
    
    def getTrainingData():
        sql = "SELECT * FROM _intergration WHERE mode = 2 ORDER BY date_time  DESC LIMIT 1;"
        cursor.execute(sql) # send sql line to db server 
        data = cursor.fetchall()
        return data

    
    ## 트레이닝 알고리즘에 필요한 데이터 삽입
    def insertAlgoData(means, mean2, mean3, mean4, diff, diff2, diff3, diff4):
        sql = "INSERT INTO _trndata(date_time, mean, mean2, mean3, mean4, diff, diff2, diff3, diff4) \
            VALUES(now(), %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (means, mean2, mean3, mean4, diff, diff2, diff3, diff4))
        connection.commit()
        print(f"Success insert trn data to db")
    
    # 다음 트레이닝을 위한 조건 삽입
    def nextTrn(step, req_count, req_set):
        sql = "INSERT INTO _next(step, date_time, req_count, req_set) \
            VALUES(%s, now(), %s, %s)"
        cursor.execute(sql, (step, req_count, req_set))
        connection.commit()
        print(f"Success insert data for next training to db")
    
    # 다음 트레이닝 조건 
    def getNext():
        sql = "SELECT * FROM _next ORDER BY date_time DESC LIMIT 1"
        cursor.execute(sql)
        data = cursor.fetchone()
        return data['step'], data['req_count'], data['req_set']
    
    ## 트레이닝 모드 초기화
    def iniTrn():
        sql = "DELETE FROM _next"
        cursor.execute(sql)
        sql = "DELETE FROM _intergration WHERE mode = 2"
        cursor.execute(sql)
        sql = "INSERT INTO _next(step, date_time, req_count, req_set) \
            VALUES(%s, now(), %s, %s)"
        cursor.execute(sql, (0, 9, 2))
        connection.commit()
        print(f"Success Initialization")
        
    
    
        
