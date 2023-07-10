import os

ABS_PATH = os.path.abspath(__file__)  # 获取当前文件的绝对路径
DIR_NAME = os.path.dirname(ABS_PATH)  # 获取文件所在的目录

# print(ABS_PATH)
# print(DIR_NAME)
# print(DIR_NAME)

import threading
import websocket


def on_message(ws, message):
    print("Received message: ", message)


def on_error(ws, error):
    print("Error: ", error)


def on_close(ws):
    print("Connection closed.")


def on_open(ws):
    def run(*args):
        ws.send("Hello, world!")
        ws.close()
        print("Thread terminating...")

    threading.Thread(target=run).start()


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://echo.websocket.org/",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
