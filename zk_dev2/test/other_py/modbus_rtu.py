import serial # 导入模块
import array
import random
import time
try:
  portx="COM3"  #输入串口名称
  bps=115200
  #超时设置,None：永远等待操作，0为立即返回请求结果，其他值为等待超时时间(单位为秒）
  timex=0.4
  ser=serial.Serial(portx,bps,timeout=timex)
  print("串口详情参数：", ser)
  fun1=bytearray(b'\x0a\x01\x00\x00\x01\x01\x01\x01')
  fun2=bytearray(b'\x01\x02\x00\x13\x00\x6e\x01\x01')
  fun3=bytearray(b'\x01\x03\x01\x02\x01\x01\x01\x01')
  fun4=bytearray(b'\x01\x04\x01\x02\x01\x01\x01\x01')
  fun5=bytearray(b'\x04\x05\xFF\x00\x00\x00\x01\x01')
  fun6=bytearray(b'\x01\x06\xFF\x00\x00\x00\x01\x01')
  fun15=bytearray(b'\x01\x0f\x00\x13\x00\x0A\x02\xCD\x01\x01\x01')
  fun16=bytearray(b'\x01\x10\x00\x00\x00\x02\x04\xcc\xcd\x3f\xcc\x01\x01')
  fun20=bytearray(b'\x01\x14\x0E\x06\x00\x04\x00\x01\x00\x02\x06\x00\x03\x00\x09\x00\x02\x01\x01')
  fun21=bytearray(b'\x01\x15\x0d\x06\x00\x04\x00\x07\x00\x03\x06\xAF\x04\xBE\x10\x0d\x01\x01')
  fun22=bytearray(b'\x01\x16\x01\x01\x01\x01\x01\x01\x01\x01')
  fun23=bytearray(b'\x01\x17\x00\x03\x00\x06\x00\x0E\x00\x04\x06\x00\xFF\x00\xFF\x00\xFF\x01\x01')
  fun24=bytearray(b'\x01\x18\x04\xDE\x01\x01')
  fun43=bytearray(b'\x01\x2B\x01\x02\x0E\x01\x01\x00\x00\x03\x02\x05\xff\x01\x01')

except Exception as e:
  print('-----异常----',e) 
 #十六进制的读取
 #print(ser.read().hex())#读一个字节

 #print("---------------")
 #ser.close()#关闭串口
def Rdom():
      fun1[2]=random.randint(0,255)
      fun1[3]=random.randint(0, 255)

      fun2[2]=random.randint(0, 255)
      fun2[2]=random.randint(0, 255)

      fun3[2]=random.randint(0, 255)
      fun3[2]=random.randint(0, 255)

      fun4[2]=random.randint(0, 255)
      fun4[2]=random.randint(0, 255)

      fun5[2]=random.randint(0, 255)
      fun5[2]=random.randint(0, 255)

      fun6[2]=random.randint(0, 255)
      fun6[2]=random.randint(0, 255)
  
      fun15[2]=random.randint(0, 255)
      fun15[2]=random.randint(0, 255)

      fun16[2]=random.randint(0, 255)
      fun16[2]=random.randint(0, 255)

      fun22[2]=random.randint(0, 255)
      fun22[2]=random.randint(0, 255)

      fun23[6]=random.randint(0, 255)
      fun23[7]=random.randint(0, 255)
      fun23[8]=random.randint(0, 118)

      fun24[2]=random.randint(0, 255)
      fun24[2]=random.randint(0, 255)

if __name__ == '__main__':

  while True:  
      Rdom()
      fun=int(input('功能码：'))
      if fun==1:
        result=ser.write(fun1)#写数据    
        print("写总字节数:",result)       
      elif fun==2:
        result=ser.write(fun2)#写数据    
        print("写总字节数:",result)
      elif fun==3:
        result=ser.write(fun3)#写数据    
        print("写总字节数:",result)
      elif fun==4:
        result=ser.write(fun4)#写数据    
        print("写总字节数:",result)
      elif fun==5:
        result=ser.write(fun5)#写数据    
        print("写总字节数:",result)
      elif fun==6:
        result=ser.write(fun6)#写数据    
        print("写总字节数:",result)
      elif fun==15:
        result=ser.write(fun15)#写数据    
        print("写总字节数:",result)
      elif fun==16:
        result=ser.write(fun16)#写数据    
        print("写总字节数:",result)
      elif fun==20:
        result=ser.write(fun20)#写数据    
        print("写总字节数:",result)
      elif fun==21:
        result=ser.write(fun21)#写数据    
        print("写总字节数:",result)
      elif fun==22:
        result=ser.write(fun22)#写数据    
        print("写总字节数:",result)
      elif fun==23:
        result=ser.write(fun23)#写数据    
        print("写总字节数:",result)
      elif fun==24:
        result=ser.write(fun24)#写数据    
        print("写总字节数:",result)
      elif fun==43:
        result=ser.write(fun43)#写数据    
        print("写总字节数:",result) 
      elif fun==0:
         test=[fun1,fun2,fun3,fun4,fun5,fun6,fun15,fun16,fun20,fun21,fun22,fun23,fun24,fun43]
         while True:
              Rdom()
              for i in test:
                  result=ser.write(i)#写数据    
                  print("写总字节数:",result)
                  time.sleep(1)
      else :
        print('请输入 0、1、2、3、4、5、6、15、16、20、21、22、23、24、43；\nNote: 0 is continuous sending')   
      
    

'''
port - 串口设备名或 None。
baudrate - 波特率，可以是50, 75, 110, 134, 150, 200, 300, 600, 1200, 1800, 2400, 4800, 9600, 19200, 38400, 57600, 115200, 230400, 460800, 500000, 576000, 921600, 1000000, 1152000, 1500000, 2000000, 2500000, 3000000, 3500000, 4000000。
bytesize - 数据位，可取值为：FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS。
parity - 校验位，可取值为：PARITY_NONE, PARITY_EVEN, PARITY_ODD, PARITY_MARK, PARITY_SPACE。
stopbits - 停止位，可取值为：STOPBITS_ONE, STOPBITS_ONE_POINT_FIVE, STOPBITS_TOW。
xonxoff - 软件流控，可取值为 True, False。
rtscts - 硬件（RTS/CTS）流控，可取值为 True, False。
dsr/dtr - 硬件（DSR/DTR）流控，可取值为 True, False。
timeout - 读超时时间，可取值为 None, 0 或者其他具体数值（支持小数）。当设置为 None 时，表示阻塞式读取，一直读到期望的所有数据才返回；当设置为 0 时，表示非阻塞式读取，无论读取到多少数据都立即返回；当设置为其他数值时，表示设置具体的超时时间（以秒为单位），如果在该时间内没有读取到所有数据，则直接返回。
write_timeout: 写超时时间，可取值为 None, 0 或者其他具体数值（支持小数）。参数值起到的效果参考 timeout 参数。
'''  