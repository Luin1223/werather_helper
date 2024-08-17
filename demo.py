import requests
import json

def get_data():
    url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001"
    params = {
        "Authorization": "CWA-AEA3C5F8-511C-4D27-ADAF-2ED06B7E8918",  # 替換為實際的API授權碼
        "locationName": "臺北市"  # 替換為實際的城市名稱，如 "Taipei"
    }

    response = requests.get(url, params=params)
    print(response.status_code)

    if response.status_code == 200:
        # 解析JSON數據
        data = json.loads(response.text)

        # 提取所需信息
        location = data["records"]["location"][0]["locationName"]
        weather_elements = data["records"]["location"][0]["weatherElement"]
        
        start_time = weather_elements[0]["time"][0]["startTime"]
        end_time = weather_elements[0]["time"][0]["endTime"]
        weather_state = weather_elements[0]["time"][0]["parameter"]["parameterName"]
        rain_prob = weather_elements[1]["time"][0]["parameter"]["parameterName"]
        min_tem = weather_elements[2]["time"][0]["parameter"]["parameterName"]
        comfort = weather_elements[3]["time"][0]["parameter"]["parameterName"]
        max_tem = weather_elements[4]["time"][0]["parameter"]["parameterName"]

        # 將提取的信息作為列表返回
        return [location, start_time, end_time, weather_state, rain_prob, min_tem, comfort, max_tem]

    else:
        print("Can't get data!")
        return []  # 返回空列表，表示未獲取到數據


def line_notify(data):
    token = "rdzUMTrD2Ce5UPj14G3Q0LQqa9kQHEzVAqqrv3VBhQP"  # 替換為你的LINE Notify權杖
    message = ""

    if len(data) == 0:
        message += "\n[Error] 無法取得天氣資訊"
    else:
        message += f"\n今天{data[0]}的天氣: {data[3]}\n"
        message += f"溫度: {data[5]}°C - {data[7]}°C\n"
        message += f"降雨機率: {data[4]}%\n"
        message += f"舒適度: {data[6]}\n"
        message += f"時間: {data[1]} ~ {data[2]}\n"

        # 判斷天氣情況並添加提示
        if int(data[4]) > 70:
            message += "\n提醒您，今天很有可能會下雨，出門記得帶把傘哦!"
        elif int(data[7]) > 33:
            message += "\n提醒您，今天很熱，外出要小心中暑哦~"
        elif int(data[5]) < 10:
            message += "\n提醒您，今天很冷，記得穿暖一點再出門哦~"

    # LINE Notify 所需的資料
    line_url = "https://notify-api.line.me/api/notify"
    line_header = {
        "Authorization": 'Bearer ' + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    line_data = {
        "message": message
    }

    # 發送 POST 請求
    response = requests.post(url=line_url, headers=line_header, data=line_data)

    if response.status_code == 200:
        print("訊息已成功發送到 LINE!")
    else:
        print(f"無法發送訊息到 LINE，狀態碼: {response.status_code}")


# 結合調用
weather_data = get_data()  # 獲取天氣數據
line_notify(weather_data)  # 發送通知

