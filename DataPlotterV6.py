print("Hello Big Money.........Be patient...........")
import os
from pathlib import Path
print("Almost there, calm down now")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
print("Quiet Please.......................shhhhhhhhhhhhh")
from matplotlib.widgets import Button
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
print("Welcome, Big Money")


def create_buttons():
    #global button2, delete, maxTemp, maxPressure, plot_temp, root
    global color1, button2
    #frame = tk.Frame(root, bg='lightgray',bd=3 ,relief='groove')
    frame = tk.Frame(root, bg=color1, bd=5,relief = 'groove')
    #frame.pack(side=tk.TOP,fill='x')
    frame.pack(side=tk.TOP)
    button = tk.Button(frame, text="Data Points", fg="blue", anchor='n',command=lambda: edit_labels("toggle"))
    button.pack(side='left',padx=5, pady=12)
    b2_param = ["Enable Delete Mode", "blue"]
    if delete is True:
        b2_param = ["Disable Delete Mode", "red"]
    button2 = tk.Button(frame, text=b2_param[0], anchor='n',fg=b2_param[1], command=delete_ann)
    button2.pack(side='left',padx=5)
    button3 = tk.Button(frame, text="TickMarks", anchor='n', fg="blue", command=tick_messagebox)
    button3.pack(side='left',padx=5)
    button4 = tk.Button(frame, text="X-Gridlines", fg="blue", command=lambda: grid_lines(True,False))
    button4.pack(side='left',padx=5)
    button4_1 = tk.Button(frame, text="Y-Gridlines", fg="blue", command=lambda: grid_lines(False,True))
    button4_1.pack(side='left',padx=5)
    button5 = tk.Button(frame, text="Reference Time", fg="blue", command=update_ref_box)
    button5.pack(side='left',padx=5)
    button7= tk.Button(frame,text='Add Data', fg='blue',command=add_data)
    button7.pack(side='left',padx=5)
    button8 = tk.Button(frame,text='Toggle Lines', fg='blue',command=toggle_lines_menu)
    button8.pack(side='left',padx=5)
    button6 = tk.Button(frame, text="Temp On/Off", fg="blue", command=toggle_temperature)
    button6.pack(side='left',padx=5)
    try:
        Mtemp_lbl = tk.Label(frame, text="Max Temperature: " + '\n'+ str("{:.2f}".format((max(Temperature)))), relief='sunken',bg='white smoke',fg="red")
    except:
        Mtemp_lbl = tk.Label(frame, text="No Temperature Data", relief='sunken',bg='white smoke',fg="red")
    Mtemp_lbl.pack(side='left',padx=5)
    Mpress_lbl = tk.Label(frame, text="Max Pressure: " + '\n'+ str("{:.2f}".format((max(Pressure)))),relief='sunken', bg='white smoke',fg="blue")
    Mpress_lbl.pack(side='left',padx=5)

def add_data():
    contents = open_file()
    main_data = choose_data_columns(contents)
    data_columns1 = main_data.return_data_columns()
    date1,real_time1,elapsed_time1,pressure1,temperature1 = process_data(data_columns1,contents)
    plot_data(date1,real_time1,elapsed_time1,pressure1,temperature1,1)
    fig.canvas.draw()

def toggle_lines_menu():
    print('toggle_lines')
    lines_window = tk.Toplevel()
    lines_window.title("Toggle Lines")
    frame = tk.Frame(lines_window)
    frame.pack(side=tk.TOP)
    line1 = tk.IntVar(value=1)
    checkbox1 = tk.Checkbutton(frame, text='Pressure 1',variable=line1, onvalue=True, offvalue=False)
    checkbox1.pack(side=tk.TOP, anchor = 'w')
    line2 = tk.IntVar(value=1)
    checkbox2 = tk.Checkbutton(frame, text='Temperature 1', variable=line2, onvalue=True, offvalue=False)
    checkbox2.pack(side=tk.TOP, anchor = 'w')
    line3 = tk.IntVar(value=1)
    checkbox3 = tk.Checkbutton(frame, text='Pressure 2', variable=line3, onvalue=True, offvalue=False)
    checkbox3.pack(side=tk.TOP, anchor = 'w')
    line4 = tk.IntVar(value=1)
    checkbox4 = tk.Checkbutton(frame, text='Temperature 2', variable=line4, onvalue=True, offvalue=False)
    checkbox4.pack(side=tk.TOP, anchor = 'w')
    frame2 = tk.Frame(lines_window)
    frame2.pack(side=tk.TOP)
    enter_btn = tk.Button(frame2, text="Submit", command=lambda: toggle_lines(line1.get(),line2.get(),line3.get(),line4.get()))
    enter_btn.pack(side=tk.BOTTOM,pady=5)

