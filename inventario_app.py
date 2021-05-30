from tkinter import *
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
import psycopg2
import smtplib
from email.message import EmailMessage

# connect to the db
con = psycopg2.connect(
    host="127.0.0.1",
    database="produtos",
    user="user",
    password="password",
    port=3307,
)

# cursor
cur = con.cursor()

# GUI window
root = Tk()
root.geometry('825x450')

# Setting the canvas
my_Canvas = Canvas(root, width=825, height=450)
my_Canvas.pack(side=LEFT, fill=BOTH, expand=1)

# Creating the Frame inside of the canvas
tree_frame = Frame(my_Canvas, width=469, height=190, background="bisque")
tree_frame.place(x=125, y=250)

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
tree.place(x=0, y=0, height=200)

# Defining the columns
tree['columns'] = ("ID", "Nome", "Quantidade", "Valor unitario")

# Formating the columns
tree.column("#0", width=0, stretch=NO)
tree.column("ID", anchor=CENTER, width=70, minwidth=25)
tree.column("Nome", anchor=CENTER, width=120, minwidth=25)
tree.column("Quantidade", anchor=CENTER, width=156, minwidth=25)
tree.column("Valor unitario", anchor=CENTER, width=120, minwidth=25)

# Create Headings
tree.heading("#0", text="", anchor=CENTER)
tree.heading("ID", text="ID", anchor=CENTER)
tree.heading("Nome", text="Nome do Produto", anchor=CENTER)
tree.heading("Quantidade", text="Quantidade em estoque", anchor=CENTER)
tree.heading("Valor unitario", text="Valor Unitário", anchor=CENTER)

cur.execute('SELECT * FROM produto ORDER BY ID')
rows = cur.fetchall()

# Create striped row tags
tree.tag_configure('oddrow', background="white")
tree.tag_configure('evenrow', background="#4b0082")

# Adicionando os dados
count = 0
for r in rows:
    if count % 2 == 0:
        tree.insert(parent='', index='end', iid=count, text='Parent', values=(r[0], r[1], r[2], r[3]),
                    tags=('evenrow',))
    else:
        tree.insert(parent='', index='end', iid=count, text='Parent', values=(r[0], r[1], r[2], r[3]), tags=('oddrow',))
    count += 1

# Definindo as labels e os botões
my_Canvas.create_text(160, 20, text='Digite o nome do produto que deseja adicionar no estoque:')
nome_produto = Entry(my_Canvas, width=25, borderwidth=2)
my_Canvas.create_window(410, 20, window=nome_produto, height=25, width=180)

my_Canvas.create_text(124, 60, text='Quantidade que deseja adicionar no estoque:')
quantidade_produto = Entry(my_Canvas, width=25, borderwidth=2)
my_Canvas.create_window(410, 60, window=quantidade_produto, height=25, width=180)

my_Canvas.create_text(109, 100, text='Valor que deseja adicionar no estoque:')
valor_produto = Entry(my_Canvas, width=25, borderwidth=2)
my_Canvas.create_window(410, 100, window=valor_produto, height=25, width=180)

my_Canvas.create_text(150, 160, text='Caso queira atualizar algum produto no estoque,')
my_Canvas.create_text(150, 173, text=' selecione abaixo o que você deseja atualizar:')

my_Canvas.create_text(150, 205, text='Quantidade no estoque:')
update_quantidade = Entry(my_Canvas, width=25, borderwidth=2)
my_Canvas.create_window(310, 205, window=update_quantidade, height=25, width=180)

my_Canvas.create_text(450, 205, text='Valor Atual:')
update_valor = Entry(my_Canvas, width=25, borderwidth=2)
my_Canvas.create_window(580, 205, window=update_valor, height=25, width=180)

my_Canvas.create_text(570, 20, text='e-mail do fornecedor:')
fornecedor = Entry(my_Canvas, borderwidth=2)
my_Canvas.create_window(725, 20, window=fornecedor, height=25, width=180)


def confirm_btn():
    global nome_produto, quantidade_produto, valor_produto, con, cur
    nome = nome_produto.get()
    qt = quantidade_produto.get()
    v = valor_produto.get()
    try:
        # Executando a query
        cur.execute(
            f"INSERT INTO produto (nome_produto, quantidade_produto, valor_produto) VALUES ('{nome}', {qt}, {v})")

        nome_produto.delete(0, END)
        quantidade_produto.delete(0, END)
        valor_produto.delete(0, END)

        # comitando o dado
        con.commit()
    except:
        msg_box = messagebox.showinfo('confirm message', 'Necessário informar o produto!',
                                      icon='warning')


