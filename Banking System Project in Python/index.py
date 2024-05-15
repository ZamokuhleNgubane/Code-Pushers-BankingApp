import tkinter as tk
from time import gmtime, strftime
from tkinter import filedialog
from tkinter import messagebox


def is_number(s):
    try:
        float(s)
        return 1
    except ValueError:
        return 0


def check_acc_nmb(num):
    try:
        fpin = open(num + ".txt", 'r')
    except FileNotFoundError:
        messagebox.showinfo("Error", "Invalid Credentials!\nTry Again!")
        return 0
    fpin.close()
    return


def home_return(master):
    master.destroy()
    Main_Menu()


def write(master, name, oc, pin):
    if ((is_number(name)) or (is_number(oc) == 0) or (is_number(pin) == 0) or name == ""):
        messagebox.showinfo("Error", "Invalid Credentials\nPlease try again.")
        master.destroy()
        return

    f1 = open("Accnt_Record.txt", 'r')
    accnt_no = int(f1.readline())
    accnt_no += 1
    f1.close()

    f1 = open("Accnt_Record.txt", 'w')
    f1.write(str(accnt_no))
    f1.close()

    fdet = open(str(accnt_no) + ".txt", "w")
    fdet.write(pin + "\n")
    fdet.write(oc + "\n")
    fdet.write(str(accnt_no) + "\n")
    fdet.write(name + "\n")
    fdet.close()

    frec = open(str(accnt_no) + "-rec.txt", 'w')
    frec.write("Date                             Credit      Debit     Balance\n")
    frec.write(str(strftime("[%Y-%m-%d] [%H:%M:%S]  ", gmtime())) + "     " + oc + "              " + oc + "\n")
    frec.close()

    messagebox.showinfo("Details", "Your Account Number is: " + str(accnt_no))
    master.destroy()
    return


def crdt_write(master, amt, accnt, name):
    if (is_number(amt) == 0):
        messagebox.showinfo("Error", "Invalid Credentials\nPlease try again.")
        master.destroy()
        return

    fdet = open(accnt + ".txt", 'r')
    pin = fdet.readline()
    camt = int(fdet.readline())
    fdet.close()
    amti = int(amt)
    cb = amti + camt
    fdet = open(accnt + ".txt", 'w')
    fdet.write(pin)
    fdet.write(str(cb) + "\n")
    fdet.write(accnt + "\n")
    fdet.write(name + "\n")
    fdet.close()
    frec = open(str(accnt) + "-rec.txt", 'a+')
    frec.write(
        str(strftime("[%Y-%m-%d] [%H:%M:%S]  ", gmtime())) + "     " + str(amti) + "              " + str(cb) + "\n")
    frec.close()
    messagebox.showinfo("Operation Successfull!!", "Amount Deposited Successfully!!")
    master.destroy()
    return


def debit_write(master, amt, accnt, name):
    if (is_number(amt) == 0):
        messagebox.showinfo("Error", "Invalid Credentials\nPlease try again.")
        master.destroy()
        return

    fdet = open(accnt + ".txt", 'r')
    pin = fdet.readline()
    camt = int(fdet.readline())
    fdet.close()
    if (int(amt) > camt):
        messagebox.showinfo("Error!!", "You dont have that amount left in your account\nPlease try again.")
    else:
        amti = int(amt)
        cb = camt - amti
        fdet = open(accnt + ".txt", 'w')
        fdet.write(pin)
        fdet.write(str(cb) + "\n")
        fdet.write(accnt + "\n")
        fdet.write(name + "\n")
        fdet.close()
        frec = open(str(accnt) + "-rec.txt", 'a+')
        frec.write(str(strftime("[%Y-%m-%d] [%H:%M:%S]  ", gmtime())) + "     " + "              " + str(
            amti) + "              " + str(cb) + "\n")
        frec.close()
        messagebox.showinfo("Operation Successfull!!", "Amount Debited Successfully!!")
        master.destroy()
        return


