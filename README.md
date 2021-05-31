# Software-de-estoque
App criado para gerenciamento de produtos no inventário.
Utilizado ```Tkinter``` como a interface gráfica, para a 
base de dados foi utilizado ```postgreSQL``` e a biblioteca ```smtp``` para 
o envio de e-mail.

## Funcionalidades
O app permite a adição de um determinado produto, informando a sua quantidade,
o seu valor e o nome do produto em questão adicionando esse dado a base de 
dados:

![imagem_inventario (2)](https://user-images.githubusercontent.com/65267252/120123525-abad3b00-c185-11eb-8399-06e2deb50cd1.png)

No app temos a representação gráfica dos dados que foram armazenados na base de dados
, podemos atualizar a tabela a qualquer momento para visualizar o nome produto
adicionado a base de dados.

![imagem_inventario (3)](https://user-images.githubusercontent.com/65267252/120123579-ffb81f80-c185-11eb-8a02-1d7ca880f9a2.png)


A tabela não é somente para visualização destes dados, mas também, para atualizar
um determinado produto ou a retirada do mesmo. Basta selecionar o produto em questão
clickando no produto na tabela e clickar no ícone da lixeira, deletando o produto
selecionado. Para atualizar um produto só selecionar e informar a nova quantidade e 
seu novo valor:

![tabela_dados](https://user-images.githubusercontent.com/65267252/120124335-5aec1100-c18a-11eb-9bc4-48ac524636a2.gif)


O app ainda possui a funcionalidade de envio de e-mails... digamos que esteja em falta
um determinado produto e seja necessário pedir uma nova remessa do mesmo ao fornecedor,
basta então informar o e-mail de contato do fornecedor e clickar no botão checar, e nele
será feito uma checagem em todos os itens da base de dados se algum deles possui a
sua quantidade igual a 0, e se algum produto possuir sua quantidade igual a, o email será enviado imediatamente ao fornecedor
informando o produto.



![image](https://user-images.githubusercontent.com/65267252/120124584-6ab82500-c18b-11eb-9ffa-a3ed4ffee539.png)

