import serial
import serial.tools.list_ports
import threading
import time
from datetime import datetime

class SerialCollector:
    def __init__(self, port: str, baudrate: int = 115200, log_file = "serial_log.txt"):
        self.port = port
        self.baudrate = baudrate
        self.log_file = log_file
        self.ser = None
        self.running = False    #控制读取线程启停

    def open_serial(self) -> bool:
        """打开串口"""
        try:
            self.ser = serial.Serial(
                port = self.port,
                baudrate = self.baudrate,
                timeout = 0.1,
                bytesize = serial.EIGHTBITS,
                parity = serial.PARITY_NONE,
                stopbits = serial.STOPBITS_ONE
            )
            if self.ser.is_open:
                print(f"串口 {self.port} 打开成功，波特率：{self.baudrate}")
                self.running = True
                # 启动串口读取子线程
                read_thread = threading.Thread(target = self._read_loop, daemon = True)
                read_thread.start()
                return True
        except Exception as e:
            print(f"串口打开失败：{e}")
        return False

    def _read_loop(self):
        """子线程：循环读取串口数据"""
        with open(self.log_file, "a", encoding = "utf-8") as f:
            while self.running and self.ser and self.ser.is_open:
                try:
                    raw_data = self.ser.readline()
                    if not raw_data:
                        continue
                    #解码，或略无法解析的字节（硬件乱码容错）
                    line = raw_data.decode("utf-8", errors = "ignore").strip()
                    if not line:
                        continue
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    log_line = f"[{timestamp}] {line}"
                    print(log_line)
                    f.write(log_line + "\n")
                    f.flush()
                except Exception as e:
                    print(f"读取异常：{e}")
                    time.sleep(0.2)

    def send_cmd(self, cmd: str):
        """向下位硬件发送串口指令，自动追加换行"""
        if self.ser and self.ser.is_open:
            send_bytes = (cmd + "\r\n").encode("utf-8")
            self.ser.write(send_bytes)
            print(f">>> 发送：{cmd}")
        else:
            print("串口未打开，无法发送")

    def close(self):
        """关闭串口，停止线程"""
        self.running = False
        if self.ser:
            self.ser.close()
            print("串口已关闭")

def list_all_ports():
    """列出本机所有可用串口"""
    ports = serial.tools.list_ports.comports()
    print("\n=== 可用串口列表 ===")
    for p in ports:
        print(f"{p.device} | {p.description}")
    return ports