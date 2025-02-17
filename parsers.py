import re
from datetime import datetime


def parse_workout_record(record: str) -> dict:
    # 初始化預設結果
    result = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "running_time": None,
        "running_speed": None,
        "max_heart_rate": None,
        "exercises": [],
        "notes": "",
    }
    lines = record.splitlines()
    notes = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("---"):
            continue
        # 處理慢跑行：例如 "慢跑 20mins (7.0 10 mins, 10mins 最高 165)"
        if "慢跑" in line:
            m = re.search(r"慢跑\s+(\d+)\s*mins.*?(\d+\.?\d*).*?最高\s*(\d+)", line)
            if m:
                result["running_time"] = int(m.group(1))
                result["running_speed"] = float(m.group(2))
                result["max_heart_rate"] = int(m.group(3))
            else:
                notes.append(line)
        # 處理運動項目：例如 "胸部推舉 110lb x 8 x 5"
        elif "x" in line:
            # 嘗試匹配含重量格式
            m = re.search(r"(.+?)\s+(\d+)(?:lb)?\s*x\s*(\d+)\s*x\s*(\d+)", line)
            if m:
                exercise = {
                    "name": m.group(1).strip(),
                    "weight": int(m.group(2)),
                    "reps": int(m.group(3)),
                    "sets": int(m.group(4)),
                }
                result["exercises"].append(exercise)
            else:
                # 匹配無重量格式，例如 "短程仰臥起坐 15 x 4"
                m2 = re.search(r"(.+?)\s+(\d+)\s*x\s*(\d+)", line)
                if m2:
                    exercise = {
                        "name": m2.group(1).strip(),
                        "weight": None,
                        "reps": int(m2.group(2)),
                        "sets": int(m2.group(3)),
                    }
                    result["exercises"].append(exercise)
                else:
                    notes.append(line)
        else:
            # 如果非運動行，當作備註累計
            notes.append(line)
    result["notes"] = " ".join(notes)
    return result
