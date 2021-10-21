"""
Thread ver_1.0.7

각 페이지별 스레딩 요소 부여

"""

## import modules
from tkinter import *
import os
from tkinter.font import Font
import threading
import datetime
import time
import sys
from Sub_UI_1 import *
from Sub_UI_2 import *
from Sub_UI_3 import *
from Get_data import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

## thread
#년,월,일 ,일 구현
class ShowDate(threading.Thread, Tk):
    def __init__(self):
        super().__init__()
        self.daemon = True

    def run(self):
        font_day = Font(size=17, weight='bold')

        date_live = datetime.datetime.now().strftime('%Y.%m.%d')

        label = Label(font=font_day, fg='#FFFFFF', bg='#465260')
        label.place(x=1327, y=36, height=25)

        label.config(text=date_live)
        label.after(1000, self.run)
#요일 구현
class ShowDay(threading.Thread, Tk):
    def __init__(self):
        super().__init__()
        self.daemon = True

    def run(self):
        font_day = Font(size=17, weight='bold')

        day_live = datetime.datetime.today().strftime('%A')

        label = Label(font=font_day, fg='#FFFFFF', bg='#465260')
        label.place(x=1455, y=34, height=27)

        label.config(text=day_live)
        label.after(1000, self.run)
# 시,분,초 구현
class ShowTime(threading.Thread, Tk):
    def __init__(self):
        super().__init__()
        self.daemon = True

    def run(self):
        font_time = Font(size=45, weight='bold')

        time_live = time.strftime('%H:%M:%S')

        label = Label(font=font_time, fg='#FFFFFF', bg='#465260')
        label.place(x=1320, y=65, width=235, height=50)

        label.config(text=time_live)
        label.after(1000, self.run)

#PLC_A의 상태 체크
class CheckPLC_1(threading.Thread, Frame):
    def __init__(self, frame):
        super().__init__()
        self.daemon = True
        self.frame = frame
        self.running = True

    def run(self):
        self.state_run_image_1 = PhotoImage(file=os.path.join(current_file, 'state_run_1.png'))
        self.state_run_image_2 = PhotoImage(file=os.path.join(current_file, 'state_run_2.png'))
        self.state_run = Label(self.frame, image=self.state_run_image_2, bg='#FFFFFF')
        self.state_run.place(x=325, y=325, width=100, height=50)

        self.state_idle_image_1 = PhotoImage(file=os.path.join(current_file, 'state_idle_1.png'))
        self.state_idle_image_2 = PhotoImage(file=os.path.join(current_file, 'state_idle_2.png'))
        self.state_idle = Label(self.frame, image=self.state_idle_image_2, bg='#FFFFFF')
        self.state_idle.place(x=425, y=325, width=100, height=50)

        self.state_stop_image_1 = PhotoImage(file=os.path.join(current_file, 'state_stop_1.png'))
        self.state_stop_image_2 = PhotoImage(file=os.path.join(current_file, 'state_stop_2.png'))
        self.state_stop = Label(self.frame, image=self.state_stop_image_1, bg='#FFFFFF')
        self.state_stop.place(x=525, y=325, width=100, height=50)

        # 상태 변경
        while self.running:
            if check_server_a[0] == 'failed':
                self.state_run.configure(image=self.state_run_image_2)
                self.state_idle.configure(image=self.state_idle_image_2)
                self.state_stop.configure(image=self.state_stop_image_1)

            elif bool_data_a[0] == 0 and check_server_a[0] == 'connected':
                self.state_run.configure(image=self.state_run_image_2)
                self.state_idle.configure(image=self.state_idle_image_1)
                self.state_stop.configure(image=self.state_stop_image_2)

            elif bool_data_a[0] == 1 and check_server_a[0] == 'connected':
                self.state_run.configure(image=self.state_run_image_1)
                self.state_idle.configure(image=self.state_idle_image_2)
                self.state_stop.configure(image=self.state_stop_image_2)

            time.sleep(1)

    def resume(self):
        self.running = True

    def pause(self):
        self.state_run.configure(image=self.state_run_image_2)
        self.state_idle.configure(image=self.state_idle_image_2)
        self.state_stop.configure(image=self.state_stop_image_1)
        self.running = False


