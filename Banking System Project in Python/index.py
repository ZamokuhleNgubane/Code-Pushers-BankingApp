import tkinter as tk
from time import gmtime, strftime
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import string
import random
import os


# Helper Functions
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def check_acc_nmb(num, pin):
    try:
        with open(num + ".txt", 'r') as fpin:
            stored_pin = fpin.readline().strip()
            if stored_pin != pin:
                messagebox.showinfo("Error", "Invalid Credentials!\nTry Again!")
                return False
    except FileNotFoundError:
        messagebox.showinfo("Error", "Invalid Credentials!\nTry Again!")
        return False
    return True


def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))


def write(controller, name, oc, pin):
    if not name or not is_number(oc) or len(pin) != 12:
        messagebox.showinfo("Error", "Invalid Credentials\nPlease try again.")
        return

    with open("Accnt_Record.txt", 'r') as f1:
        accnt_no = int(f1.readline().strip())
    accnt_no += 1

    with open("Accnt_Record.txt", 'w') as f1:
        f1.write(str(accnt_no))

    with open(f"{accnt_no}.txt", "w") as fdet:
        fdet.write(pin + "\n" + oc + "\n" + str(accnt_no) + "\n" + name + "\n")

    with open(f"{accnt_no}-rec.txt", 'w') as frec:
        frec.write("Date                             Credit      Debit     Balance\n")
        frec.write(f"{strftime('[%Y-%m-%d] [%H:%M:%S]  ', gmtime())}    {oc}             {oc}\n")

    messagebox.showinfo("Details", f"Your Account Number is: {accnt_no}")
    controller.show_frame("MainMenu")


def debit_write(controller, amt, accnt, name):
    if not is_number(amt):
        messagebox.showinfo("Error", "Invalid Credentials\nPlease try again.")
        return

    with open(f"{accnt}.txt", 'r') as fdet:
        pin = fdet.readline()
        camt = int(fdet.readline())

    if int(amt) > camt:
        messagebox.showinfo("Error", "You don't have that amount left in your account\nPlease try again.")
    else:
        amti = int(amt)
        cb = camt - amti
        with open(f"{accnt}.txt", 'w') as fdet:
            fdet.write(pin + str(cb) + "\n" + accnt + "\n" + name + "\n")

        with open(f"{accnt}-rec.txt", 'a+') as frec:
            frec.write(
                f"{strftime('[%Y-%m-%d] [%H:%M:%S]  ', gmtime())}     {'              '}{amti}              {cb}\n")

        messagebox.showinfo("Operation Successful", "Amount Debited Successfully!")
        controller.show_frame("LoggedInMenu", accnt, name)


def crdt_write(controller, amt, accnt, name):
    if not is_number(amt):
        messagebox.showinfo("Error", "Invalid Credentials\nPlease try again.")
        return

    with open(f"{accnt}.txt", 'r') as fdet:
        pin = fdet.readline()
        camt = int(fdet.readline())

    amti = int(amt)
    cb = amti + camt

    with open(f"{accnt}.txt", 'w') as fdet:
        fdet.write(pin + str(cb) + "\n" + accnt + "\n" + name + "\n")

    with open(f"{accnt}-rec.txt", 'a+') as frec:
        frec.write(f"{strftime('[%Y-%m-%d] [%H:%M:%S]  ', gmtime())}     {amti}              {cb}\n")

    messagebox.showinfo("Operation Successful", "Amount Deposited Successfully!")
    controller.show_frame("LoggedInMenu", accnt, name)


def disp_bal(accnt):
    with open(f"{accnt}.txt", 'r') as fdet:
        fdet.readline()
        bal = fdet.readline()
    messagebox.showinfo("Balance", bal)


def disp_tr_hist(controller, accnt):
    controller.switch_frame(TransactionHistoryFrame, accnt)


