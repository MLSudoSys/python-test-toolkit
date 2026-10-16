from serial_collector import SerialCollector
import serial_collector
from curses_tui import CursesTui
import curses

def main():
    print("=== 简易产线串口采集上位机 ===")
    # 打印所有串口
    serial_collector.list_all_ports()
    selected_port = input("\n输入串口名（例如 COM3 / /dev/ttyUSB0）：")
    baud = int(input("输入波特率（默认 115200，直接回车使用默认）：") or 115200)

    tui_app = CursesTui(selected_port, baud)
    curses.wrapper(tui_app.run)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"程序运行异常：{e}")
        import traceback
        traceback.print_exc()
    finally:
        input("\n按回车键退出...")
