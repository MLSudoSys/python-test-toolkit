import curses
import queue
from serial_collector import SerialCollector

class CursesTui:
    def __init__(self, port: str, baud: int = 115200):
        self.port = port
        self.baud = baud

    def run(self, stdscr):
        #初始化颜色，ERROR标红
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        RED_PAIR = 1
        curses.curs_set(1)
        stdscr.nodelay(True)    #主窗口设置非阻塞
        stdscr.timeout(10)      #等待按键超时时间（ms），超时直接继续循环

        log_q = queue.Queue(maxsize = 200)
        collector = SerialCollector(port = self.port, baudrate = self.baud, log_queue = log_q)
        if not collector.open_serial():
            return

        #窗口划分：上半日志区， 底部1行输入区
        sh, sw = stdscr.getmaxyx()
        log_win_h = sh - 2
        log_win = curses.newwin(log_win_h, sw, 0, 0)
        input_win = curses.newwin(1, sw, sh - 1, 0)
        log_win.scrollok(True) #开启自动滚动

        log_history = []
        max_lines = log_win_h - 1

        input_buffer = "" # 手动保存输入的字符串

        try:
            while True:
                # 读取队列新日志
                read_count = 0
                MAX_READ_PER_FRAME = 1
                while not log_q.empty() and read_count < MAX_READ_PER_FRAME:
                    line = log_q.get()
                    log_history.append(line)
                    if len(log_history) > max_lines:
                        log_history.pop(0)
                    read_count += 1

                # 重绘日志窗口
                log_win.clear()
                for idx, text in enumerate(log_history):
                    try:
                        if "[ERROR]" in text:
                            log_win.addstr(idx, 0, text[:sw - 1], curses.color_pair(RED_PAIR))
                        else:
                            log_win.addstr(idx, 0, text[:sw - 1])
                    except curses.error:
                        # 窗口边界溢出直接跳过，防止程序崩溃
                        pass
                log_win.refresh()

                # 底部输入区 非阻塞处理
                input_win.clear()
                prompt = "Send Cmd >> "
                input_win.addstr(0, 0, prompt + input_buffer)
                input_win.refresh()

                try:
                    key = stdscr.getch()
                except curses.error:
                    key = -1

                if key != -1:
                    if key == curses.KEY_ENTER or key == 10 or key == 13:
                        # 按下回车：发送命令
                        if input_buffer.strip() != "":
                            send_result = collector.send_cmd(input_buffer)
                            log_history.append(send_result)
                            if len(log_history) > max_lines:
                                log_history.pop(0)
                        # 输入清空
                        if input_buffer.strip() == "exit":
                            break
                        input_buffer = ""
                    elif key == curses.KEY_BACKSPACE or key == 127:
                        # 退出键
                        input_buffer = input_buffer[:-1]
                    else:
                        # 普通字符
                        char = chr(key)
                        input_buffer += char
        finally:
            collector.close()
