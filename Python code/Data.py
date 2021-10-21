"""
Data.py
----------------------------------------
수집한 데이터의 변환 및 데이터데이스에 축적

"""

## import modules
import binascii
import struct
from bitstring import BitArray
import mariadb

## sequence
# data_convert
class Data_convert:
    def data_convert(get):                                                                  #통신으로 인해 섞인 데이터순서를 변환해주는 함수
        get_1 = BitArray(bytes=get, length=16).bytes
        get_2 = BitArray(bytes=get, length=16, offset=16).bytes

        cut_1 = list(get_1)
        cut_2 = list(get_2)

        cut_1.reverse()
        cut_2.reverse()

        c = bytearray(cut_1 + cut_2)

        unpack = struct.unpack('f', c)
        changed_form = list(unpack)
        result = round(changed_form[0], 3)

        return result

    def data_convert_error(get):                                                            #통신으로 인해 섞인 에러코드 데이터순서를 변환해주는 함수
        data_1 = BitArray(bytes=get, length=16).bytes
        data_2 = BitArray(bytes=get, length=16, offset=16).bytes
        data_3 = BitArray(bytes=get, length=32, offset=32).bytes

        cut_1 = list(data_1)
        cut_2 = list(data_2)

        cut_1.reverse()
        cut_2.reverse()
        
        array= bytearray(cut_1 + cut_2)

        total = array + data_3

        changed_form = bytes(total)
        result = "0x" + changed_form.decode()

        return result

# use_DB
class Use_db:
    # write_db
    def write_db(get):
        db_number = get[0]
        cur_number = get[1]
        plc_id = get[2]
        data_1 = get[3]
        data_2 = get[4]
        data_3 = get[5]
        data_4 = get[6]

        try:
            insert_query = "INSERT INTO " + plc_id + " (Belt_Pos, Belt_Vel, Circle_Pos, Circle_Vel) VALUES (?,?,?,?)" # 쿼리문 작성
            cur_number.execute( insert_query, (data_1, data_2, data_3, data_4))                                       # 쿼리문 실행
            db_number.commit()                                                                                        # Commit 메소드를 실행하여 db에 적용
        except mariadb.Error as e:
            # print("Error connecting to MariaDB Platform : {}".format(e))                                            
            pass

    def write_db_delta(get):
        db_number = get[0]
        cur_number = get[1]
        plc_id = get[2]
        data_1 = get[3]
        data_2 = get[4]
        data_3 = get[5]
        data_4 = get[6]
        data_5 = get[7]
        data_6 = get[8]

        try:
            insert_query = "INSERT INTO " + plc_id + " (L_Pos, L_Vel, C_Pos, C_Vel, R_Pos, R_Vel) VALUES (?,?,?,?,?,?)"
            cur_number.execute( insert_query, (data_1, data_2, data_3, data_4, data_5, data_6))
            db_number.commit()
        except mariadb.Error as e:
            # print("Error connecting to MariaDB Platform : {}".format(e))
            pass

    def write_db_piano(get):
        db_number = get[0]
        cur_number = get[1]
        plc_id = get[2]
        data_1 = get[3]
        data_2 = get[4]
        data_3 = get[5]
        data_4 = get[6]
        data_5 = get[7]
        data_6 = get[8]
        data_7 = get[9]
        data_8 = get[10]

        try:
            insert_query = "INSERT INTO " + plc_id + " (L_W_Pos, L_B_Pos, R_W_Pos, R_B_Pos, L_W_Vel, L_B_Vel, R_W_Vel, R_B_Vel) VALUES (?,?,?,?,?,?,?,?)"
            cur_number.execute( insert_query, (data_1, data_2, data_3, data_4, data_5, data_6, data_7, data_8))
            db_number.commit()
        except mariadb.Error as e:
            # print("Error connecting to MariaDB Platform : {}".format(e))
            pass

    def write_db_error(get):
        db_number = get[0]
        cur_number = get[1]
        plc_id = get[2]
        data_1 = get[3]
        data_2 = get[4]

        try:
            insert_query = "INSERT INTO " + plc_id + " (ECError, MCError) VALUES (?,?)"
            cur_number.execute( insert_query, (data_1, data_2))
            db_number.commit()
        except mariadb.Error as e:
            # print("Error connecting to MariaDB Platform : {}".format(e))
            pass

    # read_db
    def read_db(get):
        cur_number = get[0]
        plc_id = get[1]
        cur_number.execute("SELECT * FROM " + plc_id)
        db_row = cur_number.fetchall()
        last_row = db_row[-1]
        last_row_list = list(last_row)

        return last_row_list