def update_clock(label):
    current_datetime = strftime('%Y-%m-%d %H:%M:%S')
    label.config(text=current_datetime)
    label.after(1000, lambda: update_clock(label))


# Frames
class BankingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.title("Tinka Bank")
        self.frames = {}
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.create_frames()
        self.show_frame("MainMenu")

    def create_frames(self):
        for F in (MainMenu, CreateAccount, LogIn, LoggedInMenu, Deposit, Withdraw, TransactionHistoryFrame):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, page_name, *args):
        frame = self.frames[page_name]
        frame.tkraise()
        if hasattr(frame, 'update_data'):
            frame.update_data(*args)

    def switch_frame(self, frame_class, *args):
        frame = frame_class(parent=self.container, controller=self)
        frame.grid(row=0, column=0, sticky="nsew")
        self.frames[frame_class.__name__] = frame
        frame.tkraise()
        if hasattr(frame, 'update_data'):
            frame.update_data(*args)


class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(background='#29c5f6')
        logo_image = tk.PhotoImage(file="918b31fa5a4b49a982796ff43e74db92 (1).png")
        logo_label = tk.Label(self, image=logo_image, bg='#29c5f6')
        logo_label.image = logo_image
        logo_label.pack(pady=10)
        fr_buttons = tk.Frame(self, bg="#29c5f6")
        fr_buttons.pack(pady=20)
        imgc = tk.PhotoImage(file="new.gif.png").subsample(2, 2)
        imglog = tk.PhotoImage(file="login.gif.png").subsample(2, 2)
        b1 = tk.Button(fr_buttons, image=imgc, command=lambda: controller.show_frame("CreateAccount"))
        b1.image = imgc
        b2 = tk.Button(fr_buttons, image=imglog, command=lambda: controller.show_frame("LogIn"))
        b2.image = imglog
        b1.grid(row=0, column=0, padx=20)
        b2.grid(row=0, column=1, padx=20)
        clock_label = tk.Label(self, font=("Courier", 20), fg="white", bg="black")
        clock_label.pack(pady=10)
        update_clock(clock_label)