#PLC_B의 상태 체크
class CheckPLC_2(threading.Thread, Frame):
    def __init__(self, frame):
        super().__init__()
        self.daemon = True
        self.frame = frame
        self.running = True

    def run(self):
        self.state_run_image_1 = PhotoImage(file=os.path.join(current_file, 'state_run_1.png'))
        self.state_run_image_2 = PhotoImage(file=os.path.join(current_file, 'state_run_2.png'))
        self.state_run = Label(self.frame, image=self.state_run_image_2, bg='#FFFFFF')
        self.state_run.place(x=980, y=325, width=100, height=50)

        self.state_idle_image_1 = PhotoImage(file=os.path.join(current_file, 'state_idle_1.png'))
        self.state_idle_image_2 = PhotoImage(file=os.path.join(current_file, 'state_idle_2.png'))
        self.state_idle = Label(self.frame, image=self.state_idle_image_2, bg='#FFFFFF')
        self.state_idle.place(x=1080, y=325, width=100, height=50)

        self.state_stop_image_1 = PhotoImage(file=os.path.join(current_file, 'state_stop_1.png'))
        self.state_stop_image_2 = PhotoImage(file=os.path.join(current_file, 'state_stop_2.png'))
        self.state_stop = Label(self.frame, image=self.state_stop_image_1, bg='#FFFFFF')
        self.state_stop.place(x=1180, y=325, width=100, height=50)

        # 상태 변경
        while self.running:
            if check_server_b[0] == 'failed':
                self.state_run.configure(image=self.state_run_image_2)
                self.state_idle.configure(image=self.state_idle_image_2)
                self.state_stop.configure(image=self.state_stop_image_1)

            elif bool_data_b[0] == 0 and check_server_b[0] == 'connected':
                self.state_run.configure(image=self.state_run_image_2)
                self.state_idle.configure(image=self.state_idle_image_1)
                self.state_stop.configure(image=self.state_stop_image_2)

            elif bool_data_b[0] == 1 and check_server_b[0] == 'connected':
                self.state_run.configure(image=self.state_run_image_1)
                self.state_idle.configure(image=self.state_idle_image_2)
                self.state_stop.configure(image=self.state_stop_image_2)

            time.sleep(1)

    def resume(self):
        self.running = True

    def pause(self):
        self.state_run.configure(image=self.state_run_image_2)
        self.state_idle.configure(image=self.state_idle_image_2)
        self.state_stop.configure(image=self.state_stop_image_1)    
        self.running = False



