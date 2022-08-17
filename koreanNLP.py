import numpy as np
import joblib
import konlpy


# ard_dict = {0: "Error",
            # 1: ""}

base_tokenizer = joblib.load("base_tokenizer.pkl")
base_model = joblib.load("base_model.pkl")
passive_tokenizer = joblib.load("passive_tokenizer.pkl")
passive_model = joblib.load("passive_model.pkl")


def kNLP(nl):
    nl_data = nl;
    okt = konlpy.tag.Okt()
    data = okt.morphs(nl_data, norm=True, stem=True)
    data_parsed = base_tokenizer.texts_to_sequences(data)
    data_list_dic = []
    for i in range(len(data_parsed)):
        if len(data_parsed[i]) == 0:
            data_list_dic.append(0)
        else:
            data_list_dic.append(data_parsed[i][0])

    while(True):
        data_list_dic.append(0)
        if len(data_list_dic)>11:
            break

    data_list_dic = np.reshape(data_list_dic, (1, -1))
    result = int(base_model.predict(data_list_dic))
    
    
    
    if result==5:
        data_parsed = passive_tokenizer.texts_to_sequences(data)
        data_list_dic = []
        for i in range(len(data_parsed)):
            if len(data_parsed[i]) == 0:
                data_list_dic.append(0)
            else:
                data_list_dic.append(data_parsed[i][0])

        while(True):
            data_list_dic.append(0)
            if len(data_list_dic)>11:
                break

        data_list_dic = np.reshape(data_list_dic, (1, -1))
        result = int(passive_model.predict(data_list_dic)) + 5
        
    print(f"Result: {result}")
    return result