def toggle_lines(pressure,temp,pressure2,temp2):
    if pressure == 0:
        ax.lines[0].set_visible(False)
    if pressure == 1:
        ax.lines[0].set_visible(True)
    if temp == 0:
        ax2.lines[0].set_visible(False)
    if temp == 1:
        ax2.lines[0].set_visible(True)
    if pressure2 == 0 and len(ax.lines) > 1:
        ax.lines[1].set_visible(False)
    if pressure2 == 1 and len(ax.lines) > 1:
        ax.lines[1].set_visible(True)
    if temp2 == 0 and len(ax2.lines) > 1:
        ax2.lines[1].set_visible(False)
    if temp2 == 1 and len(ax2.lines) > 1:
        ax2.lines[1].set_visible(True)
    fig.canvas.draw()


def update_ref_box():
    global Root, updated_elapsed_ref, updated_real_ref
    global Root
    try:
        Root.withdraw()
    except:
        print("Exception No window")
    Root = tk.Toplevel()
    Root.geometry("250x250")
    Root.resizable(False, False)
    Frame = tk.Frame(Root)
    Frame.pack()
    Root.title("Update Ref Time")
    entry1 = tk.Entry(Frame)
    label1 = tk.Label(Frame, text="Enter Hours (x.xx)")
    entry2 = tk.Entry(Frame)
    label2 = tk.Label(Frame, text="Enter Real Time (xx:xx:xx)")
    label3 = tk.Label(Frame,text="Current Reference Time"+ "\n"+ str(updated_elapsed_ref)+ "\n"+ str(updated_real_ref),)
    enter_btn = tk.Button(Frame, text="Submit", command=lambda: update_ref(entry2.get(), entry1.get()))
    label1.pack()
    entry1.pack()
    label2.pack()
    entry2.pack()
    enter_btn.pack()
    label3.pack()


def user_input(num, text):
    valid_input = False
    plot = True
    while valid_input is False:
        x = simpledialog.askstring(title="Input", prompt=text)
        if x.isdigit() is False and num == 0:
            print("Must be a number clown")
            continue
        if num == 1 and x.upper() == "X":
            plot = False
            print("Plot temp = false")
        elif num == 1 and x.isdigit() is False:
            print("Must be a number clown")
            continue
        return x, plot


def create_annotation(x_data, y_data):
    global Root2
    try:
        Root2.withdraw()
    except:
        print("Exception No window")
    Root2 = tk.Toplevel()
    Root2.title("Annotation")
    Frame2 = tk.Frame(Root2)
    Frame2.pack()
    Root2.geometry("250x250")
    print("x and y value = ", x_data, y_data)
    clock_time = convert_to_real_time(x_data)
    label= tk.Label(Frame2, text="Hours")
    label.pack()
    elapsed = tk.Text(Frame2,fg='blue',height=1,width=15)
    elapsed.insert(tk.END,str(x_data))
    elapsed.pack()
    label2= tk.Label(Frame2, text="Real Time")
    label2.pack()
    real = tk.Text(Frame2,fg='blue',height=1,width=15)
    real.insert(tk.END,str(clock_time[1]))
    real.pack()
    label3 = tk.Label(Frame2, text="Pressure")
    label3.pack()
    pressure_lbl = tk.Text(Frame2,fg='blue',height=1,width=15)
    pressure_lbl.insert(tk.END,str(y_data))
    pressure_lbl.pack()
    pressure_checkbox = tk.IntVar()
    checkbox1 = tk.Checkbutton(Frame2, text="Check box to show pressure", variable=pressure_checkbox, onvalue=True, offvalue=False)
    checkbox1.pack()
    label3= tk.Label(Frame2, text="Enter Label")
    label3.pack()
    label_entry = tk.Entry(Frame2)
    label_entry.pack()
    enter_btn2 = tk.Button(Frame2, text="Submit", command=lambda: label_annotation(label_entry.get(),x_data,y_data,pressure_checkbox.get()))
    enter_btn2.pack()
    print("x and y value = ", x_data, y_data)