#PLC_C의 상태 체크
class CheckPLC_3(threading.Thread, Frame):
    def __init__(self, frame):
        super().__init__()
        self.daemon = True
        self.frame = frame
        self.running = True

    def run(self):
        self.state_run_image_1 = PhotoImage(file=os.path.join(current_file, 'state_run_1.png'))
        self.state_run_image_2 = PhotoImage(file=os.path.join(current_file, 'state_run_2.png'))
        self.state_run = Label(self.frame, image=self.state_run_image_2, bg='#FFFFFF')
        self.state_run.place(x=325, y=325, width=100, height=50)

        self.state_idle_image_1 = PhotoImage(file=os.path.join(current_file, 'state_idle_1.png'))
        self.state_idle_image_2 = PhotoImage(file=os.path.join(current_file, 'state_idle_2.png'))
        self.state_idle = Label(self.frame, image=self.state_idle_image_2, bg='#FFFFFF')
        self.state_idle.place(x=425, y=325, width=100, height=50)

        self.state_stop_image_1 = PhotoImage(file=os.path.join(current_file, 'state_stop_1.png'))
        self.state_stop_image_2 = PhotoImage(file=os.path.join(current_file, 'state_stop_2.png'))
        self.state_stop = Label(self.frame, image=self.state_stop_image_1, bg='#FFFFFF')
        self.state_stop.place(x=525, y=325, width=100, height=50)

        # 상태 변경
        while self.running:
            if check_server_c[0] == 'failed':
                self.state_run.configure(image=self.state_run_image_2)
                self.state_idle.configure(image=self.state_idle_image_2)
                self.state_stop.configure(image=self.state_stop_image_1)

            elif bool_data_c[0] == 0 and check_server_c[0] == 'connected':
                self.state_run.configure(image=self.state_run_image_2)
                self.state_idle.configure(image=self.state_idle_image_1)
                self.state_stop.configure(image=self.state_stop_image_2)

            elif bool_data_c[0] == 1 and check_server_c[0] == 'connected':
                self.state_run.configure(image=self.state_run_image_1)
                self.state_idle.configure(image=self.state_idle_image_2)
                self.state_stop.configure(image=self.state_stop_image_2)

            time.sleep(1)

    def resume(self):
        self.running = True

    def pause(self):
        self.state_run.configure(image=self.state_run_image_2)
        self.state_idle.configure(image=self.state_idle_image_2)
        self.state_stop.configure(image=self.state_stop_image_1)
        self.running = False


#PLC_D의 상태 체크
class CheckPLC_4(threading.Thread, Frame):
    def __init__(self, frame):
        super().__init__()
        self.daemon = True
        self.frame = frame
        self.running = True

    def run(self):
        self.state_run_image_1 = PhotoImage(file=os.path.join(current_file, 'state_run_1.png'))
        self.state_run_image_2 = PhotoImage(file=os.path.join(current_file, 'state_run_2.png'))
        self.state_run = Label(self.frame, image=self.state_run_image_2, bg='#FFFFFF')
        self.state_run.place(x=980, y=325, width=100, height=50)

        self.state_idle_image_1 = PhotoImage(file=os.path.join(current_file, 'state_idle_1.png'))
        self.state_idle_image_2 = PhotoImage(file=os.path.join(current_file, 'state_idle_2.png'))
        self.state_idle = Label(self.frame, image=self.state_idle_image_2, bg='#FFFFFF')
        self.state_idle.place(x=1080, y=325, width=100, height=50)

        self.state_stop_image_1 = PhotoImage(file=os.path.join(current_file, 'state_stop_1.png'))
        self.state_stop_image_2 = PhotoImage(file=os.path.join(current_file, 'state_stop_2.png'))
        self.state_stop = Label(self.frame, image=self.state_stop_image_1, bg='#FFFFFF')
        self.state_stop.place(x=1180, y=325, width=100, height=50)

        # 상태 변경
        while self.running:
            if check_server_d[0] == 'failed':
                self.state_run.configure(image=self.state_run_image_2)
                self.state_idle.configure(image=self.state_idle_image_2)
                self.state_stop.configure(image=self.state_stop_image_1)

            elif bool_data_d[0] == 0 and check_server_d[0] == 'connected':
                self.state_run.configure(image=self.state_run_image_2)
                self.state_idle.configure(image=self.state_idle_image_1)
                self.state_stop.configure(image=self.state_stop_image_2)

            elif bool_data_d[0] == 1 and check_server_d[0] == 'connected':
                self.state_run.configure(image=self.state_run_image_1)
                self.state_idle.configure(image=self.state_idle_image_2)
                self.state_stop.configure(image=self.state_stop_image_2)

            time.sleep(1)

    def resume(self):
        self.running = True

    def pause(self):
        self.state_run.configure(image=self.state_run_image_2)
        self.state_idle.configure(image=self.state_idle_image_2)
        self.state_stop.configure(image=self.state_stop_image_1)    
        self.running = False



