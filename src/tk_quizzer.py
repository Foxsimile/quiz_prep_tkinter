import tkinter as tk
import string


class MasterWindow:
    def __init__(self):
        self.master_resize_event_funcs = []
        self.master = self.create_master()
        self.test_question = {'Q': 'What is the nature of life?', 'A': '42', 'B': 'idk', 'C': 'hamburder?', 'D': 'To make your dreams reality.', 'Ans': 'D', 'Sol': 'Dreams->Reality'}
        self.mcquestion_display = MCQuestionDisplay(self.master, self.test_question, self.add_func_to_resize_event_funcs)
    

    def create_master(self):
        master = tk.Tk()
        master.geometry('490x350')
        master.title('ACC180 Preparation')
        master.minsize(300,300)
        master.maxsize(1000, 1000)
        master.bind('<Configure>', self.master_resize_event_handler)
        return master

    
    def master_resize_event_handler(self, event):
        for x in range(len(self.master_resize_event_funcs)):
            self.master_resize_event_funcs[x].__call__(event)

    
    def add_func_to_resize_event_funcs(self, func):
        self.master_resize_event_funcs.append(func)


class MCQuestionDisplay:
    def __init__(self, master, question_dict, master_resize_func):
        self.master = master
        self.question_dict = question_dict
        self.question_dict['Q'] = 'START:lots and lots and lots and lots and lots and lots and lots and lots and lots and lots and lots and lots and lots and lots and lots and lots and lots and lots and LOTS OF TEXT'
        self.master_w_intvar = tk.IntVar()
        self.master_h_intvar = tk.IntVar()
        self.master_resize_event_list = []
        master_resize_func(self.mcquestion_master_resize_handler)
        self.update_master_width_height_intvars(self.master, self.master_w_intvar, self.master_h_intvar)
        self.mcquestion_main_frame = self.create_mcquestion_main_frame(self.master)
        self.question_frame = None
        self.question_label = None
        self.question_canvas = None
        self.question_width_percent = 0.666
        self.multichoice_radiobutton_groups = []
        self.multichoice_intvar = tk.IntVar()
        self.multichoice_width_percent = 0.8
        self.master_creation_overseer()


    def create_mcquestion_main_frame(self, frame):
        mcquestion_frame = tk.Frame(frame)
        mcquestion_frame.grid(row=1, column=0, padx=10, pady=10)
        return mcquestion_frame
    

    def master_creation_overseer(self):
        self.question_creation_overseer(self.mcquestion_main_frame, self.master_w_intvar, self.master_h_intvar, self.question_width_percent)
        self.mc_radiobuttons_creation_overseer(self.mcquestion_main_frame, self.master_w_intvar, self.master_h_intvar, self.multichoice_intvar)
    
    def question_creation_overseer(self, main_frame, w_intvar, h_intvar, question_width_percent):
        self.question_frame = self.create_question_frame(main_frame)
        self.question_canvas = self.create_question_canvas(self.question_frame, (w_intvar.get() * question_width_percent), self.resize_question_canvas_to_size)
        self.question_label = self.create_question_label(self.question_frame, self.resize_question_label_wraplength)


    def mcquestion_master_resize_handler(self, event):
        self.update_master_width_height_intvars(self.master, self.master_w_intvar, self.master_h_intvar)
        for x in range(len(self.master_resize_event_list)):
            self.master_resize_event_list[x][1](self.master_resize_event_list[x][0])


    def add_func_to_mcquestion_resize_list(self, widget, func):
        self.master_resize_event_list.append((widget, func))


    def update_master_width_height_intvars(self, master, w_intvar, h_intvar):
        self.update_intvar_from_val(master.winfo_width(), w_intvar)
        self.update_intvar_from_val(master.winfo_height(), h_intvar)

    
    def update_intvar_from_val(self, val, intvar):
        intvar.set(val)


    def configure_widget_width(self, widget, val):
        widget.configure(width=val)

    
    def create_question_frame(self, frame):
        question_frame = tk.Frame(frame, relief=tk.RIDGE, borderwidth=2, bg='black')
        question_frame.grid(column=0, row=0, padx=5, pady=5, columnspan=2, sticky=tk.NW)
        return question_frame

    
    def create_question_canvas(self, frame, w, resize_func):
        question_canvas = tk.Canvas(frame, width=w, height=0)
        question_canvas.grid(column=0, row=0, sticky=tk.NSEW)
        question_canvas.grid_propagate(0)
        self.add_func_to_mcquestion_resize_list(question_canvas, resize_func)
        return question_canvas


    def resize_question_canvas_to_size(self, widget):
        new_width = int(self.master_w_intvar.get() * self.question_width_percent)
        widget.configure(width=new_width)

    
    def create_question_label(self, frame, resize_func):
        question_label = tk.Label(frame, justify=tk.LEFT, wraplength=355, text=self.question_dict['Q'])
        question_label.grid(column=0, row=0, sticky=tk.W)
        self.add_func_to_mcquestion_resize_list(question_label, resize_func)
        return question_label

    
    def resize_question_label_wraplength(self, widget):
        new_width = int(self.master_w_intvar.get() * self.question_width_percent)
        widget.configure(wraplength=new_width)

    
    def mc_radiobuttons_creation_overseer(self, frame, w_intvar, h_intvar, intvar):
        intvar.set(0)
        self.mc_radiobutton_frame = self.create_mc_radiobutton_frame(frame)
        self.mc_radiobutton_canvas = self.create_mc_radiobutton_canvas(self.mc_radiobutton_frame, (w_intvar.get() * self.multichoice_width_percent), self.resize_mc_radiobutton_canvas)
        for x in range(1, 5):
            radiobutton_innerframe_x = self.create_mc_radiobutton_innerframe(self.mc_radiobutton_frame, (x - 1))
            radiobutton_innercanvas_x = self.create_mc_radiobutton_innercanvas(radiobutton_innerframe_x, (x - 1))
            radiobutton_x = self.create_radiobutton(radiobutton_innerframe_x, (string.ascii_uppercase[x - 1] + ' : '), intvar, x)
            #radiobutton_label_x = self.create_choice_label(radiobutton_innerframe_x, self.question_dict[string.ascii_uppercase[x - 1]], (x - 1), self.resize_mc_radiobutton_label_wraplength)
            radiobutton_label_x = self.create_choice_label(radiobutton_innerframe_x, self.question_dict['Q'], (x - 1), radiobutton_x, self.resize_mc_radiobutton_label_wraplength, self.factory_raise_event_on_alt_widget)
            self.multichoice_radiobutton_groups.append((radiobutton_x, radiobutton_label_x, radiobutton_innerframe_x, radiobutton_innercanvas_x))
    

    def create_mc_radiobutton_frame(self, frame):
        mc_radiobutton_frame = tk.Frame(frame)
        mc_radiobutton_frame.grid(column=0, row=1, pady=10, sticky=tk.NW)
        return mc_radiobutton_frame


    def create_mc_radiobutton_canvas(self, frame, w, resize_func):
        mc_radiobutton_canvas = tk.Canvas(frame, width=w, height=0, bg='white')
        mc_radiobutton_canvas.grid(column=0, row=0, columnspan=2, sticky=tk.NSEW)
        mc_radiobutton_canvas.grid_propagate(0)
        self.add_func_to_mcquestion_resize_list(mc_radiobutton_canvas, resize_func)
        return mc_radiobutton_canvas


    def resize_mc_radiobutton_canvas(self, widget):
        new_width = int(self.master_w_intvar.get() * self.multichoice_width_percent)
        widget.configure(width=new_width)

    
    def create_mc_radiobutton_innerframe(self, frame, row_val):
        mc_radiobutton_innerframe = tk.Frame(frame, borderwidth=2, bg='black', relief=tk.FLAT)
        mc_radiobutton_innerframe.grid(column=0, row=row_val, pady=2, sticky=tk.EW)
        return mc_radiobutton_innerframe

    
    def create_mc_radiobutton_innercanvas(self, frame, row_val):
        mc_radiobutton_innercanvas = tk.Canvas(frame, height=0)
        mc_radiobutton_innercanvas.grid(column=0, row=row_val, columnspan=2, sticky=tk.NSEW)
        self.add_func_to_mcquestion_resize_list(mc_radiobutton_innercanvas, self.resize_mc_radiobutton_innercanvas)
        return mc_radiobutton_innercanvas

    
    def resize_mc_radiobutton_innercanvas(self, widget):
        new_width = int(self.master_w_intvar.get() * self.multichoice_width_percent)
        widget.configure(width=new_width)

    
    def create_radiobutton(self, frame, text_string, control_var, int_val):
        radiobutton = tk.Radiobutton(frame, text=text_string, variable=control_var, value=int_val)
        radiobutton.grid(column=0, row=(int_val - 1), sticky=tk.EW)
        radiobutton.bind('<ButtonRelease>', self.factory_radiobutton_deselect(radiobutton, control_var))
        return radiobutton


    def factory_radiobutton_deselect(self, widget, control_var):
        def deselect_radiobutton(event):
            if control_var.get() == int(widget.cget('value')):
                control_var.set(0)
                return "break"
            else:
                control_var.set(int(widget.cget('value')))
                return "break"
        return deselect_radiobutton

    
    def create_choice_label(self, frame, choice_text, row_val, partner_radiobutton, resize_func, bind_func):
        choice_label = tk.Label(frame, justify=tk.LEFT, wraplength=400, text=choice_text)
        choice_label.grid(column=1, row=row_val, sticky=tk.W)
        self.add_func_to_mcquestion_resize_list(choice_label, resize_func)
        choice_label.bind('<ButtonRelease>', bind_func(partner_radiobutton, '<ButtonRelease>'))
        frame.columnconfigure(1, weight=1)
        return choice_label


    def resize_mc_radiobutton_label_wraplength(self, widget):
        new_width = int(self.master_w_intvar.get() * self.multichoice_width_percent)
        widget.configure(wraplength=new_width)

    
    def factory_raise_event_on_alt_widget(self, widget, event_string):
        def raised_event_by_alt_widget_handler(event):
            widget.event_generate(event_string)
        return raised_event_by_alt_widget_handler


if __name__ == "__main__":
    master_window = MasterWindow()
    master_window.master.mainloop()