def label_annotation(label,x_data,y_data,show_pressure):
    annotation_text = label
    print(label,x_data,y_data,show_pressure)
    if show_pressure == 1:
        annotation_text = label + "\n" + str(round(y_data, 2))
    annotation = ax.annotate(
        annotation_text,
        xy=(x_data, y_data),
        xytext=(x_data, y_data + y_data * 0.01),
        arrowprops={"arrowstyle": "->", "color": "black", "connectionstyle": "arc3"},
    )
    annotation.draggable(True)
    fig.canvas.draw()


def tick_messagebox():  # tick message box is called by clicking "TickMarks" button
    global Root
    try:
        Root.withdraw()
    except:
        print("Exception No window")
    Root = tk.Toplevel()
    Root.geometry("250x250")
    Root.resizable(False, False)
    Frame = tk.Frame(Root)
    Frame.pack()
    Root.title("Tick Mark Options")
    entry1 = tk.Entry(Frame)
    label1 = tk.Label(Frame, text="Enter Min")
    entry2 = tk.Entry(Frame)
    label2 = tk.Label(Frame, text="Enter Max")
    entry3 = tk.Entry(Frame)
    label3 = tk.Label(Frame, text="Enter # of TickMarks")
    entry4 = tk.Entry(Frame)
    label4 = tk.Label(Frame, text="Enter X, Y or T")
    var_checkbox = tk.IntVar()
    checkbox = tk.Checkbutton(Frame, text="Check box for Real Time", variable=var_checkbox, onvalue=1, offvalue=0)
    enter_btn = tk.Button(
        Frame,
        text="Submit",
        command=lambda: tick_marks(
            entry1.get(),
            entry2.get(),
            entry3.get(),
            str(entry4.get()),
            var_checkbox.get(),
        ),
    )
    label1.pack()
    entry1.pack()
    label2.pack()
    entry2.pack()
    label3.pack()
    entry3.pack()
    label4.pack()
    entry4.pack()
    checkbox.pack()
    enter_btn.pack()


# --------------EVENTS--------------------------------------------------------------------------------------------
def onpick(event):  # this allows selection of the actual data
    #global delete
    thisline = event.artist
    print("OnpickEvent", event, thisline, type(thisline), id(thisline), sep="|||")
    if "Line2D" in str(thisline):  # Pressure data point picked, create annotation
        xdata = thisline.get_xdata()
        ydata = thisline.get_ydata()
        ind = event.ind
        points = tuple(zip(xdata[ind], ydata[ind]))
        print("onpick points:", points[0][0], points[0][1])
        create_annotation(float(points[0][0]), float(points[0][1]))
        return
    elif "Annotation" in str(thisline) and delete is True:  #
        thisline.remove()
        fig.canvas.draw()
        return
    else:
        return  # do nothing


