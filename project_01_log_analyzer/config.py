#config.py
"""
配置：硬件日志异常关键词，自定义添加/删除
可以根据你的硬件日志，增加错误字符串
"""

#匹配异常/错误的关键词，全部小写，匹配时忽略大小写
ERROR_KEYWORDS = [
    "error",
    "fail",
    "failed",
    "warning",
    "exception",
    "timeout",
    "crash",
    "abort",
    "violation"
]

#是否大小写不敏感（推荐开启）
CASE_INSENSITIVE = True