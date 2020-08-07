import tkinter as tk


class ProgressBar:
    def __init__(self, target, text, width, total=100):
        self.target = target
        self.count = 0
        self.total = total
        # 0 - 10000
        self.curr_progress = 0
        self.label_width = 104
        self.width = width
        # 进度条宽度
        self.bar_width = width - self.label_width
        # 文本宽度
        self.text_width = 57

        if type(text) == tk.StringVar:
            text_variable = text
            text = None
        else:
            text_variable = None
        self.frame = tk.Frame(target, width=width, height=30)
        self.label = tk.Label(self.frame, text=text, textvariable=text_variable,
                              width=10, height=1, anchor=tk.E, padx=5, pady=8)
        self.canvas = tk.Canvas(self.frame, width=self.bar_width, height=30, background='white')
        self.rectangle = self.canvas.create_rectangle(0, 0, 0, 30, fill='green')
        self.text = self.canvas.create_text((self.text_width, 17), width=self.text_width, text='0.00%', anchor=tk.E)
        self.label.place(x=0, y=0)
        self.canvas.place(x=self.label_width, y=0)

    def _update_(self):
        try:
            curr_width = int(self.curr_progress / 10000 * self.bar_width)
            if curr_width > self.bar_width:
                curr_width = self.bar_width
            config = {
                'text': '{:>.2f}%'.format(self.curr_progress / 100),
                'fill': 'black'
            }
            text_position = self.text_width
            if curr_width > self.text_width:
                text_position = curr_width
                config['fill'] = 'white'
            self.canvas.itemconfig(self.text, **config)
            self.canvas.coords(self.rectangle, (0, 0, curr_width, 30))
            self.canvas.coords(self.text, (text_position, 17))
            self.frame.update()
            return True
        except tk.TclError:
            return False

    def set_total(self, total):
        self.total = total

    def place(self, x, y, floor=0):
        self.frame.place(x=x, y=y + (30 * floor))

    def reset(self):
        self.count = 0
        self.curr_progress = 0
        self._update_()

    def update(self, num=1):
        self.count += num
        self.curr_progress = int(self.count / self.total * 10000)
        self._update_()