#PLC에서 전송된 값들을 Update해주는 클래스
class Update_1(threading.Thread, Frame):
    def __init__(self, frame):
        super().__init__()
        self.daemon = True
        self.frame = frame
        self.running = True

    def run(self):
        # print
        data_1_1_entry = Entry(self.frame, justify='right')
        data_1_1_entry.place(x=175, y=433, width=110, height=22)

        data_1_2_entry = Entry(self.frame, justify='right')
        data_1_2_entry.place(x=175, y=463, width=110, height=22)

        data_1_3_entry = Entry(self.frame, justify='right')
        data_1_3_entry.place(x=480, y=433, width=110, height=22)

        data_1_4_entry = Entry(self.frame, justify='right')
        data_1_4_entry.place(x=480, y=463, width=110, height=22)

        
        fig_1 = plt.figure()                                    # 그래프를 그려주는 코드
        x_1 = [0 for i in range(0, 10)]
        y_1 = [0 for i in range(0, 10)]

        fig_2 = plt.figure()
        x_2 = [0 for i in range(0, 10)]
        y_2 = [0 for i in range(0, 10)]

        canvas_1 = FigureCanvasTkAgg(fig_1, master=self.frame)
        canvas_1.get_tk_widget().place(x=35, y=495, width=300, height=220)

        canvas_2 = FigureCanvasTkAgg(fig_2, master=self.frame)
        canvas_2.get_tk_widget().place(x=340, y=495, width=300, height=220)

        while self.running:                                     #그래프에 적용시킬 데이터 Update 및 delete
            data_1_1_entry.delete(0, END)
            data_1_1_entry.insert(0, Belt_Pos_a[9])
            data_1_1_entry.update()

            data_1_2_entry.delete(0, END)
            data_1_2_entry.insert(0, Belt_Vel_a[9])
            data_1_2_entry.update()

            data_1_3_entry.delete(0, END)
            data_1_3_entry.insert(0, Circle_Pos_a[9])
            data_1_3_entry.update()

            data_1_4_entry.delete(0, END)
            data_1_4_entry.insert(0, Circle_Vel_a[9])
            data_1_4_entry.update()

            fig_1.clear()                                       #그래프 클리어(현재 업데이트를 캔버스로 하기때문에 무조건 클리어를 해주어야함)
            ax_1 = fig_1.add_subplot(1, 1, 1)                   #그래프 구현
            ax_1.set(ylim=[0, 400], title='Position_Belt')
            ax_1.plot(x_1, y_1, color='blue')

            fig_2.clear()
            ax_2 = fig_2.add_subplot(1, 1, 1)
            ax_2.set(ylim=[0, 400], title='Position_Circle')
            ax_2.plot(x_2, y_2, color='red')

            canvas_1.draw()
            canvas_1.get_tk_widget().update()

            canvas_2.draw()
            canvas_2.get_tk_widget().update()

            new_x_1 = x_1[9] + 1
            del x_1[0]
            x_1.insert(9, new_x_1)
            del y_1[0]
            y_1.insert(9, Belt_Pos_a[9])

            new_x_2 = x_2[9] + 1
            del x_2[0]
            x_2.insert(9, new_x_2)
            del y_2[0]
            y_2.insert(9, Circle_Pos_a[9])

            time.sleep(1)

    def resume(self):
        self.running = True

    def pause(self):
        self.running = False