def on_click(click):
    print(click)
    if click.dblclick:
        fig_width, fig_height = fig.get_size_inches() * fig.dpi
        print(fig_width, fig_height)
        if str(click.xdata) == "None":
            print(click.x, 1 / 3 * fig_width)
            if (
                click.x < click.y and int(click.x) < 1 / 8 * fig_width
            ):  # y-axis selected
                if (
                    float(click.y) > 0.45 * fig_height
                    and float(click.y) < 0.55 * fig_height
                ):
                    edit_labels("y_label")
                else:
                    edit_labels("y_lim")
                return  # exits function
            if (
                click.x > click.y and int(click.y) < 1 / 8 * fig_height
            ):  # x-axis selected
                if (
                    float(click.x) > 0.45 * fig_width
                    and float(click.x) < 0.55 * fig_width
                ):
                    edit_labels("x_label")
                else:
                    edit_labels("x_lim")
                return
            if (
                click.x > click.y and int(click.x) > 7 / 8 * fig_width
            ):  # y2-axis selected
                if (
                    float(click.y) > 0.45 * fig_height
                    and float(click.y) < 0.55 * fig_height
                ):
                    edit_labels("y2_lbl")
                else:
                    edit_labels("y2_lim")
                return
            if int(click.y) > 7 / 8 * fig_height:  # Plot title selected
                edit_labels("plt_title")
                return
        #if click.xdata > 0:
            #create_buttons()


def on_key(event):
    #global delete, plot_temp
    print("you pressed", event.key, event.xdata, event.ydata)
    if event.key == "delete":  # enable delete mode
        messagebox.showinfo("DELETE MODE ENABLED", "DELETE MODE ENABLED")
        delete = True
        return
    if event.key == "escape":  # disable delete mode
        messagebox.showinfo("DELETE MODE DISABLED", "Delete mode disabled")
        delete = False
        return
    if event.key == "f1":  # display or hide data points
        edit_labels("toggle")
    if event.key == "f2":  # set temp axis min/max
        if plot_temp is True:
            edit_labels("y2_lim")
    if event.key == "f3":  # set pressure axis min/max
        edit_labels("y_lim")
    if event.key == "f4":  # set x axis title and title title
        edit_labels("x_label")
    if event.key == "f12":
        for child in ax.get_children():
            print(child)
        if plot_temp is True:
            print("xxxxxx")
            for child in ax2.get_children():
                print(child)
    if event.key == "f11":
        y_coord = []
        x_coord = []
        xy = []
        for tick in ax.get_xticks():
            y_coord.append(float("0"))
            x_coord.append(float(tick))
            print(tick)
        # print(y_coord)
        # print(x_coord)
        xy = list(zip(x_coord, y_coord))
        return(xy)
        # print(xy)
        # ax.text(xy[5][0],xy[5][1],'xx:xx:xx',)
        #plt.show()


# -----------------END EVENTS----------------------------------------------------------------------------------


def edit_labels(var):
    if var == "plt_title":
        title = simpledialog.askstring(title="Set Plot Title", prompt="Enter Plot Title")
        ax.set_title(title, pad=10)
        fig.canvas.draw()
    if var == "x_label":
        xlabel = simpledialog.askstring(
            title="Set X-AXIS Title", prompt="Enter X Label"
        )
        ax.set_xlabel(xlabel)
    if var == "x_lim":
        low = float(simpledialog.askstring(title="Min", prompt="Enter Start Time"))
        high = float(simpledialog.askstring(title="Max", prompt="Enter End Time"))
        ax.set_xlim(low, high)
        ax3.set_xlim(low, high)
    if var == "y_label":
        ylabel = simpledialog.askstring(
            title="Set Y-AXIS Title", prompt="Enter Y Label"
        )
        ax.set_ylabel(ylabel)
    if var == "y_lim":
        low = int(simpledialog.askstring(title="Min", prompt="Enter Min Pressure"))
        high = int(simpledialog.askstring(title="Max", prompt="Enter Max Pressure"))
        ax.set_ylim(low, high)
    if var == "y2_lim":
        low = int(simpledialog.askstring(title="Min", prompt="Enter Min Temperature"))
        high = int(simpledialog.askstring(title="Max", prompt="Enter Max Temperature"))
        ax2.set_ylim(low, high)
    if var == "y2_lbl":
        y2label = simpledialog.askstring(
            title="Set Y-AXIS Title", prompt="Enter Y Label"
        )
        ax2.set_ylabel(y2label)
    if var == "toggle":  # display or hide data points
        for i in range(
            len(ax.lines)
        ):  # find the Pressure line to add and remove data points
            name = str(ax.lines[i])
            if "Pressure" in name:
                num = i
        data_marker = str(ax.lines[0].get_marker())
        if data_marker == "None":
            ax.lines[0].set_marker(".")
            fig.canvas.draw()
            return
        else:
            ax.lines[0].set_marker(None)
            fig.canvas.draw()
            return
    fig.canvas.draw()


