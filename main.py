import tkinter as tk
import tkinter.messagebox
from enum import Enum
from chatddp import *

class ChatDdpWindow:
    def __init__(self):
        '''
        Initialise chatddp window (UI and stuff)
        '''
        self.root = tk.Tk()
        self.root.title("Chatbot Sederhana")
        self.root.geometry('500x450')
        self.color_mode = "white"

        menubar = tk.Menu(master = self.root)
        self.root.config(menu = menubar)

        # Making menu bars
        file_menu = tk.Menu(master = menubar, tearoff = 0)
        file_menu.add_command(label = 'Simpan Sesi', command = self.save_session)
        file_menu.add_command(label = 'Reset Sesi', command = self.reset_session)
        file_menu.add_separator() # Separator for dropdown menu
        file_menu.add_command(label = 'Keluar', command = self.root.quit)
        menubar.add_cascade(label = 'File', menu = file_menu)

        theme_menu = tk.Menu(master = menubar, tearoff = 0)
        theme_menu.add_command(label = 'Ubah Tema', command = self.change_theme)
        menubar.add_cascade(label = 'Tema', menu = theme_menu)

        help_menu = tk.Menu(master = menubar, tearoff = 0)
        help_menu.add_command(label = 'Tentang Aplikasi', command = self.launch_help)
        menubar.add_cascade(label = 'Tentang', menu = help_menu)

        # Make dialog frame, then put dialog screen + scroll bar in it
        frame_dialog = tk.Frame(master = self.root, bg = self.color_mode)
        dialog_scroll_bar = tk.Scrollbar(master = frame_dialog, orient = tk.VERTICAL)
        # We bind a command from scrollbar to dialog screen
        # This allows scrollbar to change yview of dialog screen 
        self.dialog_screen = tk.Text(master = frame_dialog, yscrollcommand = dialog_scroll_bar.set, bg = self.color_mode)
        # We bind dialog screen's view to scroll bar so that the scroll bar size can dynamically change on text content
        dialog_scroll_bar.config(command = self.dialog_screen.yview)
        # Use pack to make sure scrollbar takes whole dialog screen's frame
        # And manage positions of screen and scrollbar to the window
        dialog_scroll_bar.pack(side = tk.RIGHT, fill = tk.Y)
        self.dialog_screen.pack(fill = tk.BOTH, expand = True)
        frame_dialog.pack(fill = tk.BOTH, expand = True,padx = 10, pady = 10)

        # Frame that consist of all feature buttons
        frame_fitur = tk.Frame(master = self.root, bg = "light gray") # background light gray so its similar to sample
        # Bind commands to each button
        button_joke = tk.Button(master = frame_fitur, text = "Buat Lelucon", command = self.send_joke)
        button_time = tk.Button(master = frame_fitur, text = "Tanya Jam", command = self.send_clock)
        button_soal = tk.Button(master = frame_fitur, text = "Soal Matematika", command = self.send_math)
        button_tictactoe = tk.Button(master = frame_fitur, text = "Tic Tac Toe", command = self.send_tictactoe)
        # Use pack to manage positioning of all the buttons
        button_joke.pack(side = tk.LEFT, padx = 5)
        button_time.pack(side = tk.LEFT, padx = 5)
        button_soal.pack(side = tk.LEFT, padx = 5)
        button_tictactoe.pack(side = tk.LEFT, padx = 5)
        frame_fitur.pack(pady = 5)

        # Frame that consist of the entry box the user uses to send messages
        self.frame_entry = tk.Frame(master = self.root, bg = self.color_mode)
        self.entry_message = tk.Entry(master = self.frame_entry)
        self.button_send = tk.Button(master = self.frame_entry, text = "Kirim", command = self.send_msg)
        self.entry_message.pack(side = tk.LEFT, fill = tk.X, expand = True)
        self.button_send.pack(side = tk.RIGHT, expand = False)
        # Bind enter key to the entry so we can easily press enter instead of pressing the button
        self.entry_message.bind("<Return>", self.send_msg)
        self.frame_entry.pack(fill = tk.X, padx = 10, pady = 10)

        # Create new instance of ChatDdp which processes user input then outputs text back
        self.chatddp = ChatDdp()
        # Print the output of chatddp greeting to dialog screen
        self.print_chatddp_dialog(self.chatddp.greet())

        # Main loop so the event process can go on
        self.root.mainloop()
    
    def save_session(self):
        '''
        Saves chat session as text file to current folder
        '''
        # Get the whole dialog screen as a string from the widget
        whole_dialog = self.dialog_screen.get(1.0, 'end')
        # 42 is the minimum characters including greeting
        # meaning if its 42 or below, it shouldn't be saved
        if len(whole_dialog) > 42:
            # Get complete detailed local time
            current_time = time.localtime()
            year = current_time.tm_year
            month = current_time.tm_mon
            day = current_time.tm_mday
            hour = current_time.tm_hour
            minute = current_time.tm_min
            second = current_time.tm_sec
            # Use current time as the name for the file
            file_name = f"chat_session_{year:04}_{month:02}_{day:02}_{hour:02}-{minute:02}-{second:02}.txt"
            # Write whole dialog to the file
            with open(file_name, 'w') as file:
                file.write(whole_dialog)
            # Display screen to show success
            tk.messagebox.showinfo('Info', f'Sesi percakapan berhasil disimpan sebagai \'{file_name}\'.')
        else:
            # Failure to save when nothing to save
            tk.messagebox.showinfo('Info', 'Tidak ada sesi untuk disimpan.')

    def reset_session(self):
        '''
        Completely resets the session
        Instantiate new chatddp class
        '''
        self.chatddp = ChatDdp()
        self.dialog_screen.config(state = tk.NORMAL)
        self.dialog_screen.delete(1.0, 'end')
        self.entry_message.delete(0, 'end')
        self.print_chatddp_dialog(self.chatddp.greet())
        tk.messagebox.showinfo('Info', 'Sesi telah direset.')

    def change_theme(self):
        '''
        Toggles between light and dark mode
        '''
        # Text should be the opposite of bg color, set it first
        self.dialog_screen.config(fg = self.color_mode)
        self.entry_message.config(fg = self.color_mode)
        # Toggle black and white, then apply the color mode to each widget  
        self.color_mode = 'black' if self.color_mode == 'white' else 'white'
        self.root.config(bg = self.color_mode)
        self.dialog_screen.config(bg = self.color_mode)
        self.frame_entry.config(bg = self.color_mode)
        self.entry_message.config(bg = self.color_mode)

    def launch_help(self):
        '''
        Launches help message box
        '''
        tk.messagebox.showinfo('Tentang Aplikasi', "Aplikasi Chatbot ini dikembangkan oleh CHRISTOPHER-EVAN-TANUWIDJAJA dari FASILKOM UI di tahun 2024.\nSemoga aplikasi ini dapat menjadi pembelajaran yang bermanfaat, have a great day!")

    def print_chatddp_dialog(self, msg, isUser = False):
        '''
        Adds a new dialog to text widget (at the end)
        Dialog said by chatbot by default, can be changed with argument
        '''
        # Toggle between normal state and disabled state to modify our widget
        self.dialog_screen.config(state = tk.NORMAL)
        self.dialog_screen.insert(index = tk.END, chars = (("User: ") if (isUser) else ("Chatbot: ")) + msg + "\n")
        self.dialog_screen.config(state = tk.DISABLED)
    
    def send_msg(self, event = None, manmsg = None):
        '''
        Sends a message to chatbot
        Then receives message from chatbot
        Doesn't necessarily need to come from entry widget
        '''

        # Get input from entry widget if argument not used
        msg = self.entry_message.get() if manmsg == None else manmsg
        if not msg: return # Dont do anything if msg is empty
        # Clear the input from entry box
        self.entry_message.delete(0, 'end')
        # Print user input to dialog screen
        # Get chatddp output then print that afterwards
        self.print_chatddp_dialog(msg, isUser = True)
        self.print_chatddp_dialog(self.chatddp.get_answer(msg))
        self.dialog_screen.yview_moveto(1.0) # Scrolls to lowest area after each prompt :)
    
    # Various button commands which just sends manual massage to send_msg function
    def send_clock(self):
        self.send_msg(manmsg = "jam berapa")
    def send_joke(self):
        self.send_msg(manmsg = "buat lelucon")
    def send_math(self):
        self.send_msg(manmsg = "soal mat")
    def send_tictactoe(self):
        self.send_msg(manmsg = "tictactoe")

def main():
    chat_ddp_window = ChatDdpWindow()

if __name__ == "__main__":
    main()
