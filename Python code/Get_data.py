"""
Get_data.py
----------------------------------------
PLC-PC 통신 연결
FINS Commands로 데이터 송수신
Maria DB를 이용한 데이터베이스 축적
멀티스레드를 이용한 다중접속 구현
서버 접속 시 상태 변수 생성
----------------------------------------
"""

## import modules
import socket
import binascii
import struct
from bitstring import BitArray
import mariadb
import threading
import time
import sys
from Data import *
import datetime
from UI import Error_Window_PLC_A,Error_Window_PLC_B,Error_Window_PLC_C,Error_Window_PLC_D,TimeOut_Error_Window,ConnectionRefused_Error_Window
from kakao_msg import kakao_send

# 데이터 초기화 및 설정
# PLC-A
check_server_a = ['failed']
datetime_a = [0 for i in range(0, 10)]
Belt_Pos_a = [0 for i in range(0, 10)]
Belt_Vel_a = [0 for i in range(0, 10)]
Circle_Pos_a = [0 for i in range(0, 10)]
Circle_Vel_a = [0 for i in range(0, 10)]
EC_error_code_a = []
MC_error_code_a = []

# PLC-B
check_server_b = ['failed']
datetime_b = [0 for i in range(0, 10)]
Belt_Pos_b = [0 for i in range(0, 10)]
Belt_Vel_b = [0 for i in range(0, 10)]
Circle_Pos_b = [0 for i in range(0, 10)]
Circle_Vel_b = [0 for i in range(0, 10)]
EC_error_code_b = []
MC_error_code_b = []


# PLC-C
check_server_c = ['failed']
datetime_c = [0 for i in range(0, 10)]
L_Pos = [0 for i in range(0, 10)]
L_Vel = [0 for i in range(0, 10)]
C_Pos = [0 for i in range(0, 10)]
C_Vel = [0 for i in range(0, 10)]
R_Pos = [0 for i in range(0, 10)]
R_Vel = [0 for i in range(0, 10)]
EC_error_code_c = []
MC_error_code_c = []


# PLC-D 
check_server_d = ['failed']
datetime_d = [0 for i in range(0, 10)]
L_W_Pos = [0 for i in range(0, 10)]
L_B_Pos = [0 for i in range(0, 10)]
R_W_Pos = [0 for i in range(0, 10)]
R_B_Pos = [0 for i in range(0, 10)]
L_W_Vel = [0 for i in range(0, 10)]
L_B_Vel = [0 for i in range(0, 10)]
R_W_Vel = [0 for i in range(0, 10)]
R_B_Vel = [0 for i in range(0, 10)]
EC_error_code_d = []
MC_error_code_d = []

#PLC_State data
bool_data_a = [0]
bool_data_b = [0]
bool_data_c = [0]
bool_data_d = [0]