def delete_ann():
    #global delete, button2
    global delete
    if delete is True:
        button2["text"] = "Enable Delete Mode"
        button2["fg"] = "blue"
        delete = False
        return
    if delete is False:
        button2["text"] = "Disable Delete Mode"
        button2["fg"] = "red"
        delete = True
        return
    fig.canvas.draw()


# Tick Mark------------
def tick_marks(minimum, maximum, interval, axis, check_button):
    #global plot_temp
    print("edit tick marks", minimum, maximum, interval, axis, check_button, sep="---")
    i = 0
    low = float(minimum)
    high = float(maximum)
    tick_num = int(interval)
    interval = float((high - low) / tick_num)
    if axis.upper() == "Y":
        ax.set_ylim(low, high)
        y_ticks = [low]
        while i < tick_num:
            i += 1
            y_ticks.append(low + interval * i)
        ax.set_yticks(y_ticks)
        print(y_ticks)
    if axis.upper() == "X":
        ax.set_xlim(low, high)
        ax3.set_xlim(low, high)
        x_ticks = [round(low, 2)]
        while i < tick_num:
            i += 1
            # next_tick = '{:.2f}'.format(low+interval*i)
            next_tick = round(low + interval * i, 2)
            x_ticks.append(next_tick)
            # x_ticks.append('{:.2f}'.format(low + interval*i))
        ax.set_xticks(x_ticks, minor=False)
        ax3.set_xticks(x_ticks, minor=False)
        ax.tick_params(
            axis="x",
            bottom=True,
            top=False,
            labelbottom=True,
            labeltop=False,
            rotation=0,
            zorder=0,
        )
        ax3.tick_params(
            axis="x", bottom=False, top=False, labelbottom=False, labeltop=False
        )
        if check_button == 1:
            real_ticks = []
            for nums in range(0, len(x_ticks), 1):
                clock_time = convert_to_real_time(x_ticks[nums])
                real_ticks.append(clock_time[0])
            print(real_ticks)
            zip_labels = list(zip(x_ticks, real_ticks))
            print(zip_labels)
            tick_labels = []
            for a in range(0, len(zip_labels), 1):
                combine = str(zip_labels[a][0]) + "\n" + str(zip_labels[a][1])
                tick_labels.append(combine)
            ax.set_xticklabels(x_ticks)
            ax3.set_xticklabels(real_ticks)
            ax.tick_params(
                axis="x",
                bottom=True,
                top=False,
                labelbottom=True,
                labeltop=False,
                labelsize=8,
                rotation=0,
                zorder=0,
            )
            ax3.tick_params(
                axis="x",
                bottom=False,
                top=True,
                labelbottom=False,
                labeltop=True,
                labelsize=8,
                rotation=0,
                zorder=0,
            )
    if axis.upper() == "T" and len(Temperature) > 10:
        ax2.set_ylim(low, high)
        T_ticks = [low]
        while i < tick_num:
            i += 1
            T_ticks.append(low + interval * i)
        ax2.set_yticks(T_ticks)
        print(T_ticks)
    fig.canvas.draw()


def update_ref(real, elapsed):
    global updated_elapsed_ref, updated_real_ref, use_updated_ref
    use_updated_ref = True
    updated_real_ref = real
    updated_elapsed_ref = elapsed
    print(updated_real_ref, updated_elapsed_ref)
    tick_list = []
    for tick in ax.get_xticks():
        tick_list.append(tick)
    tick_marks(min(tick_list),max(tick_list),len(tick_list)-1,'x',1)
    update_ref_box()