class Update_2(threading.Thread, Frame):
    def __init__(self, frame):
        super().__init__()
        self.daemon = True
        self.frame = frame
        self.running = True

    def run(self):
        # print
        data_1_1_entry = Entry(self.frame, justify='right')
        data_1_1_entry.place(x=830, y=433, width=110, height=22)

        data_1_2_entry = Entry(self.frame, justify='right')
        data_1_2_entry.place(x=830, y=463, width=110, height=22)

        data_1_3_entry = Entry(self.frame, justify='right')
        data_1_3_entry.place(x=1135, y=433, width=110, height=22)

        data_1_4_entry = Entry(self.frame, justify='right')
        data_1_4_entry.place(x=1135, y=463, width=110, height=22)

        # draw
        fig_1 = plt.figure()
        x_1 = [0 for i in range(0, 10)]
        y_1 = [0 for i in range(0, 10)]

        fig_2 = plt.figure()
        x_2 = [0 for i in range(0, 10)]
        y_2 = [0 for i in range(0, 10)]

        canvas_1 = FigureCanvasTkAgg(fig_1, master=self.frame)
        canvas_1.get_tk_widget().place(x=690, y=495, width=300, height=220)

        canvas_2 = FigureCanvasTkAgg(fig_2, master=self.frame)
        canvas_2.get_tk_widget().place(x=995, y=495, width=300, height=220)

        while self.running:
            data_1_1_entry.delete(0, END)
            data_1_1_entry.insert(0, Belt_Pos_b[9])
            data_1_1_entry.update()

            data_1_2_entry.delete(0, END)
            data_1_2_entry.insert(0, Belt_Vel_b[9])
            data_1_2_entry.update()

            data_1_3_entry.delete(0, END)
            data_1_3_entry.insert(0, Circle_Pos_b[9])
            data_1_3_entry.update()

            data_1_4_entry.delete(0, END)
            data_1_4_entry.insert(0, Circle_Vel_b[9])
            data_1_4_entry.update()

            fig_1.clear()
            ax_1 = fig_1.add_subplot(1, 1, 1)
            ax_1.set(ylim=[0, 400], title='Position_Belt')
            ax_1.plot(x_1, y_1, color='blue')

            fig_2.clear()
            ax_2 = fig_2.add_subplot(1, 1, 1)
            ax_2.set(ylim=[0, 400], title='Position_Circle')
            ax_2.plot(x_2, y_2, color='red')

            canvas_1.draw()
            canvas_1.get_tk_widget().update()

            canvas_2.draw()
            canvas_2.get_tk_widget().update()

            new_x_1 = x_1[9] + 1
            del x_1[0]
            x_1.insert(9, new_x_1)
            del y_1[0]
            y_1.insert(9, Belt_Pos_b[9])

            new_x_2 = x_2[9] + 1
            del x_2[0]
            x_2.insert(9, new_x_2)
            del y_2[0]
            y_2.insert(9, Circle_Pos_b[9])

            time.sleep(1)

    def resume(self):
        self.running = True

    def pause(self):
        self.running = False




