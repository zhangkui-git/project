from configparser import ConfigParser
import os


class ReadConfigFile(object):
    def read_config(self):
        con = ConfigParser()
        file_path = os.path.join(os.path.abspath('.'), 'config.ini')
        print(file_path)
        if not os.path.exists(file_path):
            print("文件不存在")
        else:
            con.read(file_path)
            url3 = con.get('login', 'url')
            url4 = con.get("logout", 'url')
            print(url3+'\n', url4)


if __name__ == '__main__':
    ReadConfigFile().read_config()