## sepuence
# Get_data_PLC_A
class PLC_A(threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True
        self.running = True
        self.thread_name = 'Thread_1'
        self.plc_name = 'PLC-A'
        self.format = '(' + self.thread_name + ' ' + self.plc_name + ')'
        self.now = datetime.datetime.now()
        self.time_format = '[' + self.now.strftime('%X') + ']'
        self.running = True

    def run(self):
        # socket 선언 및 IP,포트정의
        HOST_1 = '172.31.7.11'
        PORT_1 = 9600
        client_socket_1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        global check_server_a
        global bool_data_a

        # DB Connect을 위한 구성요소
        try:
            db_1 = mariadb.connect(
                user = 'root',
                password = '1234',
                host = '127.0.0.1',
                port = 3306,
                database = 'test'
            )
        except mariadb.Error as e:
            # print(f"Error connecting to MariaDB Platform : {e}")
            sys.exit()
        #DB의 Cursor 설정
        cur_1 = db_1.cursor()

        # 식별 정보
        db_number = db_1
        cur_number = cur_1
        plc_id = "plc_a"

        # run
        print("{0} {1} : starting".format(self.time_format, self.format))
        #Socket Connect
        try:
            client_socket_1.connect((HOST_1, PORT_1))
            # print("{0} {1} : 서버와 연결되었습니다.".format(self.time_format, self.format))
            del check_server_a[0]
            check_server_a.insert(0, 'connected')

            # First step(필수적) - FINS COMMAND
            send_data = binascii.a2b_hex('46494e530000000c000000000000000000000000')

            client_socket_1.sendall(send_data)

            recv_data = client_socket_1.recv(1024)

            data_0_1 = BitArray(bytes=recv_data, length=8, offset=152).bytes                #FINS COMMAND를 사용하기위해 recv받은 값 Byte변환 후 저장
            convert_0_1 = binascii.b2a_hex(data_0_1).decode()                               #Byte값 16진수화 후 디코딩 하여 저장

            data_0_2 = BitArray(bytes=recv_data, length=8, offset=184).bytes
            convert_0_2 = binascii.b2a_hex(data_0_2).decode()

            # print("{} {} : [Server node address(hex)] {}".format(self.time_format, self.format, convert_0_1))
            # print("{} {} : [Server node address(hex)] {}".format(self.time_format, self.format, convert_0_2))

            # read data - FINS COMMAND
            send_data = binascii.a2b_hex('46494e530000001a000000020000000080000201' + convert_0_2 + '0001' +convert_0_1 + '00000101820000000009')

            while self.running:
                client_socket_1.sendall(send_data)

                recv_data = client_socket_1.recv(1024)

                # data diffentation
                diff_code = BitArray(bytes=recv_data, length=8, offset=232).bytes           

                if diff_code == b'\x00':                                                    #값이 정상적으로 전송된경우
                    data_1 = BitArray(bytes=recv_data, length=32, offset=240).bytes
                    convert_1 = Data_convert.data_convert(data_1)
                    data_2 = BitArray(bytes=recv_data, length=32, offset=272).bytes
                    convert_2 = Data_convert.data_convert(data_2)
                    data_3 = BitArray(bytes=recv_data, length=32, offset=304).bytes
                    convert_3 = Data_convert.data_convert(data_3)
                    data_4 = BitArray(bytes=recv_data, length=32, offset=336).bytes
                    convert_4 = Data_convert.data_convert(data_4)
                    data_5 = BitArray(bytes=recv_data, length=16, offset=368).bytes
                    convert_5 = binascii.b2a_hex(data_5).decode()
                    start_data = int(convert_5, 16)
                    if start_data == 1:
                        del bool_data_a[0]
                        bool_data_a.insert(0, 1)
                    elif start_data == 0:
                        del bool_data_a[0]
                        bool_data_a.insert(0, 0)

                    if bool_data_a[0] == 1:                                                     #PLC_A의 상태가 ON일때 조건
                        # write db
                        data_list_1 = [db_number, cur_number, plc_id, convert_1, convert_2, convert_3, convert_4]
                        Use_db.write_db(data_list_1)

                        # read db
                        read_key = [cur_number, plc_id]
                        read_data_1 = Use_db.read_db(read_key)

                        del datetime_a[0]
                        datetime_a.insert(9, read_data_1[0])
                        del Belt_Pos_a[0]
                        Belt_Pos_a.insert(9, read_data_1[1])
                        del Belt_Vel_a[0]
                        Belt_Vel_a.insert(9, read_data_1[2])
                        del Circle_Pos_a[0]
                        Circle_Pos_a.insert(9, read_data_1[3])
                        del Circle_Vel_a[0]
                        Circle_Vel_a.insert(9, read_data_1[4])
                    time.sleep(1)                                                        

                elif diff_code == b'@':                                                         #값이 에러값이 전송될 경우 
                    data_6 = BitArray(bytes=recv_data, length=64, offset=240).bytes
                    convert_6 = Data_convert.data_convert_error(data_6)

                    data_7 = BitArray(bytes=recv_data, length=64, offset=304).bytes
                    # print(data_7)
                    convert_7 = Data_convert.data_convert_error(data_7)

                    # write on db
                    data_list_2 = [db_number, cur_number, plc_id, convert_6, convert_7]
                    Use_db.write_db_error(data_list_2)

                    # read from db
                    read_key = [cur_number, plc_id]
                    read_data_2 = Use_db.read_db(read_key)

                    del check_server_a[0]
                    check_server_a.insert(0, 'failed')

                    if read_data_2[5] or read_data_2[6] != None:
                        EC_error_code_a.insert(0,read_data_2[5])
                        MC_error_code_a.insert(0,read_data_2[6])
                        Error_Window_PLC_A().mainloop()
                        kakao_send.refreshToken()
                        kakao_send.kakao_text()
                    break

        except TimeoutError:                                                            #TimeoutError발생시 예외처리
            TimeOut_Error_Window().mainloop()
            del check_server_a[0]
            check_server_a.insert(0, 'failed')
        except ConnectionRefusedError:                                                  #ConnectionRefusedError발생시 예외처리
            ConnectionRefused_Error_Window().mainloop()
            del check_server_a[0]
            check_server_a.insert(0, 'failed')

        db_1.close()
        client_socket_1.close()
        del check_server_a[0]
        check_server_a.insert(0, 'failed')

    def error_code(self):                                                                #에러발생 이벤트 처리에 있어서 필요한 정보반환
        return EC_error_code_a,MC_error_code_a
    
    def resume(self):
        self.running = True

    def pause(self):
        self.running = False



class PLC_B(threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True
        self.running = True
        self.thread_name = 'Thread_2'
        self.plc_name = 'PLC-B'
        self.format = '(' + self.thread_name + ' ' + self.plc_name + ')'
        self.now = datetime.datetime.now()
        self.time_format = '[' + self.now.strftime('%X') + ']'
        self.running = True

    def run(self):
        # socket 초기값
        HOST_2 = '172.31.3.22'
        PORT_2 = 9600
        client_socket_2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        global check_server_b
        global bool_data_b

        # DB 초기값
        try:
            db_2 = mariadb.connect(
                user = 'root',
                password = 'jds',
                host = '127.0.0.1',
                port = 3306,
                database = 'plc_db'
            )
        except mariadb.Error as e:
            # print(f"Error connecting to MariaDB Platform : {e}")
            sys.exit()

        cur_2 = db_2.cursor()

        # 식별 정보
        db_number = db_2
        cur_number = cur_2
        plc_id = "plc_b"

        # run
        # print("{0} {1} : starting".format(self.time_format, self.format))

        try:
            client_socket_2.connect((HOST_2, PORT_2))
            # print("{0} {1} : 서버와 연결되었습니다.".format(self.time_format, self.format))
            del check_server_b[0]
            check_server_b.insert(0, 'connected')

            # request node - First step(필수적)
            send_data = binascii.a2b_hex('46494e530000000c000000000000000000000000')

            client_socket_2.sendall(send_data)

            recv_data = client_socket_2.recv(1024)

            data_0_1 = BitArray(bytes=recv_data, length=8, offset=152).bytes
            convert_0_1 = binascii.b2a_hex(data_0_1).decode()

            data_0_2 = BitArray(bytes=recv_data, length=8, offset=184).bytes
            convert_0_2 = binascii.b2a_hex(data_0_2).decode()

            # print("{} {} : [Server node address(hex)] {}".format(self.time_format, self.format, convert_0_1))
            # print("{} {} : [Server node address(hex)] {}".format(self.time_format, self.format, convert_0_2))

            # read data - 할당된 node를 대입하여 진행
            send_data = binascii.a2b_hex('46494e530000001a000000020000000080000201' + convert_0_2 + '0001' +convert_0_1 + '00000101820000000009')

            while self.running:
                client_socket_2.sendall(send_data)

                recv_data = client_socket_2.recv(1024)

                # data diffentation
                diff_code = BitArray(bytes=recv_data, length=8, offset=232).bytes

                if diff_code == b'\x00':
                    data_1 = BitArray(bytes=recv_data, length=32, offset=240).bytes
                    convert_1 = Data_convert.data_convert(data_1)

                    data_2 = BitArray(bytes=recv_data, length=32, offset=272).bytes
                    convert_2 = Data_convert.data_convert(data_2)

                    data_3 = BitArray(bytes=recv_data, length=32, offset=304).bytes
                    convert_3 = Data_convert.data_convert(data_3)

                    data_4 = BitArray(bytes=recv_data, length=32, offset=336).bytes
                    convert_4 = Data_convert.data_convert(data_4)

                    data_5 = BitArray(bytes=recv_data, length=16, offset=368).bytes
                    convert_5 = binascii.b2a_hex(data_5).decode()
                    start_data = int(convert_5, 16)
                    if start_data == 1:
                        del bool_data_b[0]
                        bool_data_b.insert(0, 1)
                    elif start_data == 0:
                        del bool_data_b[0]
                        bool_data_b.insert(0, 0)


                    if bool_data_b[0] == 1:
                        # write on db
                        data_list_1 = [db_number, cur_number, plc_id, convert_1, convert_2, convert_3, convert_4]
                        Use_db.write_db(data_list_1)

                        # read from db
                        read_key = [cur_number, plc_id]
                        read_data_1 = Use_db.read_db(read_key)

                        global datetime_b, Belt_Pos_b, Belt_Vel_b, Circle_Pos_b, Circle_Vel_b

                        del datetime_b[0]
                        datetime_b.insert(9, read_data_1[0])
                        del Belt_Pos_b[0]
                        Belt_Pos_b.insert(9, read_data_1[1])
                        del Belt_Vel_b[0]
                        Belt_Vel_b.insert(9, read_data_1[2])
                        del Circle_Pos_b[0]
                        Circle_Pos_b.insert(9, read_data_1[3])
                        del Circle_Vel_b[0]
                        Circle_Vel_b.insert(9, read_data_1[4])

                        # print("[{0}] {1} : Belt_Pos {2} | Belt_Vel {3} | Circle_Pos {4} | Circle_Vel {5}".format(datetime_b[9], self.format, Belt_Pos_b[9], Belt_Vel_b[9], Circle_Pos_b[9], Circle_Vel_b[9]))

                    time.sleep(1)

                elif diff_code == b'@':
                    data_6 = BitArray(bytes=recv_data, length=64, offset=240).bytes
                    convert_6 = Data_convert.data_convert_error(data_6)

                    data_7 = BitArray(bytes=recv_data, length=64, offset=304).bytes
                    convert_7 = Data_convert.data_convert_error(data_7)

                    # write on db
                    data_list_2 = [db_number, cur_number, plc_id, convert_6, convert_7]
                    Use_db.write_db_error(data_list_2)

                    # read from db
                    read_key = [cur_number, plc_id]
                    read_data_2 = Use_db.read_db(read_key)

                    # print("[{0}] {1} : [EC_Error] code {2} | [MC_Error] code {3}".format(datetime_b[9], self.format, read_data_2[5], read_data_2[6]))
                    
                    del check_server_b[0]
                    check_server_b.insert(0, 'failed')
                    if read_data_2[5] or read_data_2[6] != None:
                        EC_error_code_b.insert(0,read_data_2[5])
                        MC_error_code_b.insert(0,read_data_2[6])
                        Error_Window_PLC_B().mainloop()
                        kakao_send.refreshToken()
                        kakao_send.kakao_text()
                    break

        except TimeoutError:
            # print("{0} {1} : (Error) 서버와 연결할 수 없습니다. IP주소와 포트번호를 다시 확인해주세요.".format(self.time_format, self.format))
            TimeOut_Error_Window().mainloop()
            del check_server_b[0]
            check_server_b.insert(0, 'failed')
        except ConnectionRefusedError:
            # print("{0} {1} : (Error) 서버와의 연결이 거부되었습니다. 포트번호를 다시 확인해주세요.".format(self.time_format, self.format))
            ConnectionRefused_Error_Window().mainloop()
            del check_server_b[0]
            check_server_b.insert(0, 'failed')

        db_2.close()
        client_socket_2.close()

        del check_server_b[0]
        check_server_b.insert(0, 'failed')

        # print("{0} {1} : finishing".format(self.time_format, self.format))

    def error_code(self):
        return EC_error_code_b,MC_error_code_b

    def resume(self):
        self.running = True

    def pause(self):
        self.running = False




class PLC_C(threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True
        self.running = True
        self.thread_name = 'Thread_3'
        self.plc_name = 'Delta_Robot'
        self.format = '(' + self.thread_name + ' ' + self.plc_name + ')'
        self.now = datetime.datetime.now()
        self.time_format = '[' + self.now.strftime('%X') + ']'
        self.running = True

    def run(self):
        # socket 초기값
        HOST_2 = '172.31.7.26'
        PORT_2 = 9600
        client_socket_3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        global check_server_c
        global bool_data_c

        # DB 초기값
        try:
            db_3 = mariadb.connect(
                user = 'root',
                password = '1234',
                host = '127.0.0.1',
                port = 3306,
                database = 'test'
            )
        except mariadb.Error as e:
            # print(f"Error connecting to MariaDB Platform : {e}")
            sys.exit()

        cur_3 = db_3.cursor()

        # 식별 정보
        db_number = db_3
        cur_number = cur_3
        plc_id = "plc_c"

        # run
        # print("{0} {1} : starting".format(self.time_format, self.format))

        try:
            client_socket_3.connect((HOST_2, PORT_2))
            # print("{0} {1} : 서버와 연결되었습니다.".format(self.time_format, self.format))
            del check_server_c[0]
            check_server_c.insert(0, 'connected')

            # request node - First step(필수적)
            send_data = binascii.a2b_hex('46494e530000000c000000000000000000000000')

            client_socket_3.sendall(send_data)

            recv_data = client_socket_3.recv(1024)

            data_0_1 = BitArray(bytes=recv_data, length=8, offset=152).bytes
            convert_0_1 = binascii.b2a_hex(data_0_1).decode()

            data_0_2 = BitArray(bytes=recv_data, length=8, offset=184).bytes
            convert_0_2 = binascii.b2a_hex(data_0_2).decode()

            # print("{} {} : [Server node address(hex)] {}".format(self.time_format, self.format, convert_0_1))
            # print("{} {} : [Server node address(hex)] {}".format(self.time_format, self.format, convert_0_2))

            # read data
            send_data = binascii.a2b_hex('46494e530000001a000000020000000080000201' + convert_0_2 + '0001' +convert_0_1 + '00000101820000000013')

            while self.running:
                client_socket_3.sendall(send_data)

                recv_data = client_socket_3.recv(1024)

                # data diffentation
                diff_code = BitArray(bytes=recv_data, length=8, offset=232).bytes

                if diff_code == b'\x00':
                    data_1 = BitArray(bytes=recv_data, length=32, offset=240).bytes
                    convert_1 = Data_convert.data_convert(data_1)

                    data_2 = BitArray(bytes=recv_data, length=32, offset=272).bytes
                    convert_2 = Data_convert.data_convert(data_2)

                    data_3 = BitArray(bytes=recv_data, length=32, offset=304).bytes
                    convert_3 = Data_convert.data_convert(data_3)

                    data_4 = BitArray(bytes=recv_data, length=32, offset=336).bytes
                    convert_4 = Data_convert.data_convert(data_4)

                    data_8 = BitArray(bytes=recv_data, length=32, offset=368).bytes
                    convert_8 = Data_convert.data_convert(data_8)

                    data_9 = BitArray(bytes=recv_data, length=32, offset=400).bytes
                    convert_9 = Data_convert.data_convert(data_9)

                    data_5 = BitArray(bytes=recv_data, length=16, offset=432).bytes
                    convert_5 = binascii.b2a_hex(data_5).decode()
                    start_data = int(convert_5, 16)
                    if start_data == 1:
                        del bool_data_c[0]
                        bool_data_c.insert(0, 1)
                    elif start_data == 0:
                        del bool_data_c[0]
                        bool_data_c.insert(0, 0)

                    if bool_data_c[0] == 1:
                        # write on db
                        data_list_1 = [db_number, cur_number, plc_id, convert_1, convert_2, convert_3, convert_4, convert_8, convert_9]
                        Use_db.write_db_delta(data_list_1)

                        # read from db
                        read_key = [cur_number, plc_id]
                        read_data_1 = Use_db.read_db(read_key)

                        global datetime_c, L_Pos, L_Vel, C_Pos, C_Vel, R_Pos, R_Vel

                        del datetime_c[0]
                        datetime_c.insert(9, read_data_1[0])
                        del L_Pos[0]
                        L_Pos.insert(9, read_data_1[1])
                        del L_Vel[0]
                        L_Vel.insert(9, read_data_1[2])
                        del C_Pos[0]
                        C_Pos.insert(9, read_data_1[3])
                        del C_Vel[0]
                        C_Vel.insert(9, read_data_1[4])
                        del R_Pos[0]
                        R_Pos.insert(9, read_data_1[5])
                        del R_Vel[0]
                        R_Vel.insert(9, read_data_1[6])

                        # print("[{0}] {1} : L_Pos {2} | L_Vel {3} | C_Pos {4} | C_Vel {5} | R_Pos {6} | R_Vel {7}".format(datetime_c[9], self.format, L_Pos[9], L_Vel[9], C_Pos[9], C_Vel[9], R_Pos[9], R_Vel[9]))

                    time.sleep(1)

                elif diff_code == b'@':
                    data_6 = BitArray(bytes=recv_data, length=64, offset=240).bytes
                    convert_6 = Data_convert.data_convert_error(data_6)

                    data_7 = BitArray(bytes=recv_data, length=64, offset=304).bytes
                    convert_7 = Data_convert.data_convert_error(data_7)

                    # write on db
                    data_list_2 = [db_number, cur_number, plc_id, convert_6, convert_7]
                    Use_db.write_db_error(data_list_2)

                    # read from db
                    read_key = [cur_number, plc_id]
                    read_data_2 = Use_db.read_db(read_key)

                    # print("[{0}] {1} : [EC_Error] code {2} | [MC_Error] code {3}".format(datetime_c[9], self.format, read_data_2[7], read_data_2[8]))
                    
                    del check_server_c[0]
                    check_server_c.insert(0, 'failed')
                    if read_data_2[7] or read_data_2[8] != None:
                        EC_error_code_c.insert(0,read_data_2[7])
                        MC_error_code_c.insert(0,read_data_2[8])
                        Error_Window_PLC_C().mainloop()
                        kakao_send.refreshToken()
                        kakao_send.kakao_text()
                    break

        except TimeoutError:
            # print("{0} {1} : (Error) 서버와 연결할 수 없습니다. IP주소와 포트번호를 다시 확인해주세요.".format(self.time_format, self.format))
            TimeOut_Error_Window().mainloop()
            del check_server_c[0]
            check_server_c.insert(0, 'failed')
        except ConnectionRefusedError:
            # print("{0} {1} : (Error) 서버와의 연결이 거부되었습니다. 포트번호를 다시 확인해주세요.".format(self.time_format, self.format))
            ConnectionRefused_Error_Window().mainloop()
            del check_server_c[0]
            check_server_c.insert(0, 'failed')

        db_3.close()
        client_socket_3.close()

        del check_server_c[0]
        check_server_c.insert(0, 'failed')

        # print("{0} {1} : finishing".format(self.time_format, self.format))

    def error_code(self):
        return EC_error_code_c,MC_error_code_c

    def resume(self):
        self.running = True

    def pause(self):
        self.running = False




class PLC_D(threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True
        self.running = True
        self.thread_name = 'Thread_4'
        self.plc_name = 'Piano-Robot'
        self.format = '(' + self.thread_name + ' ' + self.plc_name + ')'
        self.now = datetime.datetime.now()
        self.time_format = '[' + self.now.strftime('%X') + ']'
        self.running = True

    def run(self):
        # socket 초기값
        HOST_2 = '172.31.3.20'
        PORT_2 = 9600
        client_socket_4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        global check_server_d
        global bool_data_d

        # DB 초기값
        try:
            db_4 = mariadb.connect(
                user = 'root',
                password = 'jds',
                host = '127.0.0.1',
                port = 3306,
                database = 'plc_db'
            )
        except mariadb.Error as e:
            # print(f"Error connecting to MariaDB Platform : {e}")
            sys.exit()

        cur_4 = db_4.cursor()

        # 식별 정보
        db_number = db_4
        cur_number = cur_4
        plc_id = "plc_d"

        # run
        # print("{0} {1} : starting".format(self.time_format, self.format))

        try:
            client_socket_4.connect((HOST_2, PORT_2))
            # print("{0} {1} : 서버와 연결되었습니다.".format(self.time_format, self.format))
            del check_server_d[0]
            check_server_d.insert(0, 'connected')

            # request node - First step(필수적)
            send_data = binascii.a2b_hex('46494e530000000c000000000000000000000000')

            client_socket_4.sendall(send_data)

            recv_data = client_socket_4.recv(1024)

            data_0_1 = BitArray(bytes=recv_data, length=8, offset=152).bytes
            convert_0_1 = binascii.b2a_hex(data_0_1).decode()

            data_0_2 = BitArray(bytes=recv_data, length=8, offset=184).bytes
            convert_0_2 = binascii.b2a_hex(data_0_2).decode()

            # print("{} {} : [Server node address(hex)] {}".format(self.time_format, self.format, convert_0_1))
            # print("{} {} : [Server node address(hex)] {}".format(self.time_format, self.format, convert_0_2))

            # read data - 할당된 node를 대입하여 진행
            send_data = binascii.a2b_hex('46494e530000001a000000020000000080000201' + convert_0_2 + '0001' +convert_0_1 + '00000101820000000017')

            while self.running:
                client_socket_4.sendall(send_data)

                recv_data = client_socket_4.recv(1024)

                # data diffentation
                diff_code = BitArray(bytes=recv_data, length=8, offset=232).bytes

                if diff_code == b'\x00':
                    data_1 = BitArray(bytes=recv_data, length=32, offset=240).bytes
                    convert_1 = Data_convert.data_convert(data_1)

                    data_2 = BitArray(bytes=recv_data, length=32, offset=272).bytes
                    convert_2 = Data_convert.data_convert(data_2)

                    data_3 = BitArray(bytes=recv_data, length=32, offset=304).bytes
                    convert_3 = Data_convert.data_convert(data_3)

                    data_4 = BitArray(bytes=recv_data, length=32, offset=336).bytes
                    convert_4 = Data_convert.data_convert(data_4)

                    data_5 = BitArray(bytes=recv_data, length=32, offset=368).bytes
                    convert_5 = Data_convert.data_convert(data_5)

                    data_6 = BitArray(bytes=recv_data, length=32, offset=400).bytes
                    convert_6 = Data_convert.data_convert(data_6)

                    data_7 = BitArray(bytes=recv_data, length=32, offset=432).bytes
                    convert_7 = Data_convert.data_convert(data_7)

                    data_8 = BitArray(bytes=recv_data, length=32, offset=464).bytes
                    convert_8 = Data_convert.data_convert(data_8)

                    data_9 = BitArray(bytes=recv_data, length=16, offset=496).bytes
                    convert_9 = binascii.b2a_hex(data_9).decode()
                    start_data = int(convert_9, 16)
                    if start_data == 1:
                        del bool_data_d[0]
                        bool_data_d.insert(0, 1)
                    elif start_data == 0:
                        del bool_data_d[0]
                        bool_data_d.insert(0, 0)


                    if bool_data_d[0] == 1:
                        # write on db
                        data_list_1 = [db_number, cur_number, plc_id, convert_1, convert_2, convert_3, convert_4, convert_5, convert_6, convert_7, convert_8]
                        Use_db.write_db_piano(data_list_1)

                        # read from db
                        read_key = [cur_number, plc_id]
                        read_data_1 = Use_db.read_db(read_key)

                        global datetime_d, L_W_Pos, L_B_Pos, R_W_Pos, R_B_Pos, L_W_Vel, L_B_Vel, R_W_Vel, R_B_Vel

                        del datetime_d[0]
                        datetime_d.insert(9, read_data_1[0])
                        del L_W_Pos[0]
                        L_W_Pos.insert(9, read_data_1[1])
                        del L_B_Pos[0]
                        L_B_Pos.insert(9, read_data_1[2])
                        del R_W_Pos[0]
                        R_W_Pos.insert(9, read_data_1[3])
                        del R_B_Pos[0]
                        R_B_Pos.insert(9, read_data_1[4])
                        del L_W_Vel[0]
                        L_W_Vel.insert(9, read_data_1[5])
                        del L_B_Vel[0]
                        L_B_Vel.insert(9, read_data_1[6])
                        del R_W_Vel[0]
                        R_W_Vel.insert(9, read_data_1[7])
                        del R_B_Vel[0]
                        R_B_Vel.insert(9, read_data_1[8])

                        # print("[{0}] {1} : L_W_Pos {2} | L_B_Pos {3} | R_W_Pos {4} | R_B_Pos {5} | L_W_Vel {6} | L_B_Vel {7} | R_W_Vel {8} | R_B_Vel {9}".format(datetime_d[9], self.format, L_W_Pos[9], L_B_Pos[9], R_W_Pos[9], R_B_Pos[9], L_W_Vel[9], L_B_Vel[9], R_W_Vel[9], R_B_Vel[9]))

                    time.sleep(1)

                elif diff_code == b'@':
                    data_10 = BitArray(bytes=recv_data, length=64, offset=240).bytes
                    convert_10 = Data_convert.data_convert_error(data_10)

                    data_11 = BitArray(bytes=recv_data, length=64, offset=304).bytes
                    convert_11 = Data_convert.data_convert_error(data_11)

                    # write on db
                    data_list_2 = [db_number, cur_number, plc_id, convert_10, convert_11]
                    Use_db.write_db_error(data_list_2)

                    # read from db
                    read_key = [cur_number, plc_id]
                    read_data_2 = Use_db.read_db(read_key)

                    # print("[{0}] {1} : [EC_Error] code {2} | [MC_Error] code {3}".format(datetime_b[9], self.format, read_data_2[9], read_data_2[10]))
                    
                    del check_server_d[0]
                    check_server_d.insert(0, 'failed')
                    if read_data_2[9] or read_data_2[10] != None:
                        EC_error_code_d.insert(0,read_data_2[9])
                        MC_error_code_d.insert(0,read_data_2[10])
                        Error_Window_PLC_D().mainloop()
                        kakao_send.refreshToken()
                        kakao_send.kakao_text()
                    break

        except TimeoutError:
            # print("{0} {1} : (Error) 서버와 연결할 수 없습니다. IP주소와 포트번호를 다시 확인해주세요.".format(self.time_format, self.format))
            TimeOut_Error_Window().mainloop()
            del check_server_d[0]
            check_server_d.insert(0, 'failed')
        except ConnectionRefusedError:
            # print("{0} {1} : (Error) 서버와의 연결이 거부되었습니다. 포트번호를 다시 확인해주세요.".format(self.time_format, self.format))
            ConnectionRefused_Error_Window().mainloop()
            del check_server_d[0]
            check_server_d.insert(0, 'failed')

        db_4.close()
        client_socket_4.close()

        del check_server_d[0]
        check_server_d.insert(0, 'failed')

        # print("{0} {1} : finishing".format(self.time_format, self.format))

    def error_code(self):
        return EC_error_code_d,MC_error_code_d

    def resume(self):
        self.running = True

    def pause(self):
        self.running = False