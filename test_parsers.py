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
        self.assertEqual(result.get("running_time"), 20)
        self.assertEqual(result.get("running_speed"), 7.0)
        self.assertEqual(result.get("max_heart_rate"), 165)
        # Verify at least 4 exercises are parsed
        self.assertGreaterEqual(len(result["exercises"]), 4)
        # Verify that notes contain the residual text
        self.assertTrue("超猛" in result["notes"])


if __name__ == "__main__":
    unittest.main()