# Atualiza os dados selecionados pelo usuário
def update_func():
    global cur, update_valor, update_quantidade, con, tree
    try:
        # Pegando o número armazenado tree table
        selected = tree.focus()
        # Pegando os valores armazenados
        values = tree.item(selected, 'values')
        nome = values[1]
        # Pegando o input
        quantidade = update_quantidade.get()
        update_quantidade.delete(0, END)

        valor = update_valor.get()
        update_valor.delete(0, END)
        # Executando o update do dado
        cur.execute(f"UPDATE produto SET quantidade_produto = {quantidade} WHERE nome_produto = '{nome}';")

        cur.execute(f"UPDATE produto SET valor_produto = {valor} WHERE nome_produto = '{nome}';")

        # commiting the update
        con.commit()
    except:
        msg_box = messagebox.showinfo('update message', 'Necessário informar o produto!',
                                      icon='warning')


# Checar os dados na base de dados e envia e-mail ao fornecer se a quantidade de produtos for igual a 0
def check_func():
    global cur, fornecedor

    situation = False
    produtos_inventario = []
    cur.execute('SELECT * FROM produto')
    rows = cur.fetchall()
    for r in rows:
        if r[2] == 0:
            situation = True
            produtos_inventario.append(r[1])
    try:
        email = fornecedor.get()
        msg = EmailMessage()
        msg['Subject'] = "Reposição de estoque"
        msg['From'] = 'felippoBeifong@gmail.com'
        msg['To'] = f'{email}'

        if situation:
            msg.set_content(f"Produto necessário a reposição:{produtos_inventario[0]}")

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('email_test@gmail', 'password')
            smtp.send_message(msg)

        if situation:
            messagebox.showinfo('check message',
                                f'O produto {produtos_inventario[0]} está em falta! Já foi enviado e-mail ao fornecedor.',
                                icon='warning')
        else:
            messagebox.showinfo('check message', 'Sem produtos necessário a ser feito reposição.', icon='info')

    except:
        msg_box = messagebox.showinfo('check message', 'Necessário informar o e-mail antes do processo de checagem!',
                                      icon='warning')


def drop_func():
    global cur, con
    delete = False
    sel = True
    try:
        # Grab record data
        selected = tree.focus()
        # Grab record values
        values = tree.item(selected, 'values')
        id = values[0]
    except:
        msg_box = messagebox.showinfo('drop record', 'Necessário selecionar algum produto para retirar!',
                                      icon='warning')
    else:
        msg_box = messagebox.askquestion('drop record', 'Certeza que deseja deletar este dado?', icon='warning')
        if msg_box == 'yes':
            delete = True
        else:
            delete = False
        if delete:
            cur.execute(f'DELETE FROM produto WHERE id = {id};')
            con.commit()


def refresh_func():
    global tree
    for i in tree.get_children():
        tree.delete(i)
    tree = ttk.Treeview(tree_frame)
    tree.place(x=0, y=0, height=200)
    tree['columns'] = ("ID", "Nome", "Quantidade", "Valor unitario")
    tree.column("#0", width=0, stretch=NO)
    tree.column("ID", anchor=CENTER, width=70, minwidth=25)
    tree.column("Nome", anchor=CENTER, width=120, minwidth=25)
    tree.column("Quantidade", anchor=CENTER, width=156, minwidth=25)
    tree.column("Valor unitario", anchor=CENTER, width=120, minwidth=25)
    tree.heading("#0", text="", anchor=CENTER)
    tree.heading("ID", text="ID", anchor=CENTER)
    tree.heading("Nome", text="Nome do Produto", anchor=CENTER)
    tree.heading("Quantidade", text="Quantidade em estoque", anchor=CENTER)
    tree.heading("Valor unitario", text="Valor Unitário", anchor=CENTER)
    tree.tag_configure('oddrow', background="white")
    tree.tag_configure('evenrow', background="#4b0082")
    cur.execute('SELECT * FROM produto ORDER BY ID')
    rows = cur.fetchall()
    count = 0
    for r in rows:
        if count % 2 == 0:
            tree.insert(parent='', index='end', iid=count, text='Parent', values=(r[0], r[1], r[2], r[3]),
                        tags=('evenrow',))
        else:
            tree.insert(parent='', index='end', iid=count, text='Parent', values=(r[0], r[1], r[2], r[3]),
                        tags=('oddrow',))
        count += 1


# Botão de checagem de estoque
check = Button(my_Canvas, text='checar dados', command=check_func)
check.place(x=720, y=45)

# Botão de confirmação
confirm = Button(my_Canvas, text='confirmar', command=confirm_btn)
confirm.place(x=445, y=120)

# Botão de atualização
update = Button(my_Canvas, text='update', command=update_func)
update.place(x=680, y=205)

# Botão de retirada de item na base de dados
img1 = Image.open('trash.png')
img1_resized = img1.resize((20, 20), Image.ANTIALIAS)
img1 = ImageTk.PhotoImage(img1_resized)
drop = Button(my_Canvas, image=img1, command=drop_func, borderwidth=0)
drop.place(x=600, y=400)

# Refresh button
img2 = Image.open('refresh.png')
img2_resized = img2.resize((20, 20), Image.ANTIALIAS)
img2 = ImageTk.PhotoImage(img2_resized)
refresh = Button(my_Canvas, image=img2, command=refresh_func, borderwidth=0)
refresh.place(x=600, y=350)
mainloop()
