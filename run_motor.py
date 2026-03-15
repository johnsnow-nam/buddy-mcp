#!/usr/bin/env python3
"""호환 보드 DC 모터 구동 예제 (2초 회전 후 정지)."""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import serial
from comm.buddy_channel import buddy_channel
from comm.buddy_protocol import BuddyProtocol
from comm.packet_t import packet_t

def main():
    port = os.environ.get("BUDDY_PORT")
    if not port:
        print("BUDDY_PORT 환경 변수를 설정하세요. 예: export BUDDY_PORT=/dev/cu.USB-Serial")
        sys.exit(1)
    print(f"연결 중: {port}")
    try:
        ser = serial.serial_for_url(port, baudrate=115200, timeout=1)
    except Exception as e:
        print(f"포트 열기 실패: {e}")
        sys.exit(1)
    with buddy_channel(ser, BuddyProtocol, packet_t) as p:
        p.decideToUseSensor(0, 0, 0)
        print("DC1, DC2 두 모터 구동 (dc1=90, dc2=90, 2초)")
        p.sendDC(90, 90)
        time.sleep(2)
        print("정지 (dc1=0, dc2=0)")
        p.sendDC(0, 0)
        time.sleep(0.5)
    print("완료.")

if __name__ == "__main__":
    main()
