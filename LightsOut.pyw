import tkinter as tk
from tkinter import Toplevel
from random import randint
from datetime import datetime

class MenuWin(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Menu')
        self.geometry('220x160')
        self.resizable(False, False)
        
        self.lamps = tk.StringVar()
        self.default = tk.StringVar()
        self.lamps.set('5')
        self.default.set('1')

        self.lamp_Label = tk.Label(self,
            text='Total Lamps',
            font=('Comic Sans MS', 12,'bold')).pack(fill=None)
        
        self.lamp_Entry = tk.Entry(self, 
            textvariable=self.lamps, 
            font=('Comic Sans MS', 10,'bold'), 
            justify='center', 
            width=5, 
            validate="key", 
            validatecommand=(self.register(self.validate_lamps), self,'%P')).pack(fill=None)

        self.start_Label = tk.Label(self, 
            text='Lamps already on', 
            font=('Comic Sans MS', 12,'bold')).pack(fill=None)
        
        self.start_Entry = tk.Entry(self,
            textvariable=self.default,
            font=('Comic Sans MS', 10,'bold'),
            justify='center',
            width=5,
            validate="key", validatecommand=(self.register(self.validade_default), self,'%P')).pack(fill=None)

        self.start_Button = tk.Button(self,
            text='Start',
            font=('Comic Sans MS', 12,'bold'),
            height = 1,
            width = 10,
            command = self.open_game).pack(side='bottom')
        self.bind("<Return>", (lambda event: self.open_game()))

    def validate_lamps(self,root,lamps):
        if len(lamps) == 0 or lamps.isdigit() and 0 < int(lamps) <= 10:
            self.default.set(0)
            return True
        else:
            return False
    def validade_default(self,root,default):
        if len(default) == 0 or default.isdigit() and int(default) < int(self.lamps.get()):
            return True
        else:
            return False
    
    def open_game(self):
        self.newGameWin = GameWin(self, int(self.lamps.get()), int(self.default.get()))
        self.newGameWin.bind('<Escape>',lambda event: self.newGameWin.destroy())
        self.newGameWin.focus()


class GameWin(Toplevel):
    def __init__(self, root, lamps, default):
        super().__init__(root)

        self.title('Lights Out!')
        self.geometry(f'{58 * lamps}x70')
        self.resizable(False, False)

        self.dic = {
            True:'■',
            False:'□'
            }

        self.starting_time = datetime.now()

        self.lamps_list = [False for i in range(lamps)]
        while self.lamps_list.count(True) != default:
            self.lamps_list[randint(0,lamps-1)] = True
        
        for i in range(lamps):
            tk.Button(self,
                text = self.dic[self.lamps_list[i]],
                font = ('Comic Sans MS', 10,'bold'),
                height = 3,
                width = 6,
                command = lambda j=i: self.switch_lamps(self,j)).grid(row = 0, column = i)
            
    def switch_lamps(self,root,i):
        try:
            if i == 0:
                self.lamps_list[0] = not self.lamps_list[0]
                self.lamps_list[1] = not self.lamps_list[1]
            elif i == len(self.lamps_list)-1:
                self.lamps_list[-1] = not self.lamps_list[-1]
                self.lamps_list[-2] = not self.lamps_list[-2]
            else:
                self.lamps_list[i-1] = not self.lamps_list[i-1]
                self.lamps_list[i] = not self.lamps_list[i]
                self.lamps_list[i+1] = not self.lamps_list[i+1]
        except:
            pass
    
        for index, i in enumerate(self.winfo_children()):
            i['text'] = self.dic[self.lamps_list[index]]
        
        if all(self.lamps_list):
            for i in self.winfo_children():
                i.destroy()
            self.winner_Label = tk.Label(self, 
                text = f"{round((datetime.now() - self.starting_time).total_seconds(),3)}s",
                font = ('Comic Sans MS', 18,'bold')).pack(expand=True)
            self.geometry(f'{58 * 5}x70')
            self.title('You Win!')

if __name__ == "__main__":
    App = MenuWin()
    App.mainloop()
