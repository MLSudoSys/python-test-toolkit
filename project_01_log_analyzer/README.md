#project_01_log_analyzer
硬件日志解析小工具
用途：读取硬件文本日志->过滤错误行->统计一场数量->导出Excel报表
技术栈：python + pandas + openpyxl

目录说明：
main.py         #主程序入口
log_parser.py   #日志解析核心逻辑
config.py       #配置文件（错误关键词在这里自定义）
input/          #放原始硬件日志，比如log.txt
output/         #自动生成，输出解析后的Excel报告