def Cr_Amt(accnt, name):
    creditwn = tk.Tk()
    creditwn.geometry("600x300")
    creditwn.title("Deposit Amount")
    creditwn.configure(bg="#29c5f6")
    fr1 = tk.Frame(creditwn, bg="black")
    l_title = tk.Message(creditwn, text="TINKA BANK", relief="raised", width=2000, padx=600, pady=0, fg="white",
                         bg="black", justify="center", anchor="center")
    l_title.config(font=("Courier", "50", "bold"))
    l_title.pack(side="top",pady=(5,10))
    l1 = tk.Label(creditwn, relief="raised", text="Enter Amount to be Deposited: ")
    e1 = tk.Entry(creditwn, relief="raised")
    l1.pack(side="top",pady=(5,10))
    e1.pack(side="top", pady=(0,10))
    b = tk.Button(creditwn, text="Credit", relief="raised", command=lambda: crdt_write(creditwn, e1.get(), accnt, name))
    b.pack(side="top",pady=(5,5))
    creditwn.bind("<Return>", lambda x: crdt_write(creditwn, e1.get(), accnt, name))


def De_Amt(accnt, name):
    debitwn = tk.Tk()
    debitwn.geometry("600x300")
    debitwn.title("Debit Amount")
    debitwn.configure(bg="#29c5f6")
    fr1 = tk.Frame(debitwn, bg="#29c5f6")
    l_title = tk.Message(debitwn, text="TINKA BANK", relief="raised", width=2000, padx=600, pady=0, fg="white",
                         bg="black", justify="center", anchor="center")
    l_title.config(font=("Courier", "50", "bold"))
    l_title.pack(side="top",pady=(5,10))
    l1 = tk.Label(debitwn, relief="raised", text="Enter Amount to be Withdrawn: ")
    e1 = tk.Entry(debitwn, relief="raised")
    l1.pack(side="top",pady=(5,10 ))
    e1.pack(side="top",pady=(0,10))
    b = tk.Button(debitwn, text="Debit", relief="raised", command=lambda: debit_write(debitwn, e1.get(), accnt, name))
    b.pack(side="top",pady=(5,5))
    debitwn.bind("<Return>", lambda x: debit_write(debitwn, e1.get(), accnt, name))


def disp_bal(accnt):
    fdet = open(accnt + ".txt", 'r')
    fdet.readline()
    bal = fdet.readline()
    fdet.close()
    messagebox.showinfo("Balance", bal)

def disp_tr_hist(accnt):
    def download_history():
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            try:
                with open(accnt + "-rec.txt", 'r') as frec:
                    content = frec.read()
                with open(file_path, 'w') as fsave:
                    fsave.write(content)
                print("Transaction history saved to:", file_path)
            except FileNotFoundError:
                print("No transaction history found for account:", accnt)

    disp_wn = tk.Tk()
    disp_wn.geometry("900x600")
    disp_wn.title("Transaction History")
    disp_wn.configure(bg="#29c5f6")

    l_title = tk.Message(disp_wn, text="TINKA BANK", relief="raised", width=2000, padx=600, pady=0, fg="white",
                         bg="black", justify="center", anchor="center")
    l_title.config(font=("Courier", "50", "bold"))
    l_title.pack(side="top", pady=(10, 20))  # Add vertical padding around the title

    l1 = tk.Message(disp_wn, text="Your Transaction History:", padx=100, pady=20, width=1000, bg="black", fg="white",
                    relief="raised")
    l1.pack(side="top", pady=(10, 20))  # Add vertical padding around the heading

    fr2 = tk.Frame(disp_wn)
    fr2.pack(side="top", padx=10, pady=10)

    # Create a Text widget with a scrollbar
    text_frame = tk.Frame(disp_wn)
    text_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)

    scrollbar = tk.Scrollbar(text_frame)
    scrollbar.pack(side="right", fill="y")

    text = tk.Text(text_frame, wrap="none", yscrollcommand=scrollbar.set, font=("Courier", 12), relief="raised", bg="white")
    text.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=text.yview)

    try:
        with open(accnt + "-rec.txt", 'r') as frec:
            for line in frec:
                text.insert(tk.END, line)
    except FileNotFoundError:
        text.insert(tk.END, "No transaction history found for account: " + accnt)

    text.config(state=tk.DISABLED)  # Make the text widget read-only

    # Add the Download button
    b_download = tk.Button(disp_wn, text="Download Transaction History", relief="raised", command=download_history)
    b_download.pack(side="bottom", pady=(10, 10))  # Add vertical padding around the button

    b_quit = tk.Button(disp_wn, text="Quit", relief="raised", command=disp_wn.destroy)
    b_quit.pack(side="bottom", pady=(10, 20))  # Add vertical padding around the button

