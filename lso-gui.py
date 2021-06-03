import sqlite3
import swap_handler
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import Toplevel, messagebox as msg_box


class db:
    def __init__(self):
        self.connection = sqlite3.connect('settings.db')

        self.create_table()
        self.get_font()
        self.get_lang()

    def refresh_table(self):
        self.connection.execute("DROP TABLE SETTINGS")
        self.create_table()

    def create_table(self):
        try:
            self.connection.execute("""CREATE TABLE SETTINGS(
                ID INTEGER PRIMARY KEY,
                LANGUAGE TEXT,
                FONT TEXT)""")

            self.connection.execute(
                "INSERT INTO SETTINGS (LANGUAGE, FONT) VALUES(?,?)", ('en', 'Bahnschrift,18'))
            self.connection.commit()
        except Exception as e:
            pass

    def get_font(self):
        self.font = list(self.connection.execute(
            "SELECT FONT FROM SETTINGS"))[0][0].split(',')
        self.font_n, self.font_s = self.font[0], self.font[1]

    def get_lang(self):
        self.language = list(self.connection.execute(
            "SELECT LANGUAGE FROM SETTINGS"))[0][0]


class ui:
    def __init__(self):
        self.db = db()
        self.reboot()

    def reboot(self):
        pady = 15
        self.window = tk.Tk()
        if self.db.language == "en":
            self.window.title('Swap Area Handler')
        else:
            self.window.title('Swap Alan Kontrolcüsü')

        self.style = ttk.Style()
        self.window.option_add('*Font', self.db.font)
        self.style.configure('TNotebook.Tab', font=(self.db.font_n, 14))

        self.tabs = ttk.Notebook(self.window)
        self.main_tab = ttk.Frame(self.tabs)
        self.settings_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.main_tab, text='Home')
        self.tabs.add(self.settings_tab, text='Dil/Language')

        self.setting_options = tk.Frame(self.settings_tab)

        if self.db.language == "en":
            tk.Button(self.main_tab, text='Create Swap Area',
                      command=self.add_swap_toplevel).pack(padx=100, pady=pady + 30)
            tk.Button(self.main_tab, text='Delete Swap Area',
                      command=self.delete_swap).pack(padx=100, pady=10)

            # ---------------------
            tk.Label(self.setting_options, text='Language: ').grid(
                row=0, column=0, padx=45, pady=pady)

            font_look_text, language_text = "Font preview:", "Language"

        else:
            tk.Button(self.main_tab, text='Swap Alanı Yarat',
                      command=self.add_swap_toplevel).pack(padx=100, pady=20, )
            tk.Button(self.main_tab, text='Swap Alanı Sil',
                      command=self.delete_swap).pack(padx=100, pady=10)

            # ---------------------
            tk.Label(self.setting_options, text='Dil').grid(
                row=0, column=0, padx=45, pady=pady)

            font_look_text = "Font önizlemesi:"

        self.situation_info = tk.Label(self.main_tab, text="")
        self.situation_info.pack(pady=pady)

        self.language_var = tk.StringVar(
            value={'en': 'English', 'tr': 'Türkçe'}.get(self.db.language))

        self.language_option_menu = tk.OptionMenu(
            self.setting_options, self.language_var, *['English', 'Türkçe'])
        self.language_option_menu.grid(row=0, column=1)

        # ---------------------
        tk.Label(self.setting_options, text='Font: ').grid(
            row=1, column=0, pady=pady)

        self.font_name_var = tk.StringVar(value=self.db.font_n)

        self.font_name_option_menu = tk.OptionMenu(
            self.setting_options, self.font_name_var, *['Bahnschrift', 'Arial', 'Comic Sans', 'Calibri', 'Cambria'], command=self.change_font_preview)
        self.font_name_option_menu.grid(row=1, column=1)

        # ---------------------
        tk.Label(self.setting_options, text='Size: ').grid(
            row=2, column=0, padx=45, pady=15)

        self.font_size_var = tk.StringVar(value=self.db.font_s)

        self.font_size_option_menu = tk.OptionMenu(
            self.setting_options, self.font_size_var, *[font_size for font_size in range(10, 20)], command=self.change_font_preview)

        self.font_size_option_menu['menu'].config(
            font=(self.db.font_n, 16))

        self.font_size_option_menu.grid(row=2, column=1)
        # ---------------------
        tk.Label(self.setting_options, text='Font preview:').grid(
            row=3, column=0)
        self.font_preview = tk.Label(self.setting_options,
                                     textvariable=self.font_name_var, font=self.db.font)
        self.font_preview.grid(row=3, column=1)

        self.setting_options.pack()
        tk.Button(self.settings_tab, text='Ok',
                  command=self.apply_settings).pack(pady=15)

        self.tabs.pack(expand=1, fill="both")

    def change_font_preview(self, event):
        self.font_preview.config(text=self.font_name_var.get())
        self.font_preview.config(
            font=(self.font_name_var.get(), self.font_size_var.get()))

    def apply_settings(self):
        languages = {
            'English': 'en',
            'Türkçe': 'tr',
        }
        self.db.connection.execute(
            f"UPDATE SETTINGS SET LANGUAGE='{languages.get( self.language_var.get() )}' WHERE ID=1")
        self.db.connection.execute(
            f"UPDATE SETTINGS SET FONT='{','.join( [self.font_name_var.get(), self.font_size_var.get()])}' WHERE ID=1")

        self.db.connection.commit()
        self.db.get_font()
        self.db.get_lang()

        self.window.destroy()
        self.reboot()

    def delete_swap(self):
        if not swap_handler.has_swap():
            if self.db.language == "en":
                msg_box.showerror(
                    title='Error', message='Swap area already doesn\'t exist!.')
            else:
                msg_box.showerror(
                    title='Hata', message='Swap alanı zaten bulunmuyor!')
            return None

        if swap_handler.delete_swap() == 'ERROR':
            if self.db.language == "en":
                msg_box.showerror(
                    title='Error', message='There was an error while deleting swap are.')
            else:
                msg_box.showerror(
                    title='Hata', message='Swap alanı silinirken bir hata oluştu.')
        else:
            if self.db.language == "en":
                msg_box.showinfo(
                    title='Error', message='Succesfully deleted swap area.')
                self.situation_info.config(text='Situation: no swap area')
            else:
                msg_box.showinfo(
                    title='Hata', message='Swap alanı başarıyla silindi!')
                self.situation_info.config(text='Situation: swap alanı yok')


    def add_swap_toplevel(self):
        if swap_handler.has_swap():
            if self.db.language == "en":
                msg_box.showerror(
                    title='Error', message='Swap area is already created!')
            else:
                msg_box.showerror(
                    title='Hata', message='Zaten swap alanı bulunmakta!')
            return None


        self.toplevel = tk.Toplevel()
        self.toplevel.grab_set()
        if self.db.language == "en":
            self.toplevel.title('Enter Size To Create Swap Area')
            tk.Label(self.toplevel, text='Enter Size To Create Swap Area (In format of GB)').pack(
                pady=15)
        else:
            self.toplevel.title('Swap Alanı Için Boyut Girin.')
            tk.Label(self.toplevel, text='Swap Alanı Için Boyut Girin (GB olarak)').pack(
                pady=15)

        self.add_swap_entry = tk.Entry(self.toplevel)
        self.add_swap_entry.pack(pady=15)

        tk.Button(self.toplevel, text='Ok', command=self.add_swap).pack(pady=15)

        self.toplevel.mainloop()

    def add_swap(self):
        try:
            size = int(self.add_swap_entry.get()) * 1024
        except:
            if self.db.language == "en":
                msg_box.showerror(
                    title='Error', message='Please enter a valid number.')
            else:
                msg_box.showerror(
                    title='Hata', message='Lütfen geçerli bir sayı girin.')
            return None

        if swap_handler.add_swap(size) == 'ERROR':
            if self.db.language == "en":
                msg_box.showerror(
                    title='Error', message='There was an error while adding swap area.')
            else:
                msg_box.showerror(
                    title='Hata', message='Swap alanı oluşturulurken bir sorun oluştu.')
        else:
            if self.db.language == "en":
                self.situation_info.config(text='Situation: swap area active')
            else:
                self.situation_info.config(text='Durum: swap alanı aktif')
            self.toplevel.destroy()

ui = ui()
ui.window.mainloop()