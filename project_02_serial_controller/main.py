from serial_collector import SerialCollector
import serial_collector

def main():
    print("=== 简易产线串口采集上位机 ===")
    # 打印所有串口
    serial_collector.list_all_ports()
    selected_port = input("\n输入串口名（例如 COM3 / /dev/ttyUSB0）：")
    baud = int(input("输入波特率（默认 115200，直接回车使用默认）：") or 115200)

    collector = SerialCollector(port=selected_port, baudrate=baud)
    if not collector.open_serial():
        exit(1)

    print("\n操作说明：输入指令发送给硬件，输入 exit 退出程序")
    try:
        while True:
            user_input = input()
            if user_input.lower() == "exit":
                break
            collector.send_cmd(user_input)
    except KeyboardInterrupt:
        print("\n收到退出信号")
    finally:
        collector.close()

if __name__ == "__main__":
    main()
