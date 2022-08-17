from statistics import mean
import sqlControler



class traingAlgorithm():
    def cal():
        cnt_score = 0; set_score = 0; time_score = 0;
        step_score = 0
        
        mean_diff = sqlControler.sqlControler.readDataForTR()
        means = mean_diff['mean']; mean2 = mean_diff['mean2']
        mean3 = mean_diff['mean3']; mean4 = mean_diff['mean4'] 
        diff = mean_diff['diff']; diff2 = mean_diff['diff2']
        diff3 = mean_diff['diff3']; diff4 = mean_diff['diff4']
        
        data = sqlControler.sqlControler.getTrainingData()
        data = data[0]
        ex_time = data['ex_time']; scc = data['scc']; now_step = data['now_step']
        req_cnt = data['req_count']; req_set = data['req_set'] 
        scc1 = data['scc1']; scc2 = data['scc2'];
        scc3 = data['scc3']; scc4 = data['scc4'];
        print(ex_time)
        # time1 = data['set_time1']; time2 = data['set_time2']
        # time3 = data['set_time3']; time4 = data['set_time4']
        
        mean_full = [means, mean2, mean3, mean4]
        diff_full = [diff, diff2, diff3, diff4]
        mean_full = mean_full[:req_set]
        diff_full = diff_full[:req_set]
        
        mean_scoring = mean_full[0] - mean_full[-1]
        diff_scoring = []
        for i in range(req_set):
            diff_scoring.append(diff_full[i] / mean_full[i])
        diff_scoring = mean(diff_scoring)
        
        print(mean_scoring)
        print(diff_scoring)
        
        if (mean_scoring < -10):
            cnt_score = cnt_score + 30
            set_score = set_score + 60
        elif (-10 <= mean_scoring and mean_scoring <= 10):
            cnt_score = cnt_score + 20
            set_score = set_score + 40
        elif (mean_scoring < 10):
            cnt_score = cnt_score + 10
            set_score = set_score + 20
        
        if (diff_scoring >= 0.75):
            cnt_score = cnt_score + 20
            set_score = set_score + 10
        elif (diff_scoring <= 0.75 and diff_scoring >= 0.5):
            cnt_score = cnt_score + 40
            set_score = set_score + 20     
        elif (diff_scoring < 0.5):
            cnt_score = cnt_score + 60
            set_score = set_score + 30
            
        time_scoring = ex_time / req_set
        
        if (req_cnt == 15):
            if (time_scoring < 15):
                time_score = 10
            elif (time_scoring <= 20 and time_scoring >= 25):
                time_score = 5
            elif (time_scoring > 25):
                time_score = 1
        elif (req_cnt == 12):
            if (time_scoring < 12):
                time_score = 10
            elif (time_scoring <= 15 and time_scoring >= 20):
                time_score = 5
            elif (time_scoring > 20):
                time_score = 1
        elif (req_cnt == 9):
            if (time_scoring < 9):
                time_score = 10
            elif (time_scoring >= 12 and time_scoring <= 15):
                time_score = 5
            elif (time_scoring > 15):
                time_score = 1

        set_score = set_score + time_score
        cnt_score = cnt_score + time_score
        print(set_score); print(cnt_score)
        
        if (set_score > 85):
            if (req_set == 4):
                next_set = req_set
                step_score = step_score + 1
            else:
                next_set =  req_set + 1
        elif (set_score < 65):
            if (req_set == 2):
                next_set = req_set
                step_score = step_score - 1
            else:
                next_set = req_set - 1
        elif (set_score >= 85 and set_score <= 65):
            next_set = req_set
            
        next_cnt = req_cnt
        next_set = req_set
        if (cnt_score > 85):
            if (req_cnt == 15):
                next_cnt = req_cnt
                step_score = step_score + 1
            else:
                next_cnt =  ((req_cnt / 3) + 1) * 3
        elif (cnt_score < 65):
            if (req_cnt == 9):
                next_cnt = req_cnt
                step_score = step_score - 1
            else:
                next_cnt = ((req_cnt / 3) - 1) * 3
        elif (cnt_score >= 85 and cnt_score <= 65):
            next_cnt = req_cnt
            
        if (step_score == 2):
            next_step = now_step + 1
        else:
            if (step_score == -2):
                next_step = now_step - 1
            else:
                next_step = now_step
            
        sqlControler.sqlControler.nextTrn(step=next_step, req_count=next_cnt, req_set=next_set)
    
    
