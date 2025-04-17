from flask import Flask, request, jsonify
import re

app = Flask(__name__)

@app.route('/extract_trip_data', methods=['POST'])
def extract_trip_data():
    # 获取纯文本内容
    full_text = request.get_data(as_text=True)

    # 拆分文本为行，去掉空行
    lines = full_text.strip().splitlines()
    non_empty_lines = [line.strip() for line in lines if line.strip()]

    # 提取日期时间（格式：2025.03.08 13:08）
    date_time_match = re.search(r"(\d{4}\.\d{2}\.\d{2})\s+(\d{2}:\d{2})", full_text)
    date_time = f"{date_time_match.group(1)} {date_time_match.group(2)}" if date_time_match else "未识别"

    # 提取行驶里程（单位为 km，但排除 km/h）
    distance_match = re.search(r"(\d+(?:\.\d+)?)\s*km(?!/h)", full_text)
    distance_km = distance_match.group(1) if distance_match else "未识别"

    # 提取驾驶时长（格式：00:26:48）
    duration_match = re.search(r"(\d{2}:\d{2}:\d{2})", full_text)
    duration = duration_match.group(1) if duration_match else "未识别"

    # 提取出发地和目的地（最后两行）
    start_location = non_empty_lines[-2] if len(non_empty_lines) >= 2 else "未识别"
    end_location = non_empty_lines[-1] if len(non_empty_lines) >= 1 else "未识别"

    # 返回结构化 JSON 数据
    result = {
        "date_time": date_time,
        "distance_km": distance_km,
        "duration": duration,
        "start_location": start_location,
        "end_location": end_location
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

