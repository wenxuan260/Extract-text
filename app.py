from flask import Flask, request, jsonify
import re

app = Flask(__name__)

@app.route('/extract_trip_data', methods=['POST'])
def extract_trip_data():
    # 1. 获取纯文本内容
    full_text = request.get_data(as_text=True)

    # 2. 提取驾驶人
    driver_match = re.search(r"^(\S+)", full_text)
    driver_name = driver_match.group(1) if driver_match else "未识别"

    # 3. 提取日期和时间
    date_time_match = re.search(r"(\d{4}\.\d{2}\.\d{2})\s+(\d{2}:\d{2})", full_text)
    date_time = f"{date_time_match.group(1)} {date_time_match.group(2)}" if date_time_match else "未识别"

    # 4. 提取行驶里程（单位为 km）
    distance_match = re.search(r"(\d+(?:\.\d+)?)\s*km(?!/h)", full_text)
    distance_km = distance_match.group(1) if distance_match else "未识别"

    # 5. 提取驾驶时长（格式如 00:26:48）
    duration_match = re.search(r"(\d{2}:\d{2}:\d{2})", full_text)
    duration = duration_match.group(1) if duration_match else "未识别"

    # 6. 提取出发地和目的地（默认取最后两个中文字段）
    locations = re.findall(r"[\u4e00-\u9fa5]{2,}", full_text)
    start_location = locations[-2] if len(locations) >= 2 else "未识别"
    end_location = locations[-1] if len(locations) >= 2 else "未识别"

    # 7. 返回结构化 JSON
    result = {
        "driver_name": driver_name,
        "date_time": date_time,
        "distance_km": distance_km,
        "duration": duration,
        "start_location": start_location,
        "end_location": end_location
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

