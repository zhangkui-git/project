import socket
import datetime
import time
import threading


def put_udp(name):
    print(f"线程{name}启动")
    conn = socket.socket(type=socket.SOCK_DGRAM)
    while True:
        data = "4|^C91CB486575544B780C65A688D111111|^|^3|^1|^0|^null|^null|^2021-06-03 17:06:46|^2021-06-03 17:11:46|^|^usmadmin1/192.168.6.58|^192.168.4.164|^流出、流入|^1|^30640110|^1|^35179130|^2|^null|^test_zk9|^"
        conn.sendto(data.encode("utf-8"), ("192.168.15.8", 514))
        time.sleep(0.0001)
    conn.close()


def self_run():
    t1 = threading.Thread(target=put_udp, args=(1,))
    t2 = threading.Thread(target=put_udp, args=(2,))
    t3 = threading.Thread(target=put_udp, args=(3,))
    t4 = threading.Thread(target=put_udp, args=(4,))
    t5 = threading.Thread(target=put_udp, args=(5,))
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()


def app_run():
    return self_run()


if __name__ == '__main__':
    print("1111", datetime.datetime.now())
    app_run()