class Update_3(threading.Thread, Frame):
    def __init__(self, frame):
        super().__init__()
        self.daemon = True
        self.frame = frame
        self.running = True

    def run(self):
        # print
        data_1_1_entry = Entry(self.frame, justify='right')
        data_1_1_entry.place(x=110, y=433, width=80, height=22)

        data_1_2_entry = Entry(self.frame, justify='right')
        data_1_2_entry.place(x=110, y=463, width=80, height=22)

        data_1_3_entry = Entry(self.frame, justify='right')
        data_1_3_entry.place(x=305, y=433, width=80, height=22)

        data_1_4_entry = Entry(self.frame, justify='right')
        data_1_4_entry.place(x=305, y=463, width=80, height=22)

        data_1_5_entry = Entry(self.frame, justify='right')
        data_1_5_entry.place(x=510, y=433, width=80, height=22)

        data_1_6_entry = Entry(self.frame, justify='right')
        data_1_6_entry.place(x=510, y=463, width=80, height=22)

        # draw
        fig_1 = plt.figure()
        x_1 = [0 for i in range(0, 10)]
        y_1_1 = [0 for i in range(0, 10)]
        y_1_2 = [0 for i in range(0, 10)]
        y_1_3 = [0 for i in range(0, 10)]

        fig_2 = plt.figure()
        x_2 = [0 for i in range(0, 10)]
        y_2_1 = [0 for i in range(0, 10)]
        y_2_2 = [0 for i in range(0, 10)]
        y_2_3 = [0 for i in range(0, 10)]

        canvas_1 = FigureCanvasTkAgg(fig_1, master=self.frame)
        canvas_1.get_tk_widget().place(x=35, y=495, width=300, height=220)

        canvas_2 = FigureCanvasTkAgg(fig_2, master=self.frame)
        canvas_2.get_tk_widget().place(x=340, y=495, width=300, height=220)

        while self.running:
            data_1_1_entry.delete(0, END)
            data_1_1_entry.insert(0, L_Pos[9])
            data_1_1_entry.update()

            data_1_2_entry.delete(0, END)
            data_1_2_entry.insert(0, L_Vel[9])
            data_1_2_entry.update()

            data_1_3_entry.delete(0, END)
            data_1_3_entry.insert(0, C_Pos[9])
            data_1_3_entry.update()

            data_1_4_entry.delete(0, END)
            data_1_4_entry.insert(0, C_Vel[9])
            data_1_4_entry.update()

            data_1_5_entry.delete(0, END)
            data_1_5_entry.insert(0, R_Pos[9])
            data_1_5_entry.update()

            data_1_6_entry.delete(0, END)
            data_1_6_entry.insert(0, R_Vel[9])
            data_1_6_entry.update()

            fig_1.clear()
            ax_1 = fig_1.add_subplot(1, 1, 1)
            ax_1.set(ylim=[0, 120], title='Position')
            ax_1.plot(x_1, y_1_1, color='blue', label='L')
            ax_1.plot(x_1, y_1_2, color='red', label='C')
            ax_1.plot(x_1, y_1_3, color='green', label='R')
            ax_1.legend(loc='upper right')

            fig_2.clear()
            ax_2 = fig_2.add_subplot(1, 1, 1)
            ax_2.set(ylim=[0, 35], title='Velocity')
            ax_2.plot(x_2, y_2_1, color='blue', label='L')
            ax_2.plot(x_2, y_2_2, color='red', label='C')
            ax_2.plot(x_2, y_2_3, color='green', label='R')
            ax_2.legend(loc='upper right')

            canvas_1.draw()
            canvas_1.get_tk_widget().update()

            canvas_2.draw()
            canvas_2.get_tk_widget().update()

            new_x_1 = x_1[9] + 1
            del x_1[0]
            x_1.insert(9, new_x_1)
            del y_1_1[0]
            y_1_1.insert(9, L_Pos[9])
            del y_1_2[0]
            y_1_2.insert(9, C_Pos[9])
            del y_1_3[0]
            y_1_3.insert(9, R_Pos[9])

            new_x_2 = x_2[9] + 1
            del x_2[0]
            x_2.insert(9, new_x_2)
            del y_2_1[0]
            y_2_1.insert(9, L_Vel[9])
            del y_2_2[0]
            y_2_2.insert(9, C_Vel[9])
            del y_2_3[0]
            y_2_3.insert(9, R_Vel[9])

            time.sleep(1)

    def resume(self):
        self.running = True

    def pause(self):
        self.running = False



