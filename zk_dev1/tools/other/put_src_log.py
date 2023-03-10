import socket
from datetime import datetime
import time
import threading
import schedule


def put_udp(name):
    print(f"线程{name}启动")
    conn = socket.socket(type=socket.SOCK_DGRAM)
    while True:
        # data = "4|^C91CB486575544B780C65A688D111111|^|^3|^1|^0|^null|^null|^2021-06-03 17:06:46|^2021-06-03 17:11:46|^|^usmadmin1/192.168.6.58|^192.168.4.164|^流出、流入|^1|^30640110|^1|^35179130|^2|^null|^test_zk9|^"
        data = "10|2|1|0|2021-06-03 14:54:28"
        conn.sendto(data.encode("utf-8"), ("192.168.4.250", 514))
        time.sleep(0.001)
    conn.close()


def self_run():
    t1 = threading.Thread(target=put_udp, args=(1,))
    t2 = threading.Thread(target=put_udp, args=(2,))
    t3 = threading.Thread(target=put_udp, args=(3,))
    t4 = threading.Thread(target=put_udp, args=(4,))
    t5 = threading.Thread(target=put_udp, args=(5,))
    t6 = threading.Thread(target=put_udp, args=(6,))
    t7 = threading.Thread(target=put_udp, args=(7,))
    t8 = threading.Thread(target=put_udp, args=(8,))
    t9 = threading.Thread(target=put_udp, args=(9,))
    t10 = threading.Thread(target=put_udp, args=(10,))
    t11 = threading.Thread(target=put_udp, args=(11,))
    t12 = threading.Thread(target=put_udp, args=(12,))
    t13 = threading.Thread(target=put_udp, args=(13,))
    t14 = threading.Thread(target=put_udp, args=(14,))
    t15 = threading.Thread(target=put_udp, args=(15,))
    t16 = threading.Thread(target=put_udp, args=(16,))
    t17 = threading.Thread(target=put_udp, args=(17,))
    t18 = threading.Thread(target=put_udp, args=(18,))
    t19 = threading.Thread(target=put_udp, args=(19,))
    t20 = threading.Thread(target=put_udp, args=(20,))
    t21 = threading.Thread(target=put_udp, args=(21,))
    t22 = threading.Thread(target=put_udp, args=(22,))
    t23 = threading.Thread(target=put_udp, args=(23,))
    t24 = threading.Thread(target=put_udp, args=(24,))
    t25 = threading.Thread(target=put_udp, args=(25,))
    t26 = threading.Thread(target=put_udp, args=(26,))
    t27 = threading.Thread(target=put_udp, args=(27,))
    t28 = threading.Thread(target=put_udp, args=(28,))
    t29 = threading.Thread(target=put_udp, args=(29,))
    t30 = threading.Thread(target=put_udp, args=(30,))
    t1.start()
    time.sleep(1)
    t2.start()
    time.sleep(1)
    t3.start()
    time.sleep(1)
    t4.start()
    time.sleep(1)
    t5.start()
    time.sleep(1)
    t6.start()
    time.sleep(1)
    t7.start()
    time.sleep(1)
    t8.start()
    time.sleep(1)
    t9.start()
    time.sleep(1)
    t10.start()
    time.sleep(1)
    t11.start()
    time.sleep(1)
    t12.start()
    time.sleep(1)
    t13.start()
    time.sleep(1)
    t14.start()
    time.sleep(1)
    t15.start()
    time.sleep(1)
    t16.start()
    time.sleep(1)
    t17.start()
    time.sleep(1)
    t18.start()
    time.sleep(1)
    t19.start()
    time.sleep(1)
    t20.start()
    # t21.start()
    # t22.start()
    # t23.start()
    # t24.start()
    # t25.start()
    # t26.start()
    # t27.start()
    # t28.start()
    # t29.start()
    # t30.start()


if __name__ == '__main__':
    self_run()









