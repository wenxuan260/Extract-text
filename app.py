from flask import Flask, request, jsonify
import re

app = Flask(__name__)

@app.route('/extract_trip_data', methods=['POST'])
def extract_trip_data():
    data = request.get_json()
    full_text = data.get("text", "")

    # 驾驶人
    driver_match = re.search(r"(\S+)", full_text)
    driver_name = driver_match.group(1) if driver_match else "未识别"

    # 日期时间
    date_time_match = re.search(r"(\d{4}\.\d{2}\.\d{2})\s*(\d{2}:\d{2})", full_text)
    date_time_str = f"{date_time_match.group(1)} {date_time_match.group(2)}" if date_time_match else "未匹配"

    # 行驶里程
    distance_match = re.search(r"(\d+(?:\.\d+)?)\s*km(?!/h)", full_text)
    distance = distance_match.group(1) if distance_match else "未匹配"

    # 驾驶时长
    duration_match = re.search(r"(\d+:\d+:\d+)", full_text)
    duration = duration_match.group(1) if duration_match else "未匹配"

    # 出发地和目的地
    locations = re.findall(r"([\u4e00-\u9fa5]+(?:（.*?）)?)", full_text)
    start_location = locations[-2] if len(locations) >= 2 else "未识别"
    end_location = locations[-1] if len(locations) >= 2 else "未识别"

    # 返回结构化 JSON 数据
    result = {
        "driver_name": driver_name,
        "date_time": date_time_str,
        "distance_km": distance,
        "duration": duration,
        "start_location": start_location,
        "end_location": end_location
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
