import serial
import time
import random

# ======== 配置，改成创建的虚拟串口 COMX ========
COM_PORT = "COM6"
BAUDRATE = 115200

def simulate_hardware():
    ser = serial.Serial(COM_PORT, BAUDRATE, timeout = 0.2)
    print(f"模拟硬件启动，端口 {COM_PORT} 已打开， 等待上位机链接")
    print("模拟硬件：定时输出硬件日志，同时监听上位机下发命令\n")

    counter = 0
    try:
        while True:
            # 1 模拟硬件主动打印日志（SSD/NAND硬件调试日志）
            temp = round(35 + random.uniform(-3, 3), 2)
            if counter % 5 == 0:
                # 模拟错误日志
                log_line = f"[ERROR] NAND page read fail, LBA = {random.randint(0, 1000)}, retry = 1\n"
            else:
                log_line = f"[INFO] Device status OK, temp = {temp}℃，page = {counter}, plane = 0\n"
            ser.write(log_line.encode("utf-8"))
            print("[硬件输出]" + log_line.strip())

            # 2 监听上位机下发的控制命令
            if ser.in_waiting > 0:
                cmd = ser.readline().decode("utf-8", errors = "ignore").strip()
                print(f"<<< 收到上位机命令：{cmd}")
                # 模拟硬件响应指令
                if cmd == "status":
                    ser.write(b"[RESP] Device: ONLINE, ECC_COR = 0, ECC_UNCOR = 0\n")
                elif cmd == "reset":
                    ser.write(b"[RESP] Reset trigger, success, rebooting...\n")
                elif cmd == "get_err":
                    ser.write(b"[RESP] Total error count: 3\n")
                else:
                    ser.write(b"[RESP] Unknown cmd\n")
            counter += 1
            time.sleep(0.8)
    except KeyboardInterrupt:
        print("\n模拟硬件停止")
    finally:
        ser.close()

if __name__ == "__main__":
    simulate_hardware()