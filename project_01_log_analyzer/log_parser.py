#log_parser.py
import re
from config import ERROR_KEYWORDS, CASE_INSENSITIVE

class HardwareLogParser:
    def __init__(self):
        self.error_records = []

    def scan_file(self, file_path: str):
        """读取日志文件，逐行扫描，提取异常行"""
        self.error_records.clear()

        with open(file_path, "r", encoding = "utf-8", errors = "ignore") as f:
            lines = f.readlines()

        for line_no, raw_line in enumerate(lines, start = 1):
            line = raw_line.strip()
            if not line:
                continue

            #判断该行是否包含错误关键词
            match = False
            check_line = line.lower() if CASE_INSENSITIVE else line
            for kw in ERROR_KEYWORDS:
                if kw in check_line:
                    match = True
                    break

            if match:
                self.error_records.append({
                    "line_number": line_no,
                    "log_content":raw_line.strip()
                })
            return self.error_records

    def get_statistics(self):
        """返回统计信息"""
        return {
            "total_error_count": len(self.error_records)
        }