# Assuming a test account record file for demonstration
def create_test_record():
    with open("12345-rec.txt", "w") as file:
        file.write("Date       | Transaction | Amount\n")
        file.write("2023-05-01 | Deposit     | 1000\n")
        file.write("2023-05-02 | Withdrawal  | 500\n")

create_test_record()
disp_tr_hist("12345")
tk.mainloop()


def logged_in_menu(accnt, name):
    rootwn = tk.Tk()
    rootwn.geometry("1600x500")
    rootwn.title("TINKA BANK-" + name)
    rootwn.configure(background='#29c5f6')
    fr1 = tk.Frame(rootwn)
    fr1.pack(side="top")
    l_title = tk.Message(rootwn, text="TINKA BANK", relief="raised", width=2000, padx=600, pady=0, fg="white",
                         bg="black", justify="center", anchor="center")
    l_title.config(font=("Courier", "50", "bold"))
    l_title.pack(side="top")
    label = tk.Label(text="Logged in as: " + name, relief="raised", bg="black", fg="white", anchor="center",
                     justify="center")
    label.pack(side="top")
    img2 = tk.PhotoImage(file="credit.gif.png")
    myimg2 = img2.subsample(2, 2)
    img3 = tk.PhotoImage(file="debit.gif.png")
    myimg3 = img3.subsample(2, 2)
    img4 = tk.PhotoImage(file="balance1.gif.png")
    myimg4 = img4.subsample(2, 2)
    img5 = tk.PhotoImage(file="transaction.gif.png")
    myimg5 = img5.subsample(2, 2)
    b2 = tk.Button(image=myimg2, command=lambda: Cr_Amt(accnt, name))
    b2.image = myimg2
    b3 = tk.Button(image=myimg3, command=lambda: De_Amt(accnt, name))
    b3.image = myimg3
    b4 = tk.Button(image=myimg4, command=lambda: disp_bal(accnt))
    b4.image = myimg4
    b5 = tk.Button(image=myimg5, command=lambda: disp_tr_hist(accnt))
    b5.image = myimg5

    img6 = tk.PhotoImage(file="logout.gif.png")
    myimg6 = img6.subsample(2, 2)
    b6 = tk.Button(image=myimg6, relief="raised", command=lambda: logout(rootwn))
    b6.image = myimg6

    b2.place(x=100, y=150)
    b3.place(x=100, y=220)
    b4.place(x=900, y=150)
    b5.place(x=900, y=220)
    b6.place(x=500, y=400)


def logout(master):
    messagebox.showinfo("Logged Out", "You Have Been Successfully Logged Out!!")
    master.destroy()
    Main_Menu()


def check_log_in(master, name, acc_num, pin):
    if (check_acc_nmb(acc_num) == 0):
        master.destroy()
        Main_Menu()
        return

    if ((is_number(name)) or (is_number(pin) == 0)):
        messagebox.showinfo("Error", "Invalid Credentials\nPlease try again.")
        master.destroy()
        Main_Menu()
    else:
        master.destroy()
        logged_in_menu(acc_num, name)


