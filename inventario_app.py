from tkinter import *
from tkinter import ttk, messagebox
import psycopg2
import smtplib
from email.message import EmailMessage

# connect to the db
con = psycopg2.connect(
    host="127.0.0.1",
    database="produtos",
    user="postgres",
    password="postgres",
    port=3307,
)

# cursor
cur = con.cursor()

# GUI window
root = Tk()
root.geometry('960x600')

# Setting the canvas
my_Canvas = Canvas(root, width=960, height=600)
my_Canvas.pack(side=LEFT, fill=BOTH, expand=1)

# Creating the Frame inside of the canvas
tree_frame = Frame(my_Canvas, width=710, height=290, background="bisque")
tree_frame.place(x=120, y=300)

# Styling the tree
style = ttk.Style()
style.configure("Treeview",
                background="silver",
                foreground="black",
                rowheight=25,
                fieldbackground="silver")
style.map('Treeview',
          background=[('selected', 'green')])

# Adding the tree
tree = ttk.Treeview(tree_frame)

# Defining the columns
tree['columns'] = ("ID", "Nome", "Quantidade", "Valor unitario")

# Formating the columns
tree.column("#0", width=0, stretch=NO)
tree.column("ID", anchor=CENTER, width=180, minwidth=25)
tree.column("Nome", anchor=CENTER, width=180, minwidth=25)
tree.column("Quantidade", anchor=CENTER, width=176, minwidth=25)
tree.column("Valor unitario", anchor=CENTER, width=170, minwidth=25)

# Create Headings
tree.heading("#0", text="", anchor=CENTER)
tree.heading("ID", text="ID", anchor=CENTER)
tree.heading("Nome", text="Nome do Produto", anchor=CENTER)
tree.heading("Quantidade", text="Quantidade em estoque", anchor=CENTER)
tree.heading("Valor unitario", text="Valor Unitário", anchor=CENTER)

cur.execute('SELECT * FROM produto')
rows = cur.fetchall()

# Create striped row tags
tree.tag_configure('oddrow', background="white")
tree.tag_configure('evenrow', background="#4b0082")

# Adding the data
tree.place(x=0,y=0, height=290)
count = 0
for r in rows:
    if count % 2 == 0:
        tree.insert(parent='', index='end',iid=count, text='Parent', values=(r[0], r[1], r[2], r[3]), tags=('evenrow',))
    else:
        tree.insert(parent='', index='end', iid=count, text='Parent', values=(r[0], r[1], r[2], r[3]), tags=('oddrow',))
    count += 1

# setting the labels and the buttons
my_Canvas.create_text(160, 20, text='Digite o nome do produto que deseja add no inventário')
nome_produto = Entry(my_Canvas, width=25, borderwidth=2)
my_Canvas.create_window(410, 20, window=nome_produto, height=25, width=180)

my_Canvas.create_text(124, 60, text='Quantidade que deseja add no inventário')
quantidade_produto = Entry(my_Canvas, width=25, borderwidth=2)
my_Canvas.create_window(410, 60, window=quantidade_produto, height=25, width=180)

my_Canvas.create_text(109, 100, text='Valor que deseja add no inventário')
valor_produto = Entry(my_Canvas, width=25, borderwidth=2)
my_Canvas.create_window(410, 100, window=valor_produto, height=25, width=180)

my_Canvas.create_text(630, 65, text='Nome do produto no qual deseja atualizar')
label_update_nome_entry = Entry(my_Canvas, width=25, borderwidth=2)
my_Canvas.create_window(850, 65, window=label_update_nome_entry, height=25, width=180)

my_Canvas.create_text(670, 20, text='Caso queira atualizar algum produto no estoque,')
my_Canvas.create_text(670, 35, text=' selecione abaixo o que você deseja atualizar:')

# Setting the Radio buttons
option_selected = IntVar()
option_1 = Radiobutton(my_Canvas, text='Quantidade do Produto', variable=option_selected, value=1,
                       command=lambda: clicked(option_selected.get())).place(x=600, y=97)
option_2 = Radiobutton(my_Canvas, text='Valor do Produto', variable=option_selected, value=2,
                       command=lambda: clicked(option_selected.get())).place(x=600, y=117)
option_3 = Radiobutton(my_Canvas, text='Quantidade e Valor do Produto', variable=option_selected, value=3,
                       command=lambda: clicked(option_selected.get())).place(x=600, y=137)


