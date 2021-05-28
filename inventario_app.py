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


def confirm_btn():
    global nome_produto, quantidade_produto, valor_produto, con, cur
    nome = nome_produto.get()
    qt = quantidade_produto.get()
    v = valor_produto.get()

    # Executando a query
    cur.execute(f"INSERT INTO produto (nome_produto, quantidade_produto, valor_produto) VALUES ('{nome}', {qt}, {v})")

    nome_produto.delete(0, END)
    quantidade_produto.delete(0, END)
    valor_produto.delete(0, END)

    # comitando o dado
    con.commit()


# Atualiza os dados selecionados pelo usuário
def update_func():
    global cur, update_valor, update_quantidade, con, tree
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


# Checar os dados na base de dados e envia e-mail ao fornecer se a quantidade de produtos for igual a 0
def check_func():
    global cur
    situation = False
    produtos_inventario = []
    cur.execute('SELECT * FROM produto')
    rows = cur.fetchall()
    for r in rows:
        print(r)
        if r[2] == 0:
            situation = True
            produtos_inventario.append(r[1])
    msg = EmailMessage()
    msg['Subject'] = "Reposição de estoque"
    msg['From'] = 'felippoBeifong@gmail.com'
    msg['To'] = 'pedronhk@gmail.com'
    if situation:
        msg.set_content(f"Produto necessário a reposição:{produtos_inventario[0]}")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('felippoBeifong@gmail.com', 'beifongtophlinsuyin')
        smtp.send_message(msg)

    if situation:
        messagebox.showinfo('check message',
                            f'O produto {produtos_inventario[0]} está em falta! Já foi enviado e-mail ao fornecedor.',
                            icon='warning')
    else:
        messagebox.showinfo('check message', 'Sem produtos necessário a ser feito reposição.', icon='info')


def drop_func():
    global cur
    delete = False
    # Grab record data
    selected = tree.focus()
    # Grab record values
    values = tree.item(selected, 'values')
    nome = values[1]
    msg_box = messagebox.askquestion('drop record', 'Certeza que deseja deletar este dado?', icon='warning')
    if msg_box == 'yes':
        delete = True
    else:
        delete = False
    if delete:
        cur.execute(f'DELETE FROM produto WHERE nome_produto = {nome}')


# Botão de checagem de estoque
check = Button(my_Canvas, text='check', command=check_func)
check.place(x=720, y=260)

# Botão de confirmação
confirm = Button(my_Canvas, text='confirmar', command=confirm_btn)
confirm.place(x=445, y=120)

# Botão de atualização
update = Button(my_Canvas, text='update', command=update_func)
update.place(x=680, y=205)

# Botão de retirada de item na base de dados
drop = Button(my_Canvas, image='drop', command=drop_func)

mainloop()