def get_reference_time(updated):
    #global x, time, updated_real_ref, updated_elapsed_ref
    global updated_real_ref, updated_elapsed_ref
    if updated is False:
        real_ref = Real_Time[0]
        elapsed_ref = float(Elapsed_Time[0])
    else:
        real_ref = updated_real_ref
        elapsed_ref = updated_elapsed_ref
    return real_ref, elapsed_ref


def convert_to_real_time(elapsed_time):
    #global x, time, use_updated_ref  # x and time are from the actual data imported
    global use_updated_ref
    real_ref, elapsed_ref = get_reference_time(use_updated_ref)
    elapsed_ref = float(elapsed_ref)
    delta_time = elapsed_time - elapsed_ref
    delta_hours = int(delta_time)
    delta_minutes = int((delta_time - delta_hours) * 60)
    delta_seconds = round((delta_time - delta_hours - delta_minutes / 60) * 60 * 60, 0)
    split_real_ref = real_ref.split(":")
    real_hours = int(split_real_ref[0]) + delta_hours
    real_minutes = int(split_real_ref[1]) + delta_minutes
    real_seconds = int(split_real_ref[2]) + delta_seconds
    if elapsed_time >= elapsed_ref:
        if real_seconds > 59:
            real_seconds = real_seconds - 60
            real_minutes = real_minutes + 1
        if real_minutes > 59:
            real_minutes = real_minutes - 60
            real_hours = real_hours + 1
        while real_hours > 23:
            real_hours = real_hours - 24
    if elapsed_time < elapsed_ref:
        if real_seconds < 0:
            real_seconds = 60 + real_seconds
            real_minutes = real_minutes - 1
        if real_minutes < 0:
            real_minutes = 60 + real_minutes
            real_hours = real_hours - 1
        while real_hours < 0:
            real_hours = 24 + real_hours
    if len(str(round(real_seconds))) < 2:
        real_seconds = "0" + str(round(real_seconds))
    else:
        real_seconds = round(real_seconds)
    if len(str(real_minutes)) < 2:
        real_minutes = "0" + str(real_minutes)
    if len(str(real_hours)) < 2:
        real_hours = "0" + str(real_hours)
    real_time1 = (
        str(real_hours) + ":" + str(real_minutes) + ":" + str(real_seconds)
    )  # xx:xx:xx
    real_time = str(real_hours) + ":" + str(real_minutes)  # xx:xx
    # print("Reference times are:", split_real_ref,real_ref,elapsed_ref,sep=' || ')
    # print("Delta Times are:",delta_hours,delta_minutes,delta_seconds,sep=' || ')
    print("Real Times are:", real_hours, real_minutes, real_seconds, sep=" || ")
    return real_time, real_time1


def grid_lines(x,y):
    #global root,fig
    # plt.grid()
    if x is True:
        ax.grid(axis="x")
    if y is True:
        ax.grid(axis="y")
    fig.canvas.draw()


def toggle_temperature():
    if ax2.get_visible() is True:
        ax2.set_visible(False)
    else:
        ax2.set_visible(True)
    fig.canvas.draw()


def open_file():
    file_path = filedialog.askopenfilename()
    file = Path(file_path)
    open_file = open(file)
    contents = open_file.readlines()  # read contents, and store in list
    open_file.close()  # close file
    return contents