# Getting the value of the Dropdown menus
def clicked(value):
    global label_update_quantidade_entry, label_update_valor_entry
    if value == 1:
        my_Canvas.create_text(642, 210, text='Quantidade do Produto:')
        label_update_quantidade_entry = Entry(my_Canvas, width=25, borderwidth=2)
        my_Canvas.create_window(830, 210, window=label_update_quantidade_entry, height=25, width=180)

    if value == 2:
        my_Canvas.create_text(642, 210, text='Valor do Produto:')
        label_update_valor_entry = Entry(my_Canvas, width=25, borderwidth=2)
        my_Canvas.create_window(830, 210, window=label_update_valor_entry, height=25, width=180)

    if value == 3:
        my_Canvas.create_text(642, 185, text='Quantidade do Produto:')
        label_update_quantidade_entry = Entry(my_Canvas, width=25, borderwidth=2)
        my_Canvas.create_window(830, 185, window=label_update_quantidade_entry, height=25, width=180)

        my_Canvas.create_text(660, 220, text='Valor do Produto:')
        label_update_valor_entry = Entry(my_Canvas, width=25, borderwidth=2)
        my_Canvas.create_window(830, 220, window=label_update_valor_entry, height=25, width=180)

    # Update button
    update = Button(my_Canvas, text='atualizar', command=lambda: update_func(option_selected.get()))
    update.place(x=820, y=260)


# Getting the value of the inserted options
def confirm_btn():
    global nome, qt, valor, con, cur
    nome = nome_produto.get()
    print(nome)
    qt = quantidade_produto.get()
    print(qt)
    valor = valor_produto.get()
    print(valor)

    # execute query
    cur.execute(
        f"INSERT INTO produto (nome_produto, quantidade_produto, valor_produto) VALUES ('{nome}', {qt}, {valor})")

    cur.execute('SELECT * FROM produto')

    rows = cur.fetchall()
    for r in rows:
        print(f'id = {r[0]}, nome produto = {r[1]}, quantidade = {r[2]}, valor = {r[3]}')

    # commiting the data
    con.commit()


def update_func(value):
    global cur, label_update_quantidade_entry, label_update_valor_entry, label_update_nome_entry, con
    nome = label_update_nome_entry.get()
    print(nome)
    if value == 1:
        quantidade = label_update_quantidade_entry.get()
        print(quantidade)

        cur.execute(
            f"UPDATE produto SET quantidade_produto = {quantidade} WHERE nome_produto = '{nome}';")
    if value == 2:
        valor = label_update_valor_entry.get()

        cur.execute(
            f"UPDATE produto SET valor_produto = {valor} WHERE nome_produto = '{nome}';")

    if value == 3:
        quantidade = label_update_quantidade_entry.get()
        valor = label_update_valor_entry.get()

        cur.execute(
            f"UPDATE produto SET quantidade_produto = {quantidade} WHERE nome_produto = '{nome}';")

        cur.execute(
            f"UPDATE produto SET valor_produto = {valor} WHERE nome_produto = '{nome}';")

    # commiting the update
    con.commit()


def check_func():
    global cur
    situation = False
    produtos_inventario = []
    cur.execute('SELECT * FROM produto')
    rows = cur.fetchall()
    for r in rows:
        print(r)
        if r[2] == 0:
            print(f'o valor contido em r {r[2]}')
            situation = True
            produtos_inventario.append(r[1])
    msg = EmailMessage()
    msg['Subject'] = "Reposição de estoque"
    msg['From'] = 'felippoBeifong@gmail.com'
    msg['To'] = 'coelho.luizfelippo@gmail.com'
    if situation:
        msg.set_content(f"Produto necessário a reposição:{produtos_inventario[0]}")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('felippoBeifong@gmail.com', 'beifongtophlinsuyin')
        smtp.send_message(msg)

    if situation:
        messagebox.showinfo('check message',
                            f'O produto {produtos_inventario[0]} está em falta! Já foi enviado e-mail ao fornecedor.')
    else:
        messagebox.showinfo('check message', 'Sem produtos necessário a ser feito reposição.')


def close_btn():
    # close the cursor
    cur.close()
    # close the connection
    con.close()
    root.destroy()


# Checking the inventory Button
check = Button(my_Canvas, text='check', command=check_func)
check.place(x=720, y=260)

# Confirm button
confirm = Button(my_Canvas, text='confirmar', command=confirm_btn)
confirm.place(x=445, y=140)

# Close button
close = Button(my_Canvas, text='fechar programa', command=close_btn)
close.place(x=40, y=220)

mainloop()