class CreateAccount(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#29c5f6")
        logo_image = tk.PhotoImage(file="918b31fa5a4b49a982796ff43e74db92 (1).png")
        logo_label = tk.Label(self, image=logo_image, bg='#29c5f6')
        logo_label.image = logo_image
        logo_label.pack(pady=(5, 0))
        self.create_widgets()

    def create_widgets(self):
        l1 = tk.Label(self, text="Enter Name:", relief="raised")
        l1.pack(side="top", pady=(8, 4))
        self.e1 = tk.Entry(self)
        self.e1.pack(side="top", pady=(0, 8))
        l2 = tk.Label(self, text="Opening Credit:", relief="raised")
        l2.pack(side="top", pady=(8, 4))
        self.e2 = tk.Entry(self)
        self.e2.pack(side="top", pady=(0, 8))
        l3 = tk.Label(self, text="Pin (12-digit):", relief="raised")
        l3.pack(side="top", pady=(8, 4))
        self.e3 = tk.Entry(self, show="*")
        self.e3.pack(side="top", pady=(0, 8))
        self.show_password_var = tk.BooleanVar()
        show_password_check = tk.Checkbutton(self, text="Show Password", variable=self.show_password_var, command=self.toggle_password)
        show_password_check.pack()
        generate_password_button = tk.Button(self, text="Generate Password", command=self.generate_password)
        generate_password_button.pack(pady=10)
        create_acc_button = tk.Button(self, text="Create Account", command=self.create_account)
        create_acc_button.pack(pady=10)
        back_button = tk.Button(self, text="Back", command=lambda: self.controller.show_frame("MainMenu"))
        back_button.pack(pady=10)

    def toggle_password(self):
        if self.show_password_var.get():
            self.e3.config(show="")
        else:
            self.e3.config(show="*")

    def generate_password(self):
        password = generate_password()
        self.e3.delete(0, tk.END)
        self.e3.insert(0, password)
        self.toggle_password()

    def create_account(self):
        name = self.e1.get()
        oc = self.e2.get()
        pin = self.e3.get()
        write(self.controller, name, oc, pin)


class LogIn(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#29c5f6")
        logo_image = tk.PhotoImage(file="918b31fa5a4b49a982796ff43e74db92 (1).png")
        logo_label = tk.Label(self, image=logo_image, bg='#29c5f6')
        logo_label.image = logo_image
        logo_label.pack(pady=(5, 0))
        self.create_widgets()

    def create_widgets(self):
        l1 = tk.Label(self, text="Enter Account Number:", relief="raised")
        l1.pack(side="top", pady=(8, 4))
        self.e1 = tk.Entry(self)
        self.e1.pack(side="top", pady=(0, 8))
        l2 = tk.Label(self, text="Enter Pin:", relief="raised")
        l2.pack(side="top", pady=(8, 4))
        self.e2 = tk.Entry(self, show="*")
        self.e2.pack(side="top", pady=(0, 8))
        self.show_password_var = tk.BooleanVar()
        show_password_check = tk.Checkbutton(self, text="Show Password", variable=self.show_password_var, command=self.toggle_password)
        show_password_check.pack()
        login_button = tk.Button(self, text="Log In", command=self.login)
        login_button.pack(pady=10)
        back_button = tk.Button(self, text="Back", command=lambda: self.controller.show_frame("MainMenu"))
        back_button.pack(pady=10)

    def toggle_password(self):
        if self.show_password_var.get():
            self.e2.config(show="")
        else:
            self.e2.config(show="*")

    def login(self):
        accnt = self.e1.get()
        pin = self.e2.get()
        if check_acc_nmb(accnt, pin):
            with open(accnt + ".txt", 'r') as fdet:
                fdet.readline()
                fdet.readline()
                accnt_no = fdet.readline().strip()
                name = fdet.readline().strip()
            self.controller.show_frame("LoggedInMenu", accnt_no, name)
        else:
            messagebox.showinfo("Error", "Invalid Credentials!\nTry Again!")


class LoggedInMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#29c5f6")
        logo_image = tk.PhotoImage(file="918b31fa5a4b49a982796ff43e74db92 (1).png")
        logo_label = tk.Label(self, image=logo_image, bg='#29c5f6')
        logo_label.image = logo_image
        logo_label.pack(pady=(5, 0))
        self.create_widgets()

    def create_widgets(self):
        self.name_label = tk.Label(self, text="", font=("Helvetica", 18), bg='#29c5f6')
        self.name_label.pack(pady=20)
        self.accnt_label = tk.Label(self, text="", font=("Helvetica", 18), bg='#29c5f6')
        self.accnt_label.pack(pady=20)
        b1 = tk.Button(self, text="Balance Enquiry", command=lambda: disp_bal(self.accnt))
        b1.pack(pady=10)
        b2 = tk.Button(self, text="Deposit", command=lambda: self.controller.show_frame("Deposit", self.accnt, self.name))
        b2.pack(pady=10)
        b3 = tk.Button(self, text="Withdraw", command=lambda: self.controller.show_frame("Withdraw", self.accnt, self.name))
        b3.pack(pady=10)
        b4 = tk.Button(self, text="Transaction History", command=lambda: disp_tr_hist(self.controller, self.accnt))
        b4.pack(pady=10)
        back_button = tk.Button(self, text="Back", command=lambda: self.controller.show_frame("MainMenu"))
        back_button.pack(pady=10)

    def update_data(self, accnt, name):
        self.accnt = accnt
        self.name = name
        self.name_label.config(text=f"Welcome, {name}")
        self.accnt_label.config(text=f"Account Number: {accnt}")


class Deposit(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#29c5f6")
        logo_image = tk.PhotoImage(file="918b31fa5a4b49a982796ff43e74db92 (1).png")
        logo_label = tk.Label(self, image=logo_image, bg='#29c5f6')
        logo_label.image = logo_image
        logo_label.pack(pady=(5, 0))
        self.create_widgets()

    def create_widgets(self):
        l1 = tk.Label(self, text="Enter Amount to Deposit:", relief="raised")
        l1.pack(side="top", pady=(8, 4))
        self.e1 = tk.Entry(self)
        self.e1.pack(side="top", pady=(0, 8))
        deposit_button = tk.Button(self, text="Deposit", command=self.deposit)
        deposit_button.pack(pady=10)
        back_button = tk.Button(self, text="Back", command=lambda: self.controller.show_frame("LoggedInMenu", self.accnt, self.name))
        back_button.pack(pady=10)

    def update_data(self, accnt, name):
        self.accnt = accnt
        self.name = name

    def deposit(self):
        amt = self.e1.get()
        crdt_write(self.controller, amt, self.accnt, self.name)


class Withdraw(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#29c5f6")
        logo_image = tk.PhotoImage(file="918b31fa5a4b49a982796ff43e74db92 (1).png")
        logo_label = tk.Label(self, image=logo_image, bg='#29c5f6')
        logo_label.image = logo_image
        logo_label.pack(pady=(5, 0))
        self.create_widgets()

    def create_widgets(self):
        l1 = tk.Label(self, text="Enter Amount to Withdraw:", relief="raised")
        l1.pack(side="top", pady=(8, 4))
        self.e1 = tk.Entry(self)
        self.e1.pack(side="top", pady=(0, 8))
        withdraw_button = tk.Button(self, text="Withdraw", command=self.withdraw)
        withdraw_button.pack(pady=10)
        back_button = tk.Button(self, text="Back", command=lambda: self.controller.show_frame("LoggedInMenu", self.accnt, self.name))
        back_button.pack(pady=10)

    def update_data(self, accnt, name):
        self.accnt = accnt
        self.name = name

    def withdraw(self):
        amt = self.e1.get()
        debit_write(self.controller, amt, self.accnt, self.name)


class TransactionHistoryFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#29c5f6")
        self.accnt = None
        self.create_widgets()

    def create_widgets(self):
        logo_image = tk.PhotoImage(file="918b31fa5a4b49a982796ff43e74db92 (1).png")
        logo_label = tk.Label(self, image=logo_image, bg='#29c5f6')
        logo_label.image = logo_image
        logo_label.pack(pady=(5, 0))

        back_button = tk.Button(self, text="Back", command=self.go_back)
        back_button.pack(pady=10)

        download_button = tk.Button(self, text="Download", command=self.download_transaction_history)
        download_button.pack(pady=10)

        transaction_history_label = tk.Label(self, text="Transaction History", font=("Helvetica", 18), bg='#29c5f6')
        transaction_history_label.pack(pady=10)

        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_box = tk.Text(self, height=20, width=80, bg="white", fg="black", yscrollcommand=scrollbar.set)
        self.text_box.pack(side=tk.LEFT, fill=tk.BOTH, padx=20, pady=(0, 10))
        scrollbar.config(command=self.text_box.yview)

    def go_back(self):
        self.controller.show_frame("LoggedInMenu", self.accnt)

    def download_transaction_history(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filename:
            with open(filename, 'w') as file:
                file.write(self.text_box.get("1.0", tk.END))

    def update_data(self, accnt):
        self.accnt = accnt
        self.text_box.delete("1.0", tk.END)
        with open(f"{accnt}-rec.txt", 'r') as file:
            header = "Date                   Credit      Debit      Balance\n"
            self.text_box.insert(tk.END, header)
            self.text_box.insert(tk.END, "-" * 60 + "\n")
            for line in file:
                self.text_box.insert(tk.END, line)




if __name__ == "__main__":
    app = BankingApp()
    app.mainloop()

