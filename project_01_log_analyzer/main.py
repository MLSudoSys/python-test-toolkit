#main.py
import os
import  pandas as pd
from log_parser import HardwareLogParser

def main():
    #=========【在这里修改文件路径，后续微调重点位置】=======
    INPUT_LOG_PATH = "./input/hardware_log.txt"
    OUTPUT_EXCEL_PATH = "./output/log_analysis_report.xlsx"
    #====================================================

    #创建文件夹（不存在自动新建）
    os.makedirs("./input", exist_ok = True)
    os.makedirs("./output", exist_ok = True)

    print("===== 硬件日志自动解析工具 开始运行 ====")
    parser = HardwareLogParser()

    if not os.path.exists(INPUT_LOG_PATH):
        print(f"错误：日志文件不存在！路径：{INPUT_LOG_PATH}")
        print("请把硬件日志文件放到 input/hardware_log.txt")
        return

    #解析日志
    error_list = parser.scan_file(INPUT_LOG_PATH)
    stat = parser.get_statistics()

    print(f"扫描完成，一共发现异常条目：{stat['total_error_count']}")

    #导出Excel
    df = pd.DataFrame(error_list)
    df.to_excel(OUTPUT_EXCEL_PATH, index = False, engine = "openpyxl")
    print(f"报表已保存到：{OUTPUT_EXCEL_PATH}")
    print("==== 执行结束 ====")

if __name__ == "__main__":
    main()