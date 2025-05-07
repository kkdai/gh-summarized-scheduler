import unittest
from parsers import parse_workout_record


class TestParseWorkoutRecord(unittest.TestCase):
    def test_parse_workout_record(self):
        sample = """
把拔紀錄 （四)
慢跑 20mins (7.0 10 mins, 10mins 最高 165)
胸部推舉 110lb x 8 x 5
背部下拉 90lb x 8 x 5
腹部彎曲 110lb x 15 x 4
短程仰臥起坐 15 x 4 (回升
左右仰臥起坐 10 x 4
肌肉力量還沒恢復，今天看到有人在跑步機跑 12.5 的速度。（五分），超猛。
"""
        result = parse_workout_record(sample)
        # Verify running parameters are parsed
        print(result)
        self.assertEqual(result.get("running_time"), 20)
        self.assertEqual(result.get("running_speed"), 7.0)
        self.assertEqual(result.get("max_heart_rate"), 165)
        # Verify at least 4 exercises are parsed
        self.assertGreaterEqual(len(result["exercises"]), 4)
        # Verify that notes contain the residual text
        self.assertTrue("超猛" in result["notes"])

    def test_parse_workout_record_set2(self):
        sample = """
#把拔紀錄 (二）
跑步 20 mins (7.0 10mins, 10mins max 165 )
背部下拉 90lb x 8 x 6
胸部推舉 110lb x 8 x 6
短程仰臥起坐 15 x 4
左右仰臥起坐 10 x 4
恢復連續兩天運動，一開始跑步有點小抽筋。後來速度降下來就好一點。
"""
        result = parse_workout_record(sample)
        print("\\nTest Case 2 Result:")
        print(result)
        self.assertEqual(result.get("running_time"), 20, "Running time mismatch")
        self.assertEqual(result.get("running_speed"), 7.0, "Running speed mismatch")
        self.assertEqual(result.get("max_heart_rate"), 165, "Max heart rate mismatch")
        self.assertGreaterEqual(len(result.get("exercises", [])), 4, "Number of exercises mismatch")
        self.assertTrue("恢復連續兩天運動" in result.get("notes", ""), "Notes content mismatch")

    def test_parse_workout_record_set3(self):
        sample = """
#把拔紀錄 (一)
跑步 10 mins (7.5 10 mins max 172 )
胸部推舉 110lb x 8 x 6
下拉訓練 90lb x 8 x 6
短程仰臥起坐 15 x 4
左右仰臥起坐 10 x 4
今天先重訓再跑步，然後就跑不動惹。
"""
        result = parse_workout_record(sample)
        print("\\\\nTest Case 3 Result:")
        print(result)
        self.assertEqual(result.get("running_time"), 10, "Running time mismatch for set 3")
        self.assertEqual(result.get("running_speed"), 7.5, "Running speed mismatch for set 3")
        self.assertEqual(result.get("max_heart_rate"), 172, "Max heart rate mismatch for set 3")
        self.assertGreaterEqual(len(result.get("exercises", [])), 4, "Number of exercises mismatch for set 3")
        self.assertTrue("今天先重訓再跑步" in result.get("notes", ""), "Notes content mismatch for set 3")

    def test_skip_non_workout_text(self):
        sample = """
github.com/micr
- 微軟提供一個 AI 代理程式入門課程，共 10 堂課。
- 課程包含文字教材、影片教學和程式碼範例。
- 使用 Azure AI Foundry 和 GitHub Models 等工具。
- 支援多種語言，包含繁體中文。
- 課程內容涵蓋 AI 代理程式的基本概念和設計模式。
#AIAgents #MachineLearning #Microsoft
"""
        result = parse_workout_record(sample)
        print("\\nTest Case Skip Non-Workout Result:")
        print(result)
        self.assertEqual(result, {}, "Non-workout text should return an empty dict")


if __name__ == "__main__":
    unittest.main()