class choose_data_columns():
    global color1,color2
    def __init__(self,contents):
        self.date = ''
        self.time = ''
        self.elapsed = ''
        self.pressure = ''
        self.temperature = ''
        self.data_columns = []
        #root.withdraw()
        # Print sample of file for user to see columns
        self.sample_window = tk.Toplevel(root,bg=color2)
        sample_window_frame = tk.Frame(self.sample_window,bg=color2)
        entry_frame = tk.Frame(self.sample_window,bg=color2,pady=8)
        label_frame = tk.Frame(self.sample_window,bg=color2)
        instruction_frame = tk.Frame(self.sample_window,pady=10, bg=color2)
        entry1 = tk.Entry(entry_frame)
        entry2 = tk.Entry(entry_frame)
        entry3 = tk.Entry(entry_frame)
        entry4 = tk.Entry(entry_frame)
        entry5 = tk.Entry(entry_frame)
        label1 = tk.Label(label_frame,text='Date',padx=40,bg=color2)
        label2 = tk.Label(label_frame,text='Real Time',padx=40,bg=color2)
        label3 = tk.Label(label_frame,text='Hours',padx=40,bg=color2)
        label4 = tk.Label(label_frame,text='Pressure',padx=40,bg=color2)
        label5 = tk.Label(label_frame,text='Temperature',padx=40,bg=color2)
        instructions = tk.Label(instruction_frame,text='Enter Column Number (1-5) or Enter X to Skip',
            relief='groove',bg='white',width = 100)
        submit_btn = tk.Button(self.sample_window,text='CLICK HERE TO CONTINUE', pady = 8,
            command= lambda: self.set_columns(entry1.get(),entry2.get(),entry3.get(),entry4.get(),entry5.get()))
        sampleX = []
        counter = 0
        label1.pack(side=tk.LEFT)
        label2.pack(side=tk.LEFT)
        label3.pack(side=tk.LEFT)
        label4.pack(side=tk.LEFT)
        label5.pack(side=tk.LEFT)
        entry1.pack(side=tk.LEFT)
        entry2.pack(side=tk.LEFT)
        entry3.pack(side=tk.LEFT)
        entry4.pack(side=tk.LEFT)
        entry5.pack(side=tk.LEFT)
        instructions.pack()
        instruction_frame.pack(side=tk.TOP)
        counter1=0
        for i in range(50, len(contents), int((len(contents)-50)/25)):
            sampleX = contents[i].split()
            #for n in range(0,len(sampleX),1):
            counter1 +=1
            for counter in range(0,len(sampleX),1):
                tk.Label(sample_window_frame, text=sampleX[counter], bg=color1, width=18, justify=tk.RIGHT).grid(row=counter1,column=counter)
        label_frame.pack(side=tk.TOP)
        entry_frame.pack(side=tk.TOP)
        sample_window_frame.pack(side=tk.TOP,pady=10)
        submit_btn.pack(side=tk.TOP)
        self.sample_window.wait_window()

    def set_columns(self,a,b,c,d,e):
        self.date = a
        self.time = b
        self.elapsed = c
        self.pressure = d
        self.temperature = e
        if a.isdigit() is True:
            list1 = [self.date,True]
        else:
           list1 = [self.date,False]
        if b.isdigit() is True:
            list2 = [self.time,True]
        else:
            list2 = [self.time,False]
        if c.isdigit() is True:
            list3 = [self.elapsed,True]
        else:
            list3 = [self.elapsed,False]
        if d.isdigit() is True:
            list4 = [self.pressure,True]
        else:
            list4 = [self.pressure,False]
        if e.isdigit() is True:
            list5 = [self.temperature,True]
        else:
            list5 = [self.temperature,False]
        self.data_columns = [list1,list2,list3,list4,list5]
        self.sample_window.destroy()

    def return_data_columns(self):
        return self.data_columns


def process_data(data,contents1):
    # Process data for plotting.............................
    date = []  # empty list for date
    time = []
    x = []  # empty list for x value
    y = []  # empty list for y values
    y2 = []  # empty list for temperature
    xy = []  # empty list to store return value of .readlines()
    no_data = 0
    # x_value_previous = 0
    # x_value = 0
    # Create list of x values and list of y values by splitting the contents list
    for lines in range(0, len(contents1), 1):
        xy = contents1[lines].split()  # splits string xy into values, removes blanks
        try:
            # user_input returns a list for time_column, pressure_column, temperature_column
            if data[4][1] is True:
                y2_value = float(xy[int(data[4][0]) - 1])  # this is temperature
            if data[0][1] is True:
                date_value = xy[int(data[0][0]) - 1] #date column
            if data[1][1] is True: #Real Time
                time_value = xy[int(data[1][0]) - 1]
            x_value = float(xy[int(data[2][0]) - 1])  # this is elapsed time column
            y_value = float(xy[int(data[3][0]) - 1])  # this is pressure
        except Exception:
            no_data += 1
            if (
                no_data > 500
            ):  # bad data, or wrong column selected, stop trying after 500 faild attempts
                break
            continue  # if bad data is encountered, skip this iteration and go to next
        # append list with data
        if data[0][1] is True:
            date.append(date_value)  # date
        if data[1][1] is True:
            time.append(time_value)  # time
        x.append(x_value)  # hours
        y.append(y_value)  # pressure
        if data[4][1] is True:
            y2.append(y2_value)  # temperature
    # Create dictionary where elapsed time is item and real time is value
    real_time = dict(zip(x, time))
    return date,time,x,y,y2