class Update_4(threading.Thread, Frame):
    def __init__(self, frame):
        super().__init__()
        self.daemon = True
        self.frame = frame
        self.running = True

    def run(self):
        # print
        data_1_1_entry = Entry(self.frame, justify='right')
        data_1_1_entry.place(x=745, y=433, width=55, height=22)

        data_1_2_entry = Entry(self.frame, justify='right')
        data_1_2_entry.place(x=745, y=463, width=55, height=22)

        data_1_3_entry = Entry(self.frame, justify='right')
        data_1_3_entry.place(x=885, y=433, width=55, height=22)

        data_1_4_entry = Entry(self.frame, justify='right')
        data_1_4_entry.place(x=885, y=463, width=55, height=22)

        data_1_5_entry = Entry(self.frame, justify='right')
        data_1_5_entry.place(x=1040, y=433, width=55, height=22)

        data_1_6_entry = Entry(self.frame, justify='right')
        data_1_6_entry.place(x=1040, y=463, width=55, height=22)

        data_1_7_entry = Entry(self.frame, justify='right')
        data_1_7_entry.place(x=1190, y=433, width=55, height=22)

        data_1_8_entry = Entry(self.frame, justify='right')
        data_1_8_entry.place(x=1190, y=463, width=55, height=22)

        # draw
        fig_1 = plt.figure()
        x_1 = [1+i for i in range(4)]
        y_1 = [0 for i in range(4)]
        xticks_1 = ['L_W', 'L_B', 'R_W', 'R_B']

        fig_2 = plt.figure()
        x_2 = [1+i for i in range(4)]
        y_2 = [0 for i in range(4)]
        xticks_2 = ['L_W', 'L_B', 'R_W', 'R_B']

        canvas_1 = FigureCanvasTkAgg(fig_1, master=self.frame)
        canvas_1.get_tk_widget().place(x=690, y=495, width=300, height=220)

        canvas_2 = FigureCanvasTkAgg(fig_2, master=self.frame)
        canvas_2.get_tk_widget().place(x=995, y=495, width=300, height=220)

        while self.running:
            data_1_1_entry.delete(0, END)
            data_1_1_entry.insert(0, L_W_Pos[9])
            data_1_1_entry.update()

            data_1_2_entry.delete(0, END)
            data_1_2_entry.insert(0, L_B_Pos[9])
            data_1_2_entry.update()

            data_1_3_entry.delete(0, END)
            data_1_3_entry.insert(0, R_W_Pos[9])
            data_1_3_entry.update()

            data_1_4_entry.delete(0, END)
            data_1_4_entry.insert(0, R_B_Pos[9])
            data_1_4_entry.update()

            data_1_5_entry.delete(0, END)
            data_1_5_entry.insert(0, L_W_Vel[9])
            data_1_5_entry.update()

            data_1_6_entry.delete(0, END)
            data_1_6_entry.insert(0, L_B_Vel[9])
            data_1_6_entry.update()

            data_1_7_entry.delete(0, END)
            data_1_7_entry.insert(0, R_W_Vel[9])
            data_1_7_entry.update()

            data_1_8_entry.delete(0, END)
            data_1_8_entry.insert(0, R_B_Vel[9])
            data_1_8_entry.update()

            fig_1.clear()
            ax_1 = fig_1.add_subplot(1, 1, 1)
            ax_1.set(ylim=[0, 400], title='Position')
            ax_1.bar(x_1, y_1, color='blue')
            ax_1.set_xticks(x_1)
            ax_1.set_xticklabels(xticks_1)

            fig_2.clear()
            ax_2 = fig_2.add_subplot(1, 1, 1)
            ax_2.set(ylim=[0, 400], title='Velocity')
            ax_2.bar(x_2, y_2, color='red')
            ax_2.set_xticks(x_2)
            ax_2.set_xticklabels(xticks_2)

            canvas_1.draw()
            canvas_1.get_tk_widget().update()

            canvas_2.draw()
            canvas_2.get_tk_widget().update()

            del y_1[0]
            y_1.insert(0, L_W_Pos[9])
            del y_1[1]
            y_1.insert(1, L_B_Pos[9])
            del y_1[2]
            y_1.insert(2, R_W_Pos[9])
            del y_1[3]
            y_1.insert(3, R_B_Pos[9])

            del y_2[0]
            y_2.insert(0, L_W_Vel[9])
            del y_2[1]
            y_2.insert(1, L_B_Vel[9])
            del y_2[2]
            y_2.insert(2, R_W_Vel[9])
            del y_2[3]
            y_2.insert(3, R_B_Vel[9])

            time.sleep(1)

    def resume(self):
        self.running = True

    def pause(self):
        self.running = False