def log_in(master):
    master.destroy()
    loginwn = tk.Tk()
    loginwn.geometry("600x300")
    loginwn.title("Log in")
    loginwn.configure(bg="#29c5f6")
    fr1 = tk.Frame(loginwn, bg="white")
    l_title = tk.Message(loginwn, text="TINKA BANK", relief="raised", width=2000, padx=600, pady=0, fg="white",
                         bg="black", justify="center", anchor="center")
    l_title.config(font=("Courier", "50", "bold"))
    l_title.pack(side="top", pady=(5,10))
    l1 = tk.Label(loginwn, text="Enter Name:", relief="raised")
    l1.pack(side="top",pady=(8,4))
    e1 = tk.Entry(loginwn)
    e1.pack(side="top" ,pady=(0,5))
    l2 = tk.Label(loginwn, text="Enter account number:", relief="raised")
    l2.pack(side="top" , pady=(8,4))
    e2 = tk.Entry(loginwn)
    e2.pack(side="top",pady=(0,5))
    l3 = tk.Label(loginwn, text="Enter your PIN:", relief="raised")
    l3.pack(side="top", pady=(8,4))
    e3 = tk.Entry(loginwn, show="*")
    e3.pack(side="top", pady=(0,10))
    b = tk.Button(loginwn, text="Submit",
                  command=lambda: check_log_in(loginwn, e1.get().strip(), e2.get().strip(), e3.get().strip()))
    b.pack(side="top", pady=(5,5))
    b1 = tk.Button(text="HOME", relief="raised", bg="black", fg="white", command=lambda: home_return(loginwn))
    b1.pack(side="top",pady=(8,8) )
    loginwn.bind("<Return>", lambda x: check_log_in(loginwn, e1.get().strip(), e2.get().strip(), e3.get().strip()))


def Create():
    crwn = tk.Tk()
    crwn.geometry("600x300")
    crwn.title("Create Account")
    crwn.configure(bg="#29c5f6")
    fr1 = tk.Frame(crwn, bg="white")
    l_title = tk.Message(crwn, text="TINKA BANK", relief="raised", width=2000, padx=600, pady=0, fg="white", bg="black",
                         justify="center", anchor="center")
    l_title.config(font=("Courier", "50", "bold"))
    l_title.pack(side="top",pady=(10,20))
    l1 = tk.Label(crwn, text="Enter Name:", relief="raised")
    l1.pack(side="top", pady=(8,4))
    e1 = tk.Entry(crwn)
    e1.pack(side="top" ,pady=(0,5))
    l2 = tk.Label(crwn, text="Enter Opening Deposit:", relief="raised")
    l2.pack(side="top",pady=(8,4))
    e2 = tk.Entry(crwn)
    e2.pack(side="top", pady=(0,5))
    l3 = tk.Label(crwn, text="Enter Desired PIN:", relief="raised")
    l3.pack(side="top",pady=(8,4))
    e3 = tk.Entry(crwn, show="*")
    e3.pack(side="top",pady=(8,8))
    b = tk.Button(crwn, text="Submit",
                  command=lambda: write(crwn, e1.get().strip(), e2.get().strip(), e3.get().strip()))
    b.pack(side="top")
    crwn.bind("<Return>", lambda x: write(crwn, e1.get().strip(), e2.get().strip(), e3.get().strip()))
    return


def Main_Menu():
    rootwn = tk.Tk()
    rootwn.title("Tinka Bank")
    rootwn.configure(background='#29c5f6')

    # Title label
    l_title = tk.Label(rootwn, text="TINKA BANK", font=("Courier", 50, "bold"), fg="white", bg="black")
    l_title.pack(pady=20)

    # Frame for buttons
    fr_buttons = tk.Frame(rootwn, bg="#29c5f6")
    fr_buttons.pack(pady=20)

    # Buttons
    imgc = tk.PhotoImage(file="new.gif.png").subsample(2, 2)
    imglog = tk.PhotoImage(file="login.gif.png").subsample(2, 2)
    b1 = tk.Button(fr_buttons, image=imgc, command=Create)
    b1.image = imgc
    b2 = tk.Button(fr_buttons, image=imglog, command=lambda: log_in(rootwn))
    b2.image = imglog

    b1.grid(row=0, column=0, padx=20)
    b2.grid(row=0, column=1, padx=20)

    rootwn.mainloop()


Main_Menu()