def plot_data(date,real_time,elapsed_time,pressure,temperature,i):
    if i == 0: # this is the initial data added
        if len(temperature) > 2:
            maxTemp = max(temperature)
            print("MAX TEMPERATURE RECORDED IS ", maxTemp)
            minTemp = min(temperature)
            ax2.set(ylabel="degF")
            ax2.plot(elapsed_time, temperature, color="red", label="Temperature")
            ax2.set_ylim(0, maxTemp + 5)
            ax2.tick_params(axis="y", labelsize=8)
            ax.set_alpha(0)  # makes main AXES transparent so the Temperature line is visible
            ax.set_facecolor("none")  # no color for main AXES
            ax.set_zorder(1)  # set main axe on top so that pickevent will attach to it
            ax2.set_zorder(0)  # sets ax2 on bottom
        ax.set(xlabel="Time: Hours", ylabel="psia")
        ax.set_title(label="TCP Pressure Data", pad=10)
        ax.plot(elapsed_time, pressure, picker=True, pickradius=2, color="blue", label="Pressure", marker=None)
        ax.tick_params(axis="x", labelsize=8)
        ax.tick_params(axis="y", labelsize=8)
        ax3.plot(elapsed_time, pressure, visible=False) #ax3 allows real time labels at the top
        ax3.tick_params(axis="x", bottom=False, top=False, labelbottom=False, labeltop=False)
    else:
        ax.plot(elapsed_time,pressure,color="purple")
        if len(temperature) > 2:
            ax2.plot(elapsed_time,temperature,color='yellow')
            ax2.set_visible(True)
        print("Data Added")








# Main Code is Below------------------------------------------
#below variables defined in global scope for use within functions
updated_elapsed_ref = 0
updated_real_ref = "00:00:00"
use_updated_ref = False
delete = False
color1 = 'gray95'
color2 = 'gray80'
#entry1, entry2, entry3 = [0, 0, 0]

#define main window "root" in global scope
root = tk.Tk()
root.configure(bg=color1)
#open files and process data
Contents = open_file()

main_data = choose_data_columns(Contents)
data_columns = main_data.return_data_columns()
#data_columns = main_data.data_columns()

Date,Real_Time,Elapsed_Time,Pressure,Temperature = process_data(data_columns,Contents)

#create main fig, AXES and axises in the global scope
fig, ax = plt.subplots()  # create the canvas (fig) and the AXES (pressure_ax)
ax3 = ax.twiny()
ax2 = ax.twinx()
if len(Temperature) < 2:
    ax2.set_visible(False)


#plot the data
plot_data(Date,Real_Time,Elapsed_Time,Pressure,Temperature,0) #the zero indicates first time plotting

fig.canvas.mpl_connect("button_press_event", on_click)  # mouse clicks
fig.canvas.mpl_connect("key_press_event", on_key)  # key presses
fig.canvas.mpl_connect("pick_event", onpick)  # allows selection of data points
root.deiconify()
root.title("DataPlotterV6")
imbed_plot = FigureCanvasTkAgg(fig, root)
toolbar = NavigationToolbar2Tk(imbed_plot,root)
imbed_plot.get_tk_widget().pack(side=tk.BOTTOM,fill=tk.BOTH, expand=True)
create_buttons()
root.mainloop()



