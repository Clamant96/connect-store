import mysql.connector
from mysql.connector import errorcode, Error

def connect_mysql():
    global conexao
    try:
        # realiza a conexao no banco
        conexao = mysql.connector.connect(
            host='localhost',
            user='kneri',
            password='123456'
        )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Exite algo errado com as credenciais de seu banco, usuario ou senha incorreto')
        else:
            print(err)

    return conexao

def acessando_base():
    global connection

    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='connect_store',
                                             user='kneri',
                                             password='123456')

        if connection.is_connected():
            db_Info = connection.get_server_info()
            # print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            # print("Conectado no banco: ", record)

    except Error as e:
        print("Ocorreu um erro ao tentar se conectar ao banco de dados MySQL: ERRO [{}]".format(e))
        print("Vou tentar abrir a conexao novamente")

        if connection.is_connected():
            connection.close()
            connection.cursor().close()

        else:
            print("nao existe conexao ativa para essa instancia DB")

        try:
            connection = mysql.connector.connect(host='localhost',
                                                 database='connect_store',
                                                 user='kneri',
                                                 password='123456')

            if connection.is_connected():
                db_Info = connection.get_server_info()
                # print("Connected to MySQL Server version ", db_Info)
                cursor = connection.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                # print("Conectado no banco: ", record)

        except Error as e:
            print("Ocorreu um erro ao tentar se conectar ao banco de dados MySQL: ERRO [{}]".format(e))

    return connection

def criando_schemas():
    cursor = connect_mysql().cursor()  # conecata no banco

    cursor.execute(
        'DROP DATABASE IF EXISTS `connect_store`;')  # verifica se existe uma base de dados criado com esse nome, caso exista dropa a base toda

    cursor.execute('CREATE DATABASE `connect_store`;')  # cria a base de dados connect_store

    cursor.execute('USE `connect_store`')  # define a connect_store como banco atual do projeto

    # monta a estrutura dos schemas a serem cadastrados no banco
    TABLES = {}
    TABLES['Usuario'] = ('''
        CREATE TABLE `usuario` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `nome` varchar(100) NOT NULL,
            `username` varchar(20) NOT NULL,
            `email` varchar(100) NOT NULL,
            `senha` varchar(100) NOT NULL,
            PRIMARY KEY (id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;'''
                         )

    TABLES['Console'] = ('''
        CREATE TABLE `console` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `nome` varchar(100) NOT NULL,
            `icone` varchar(100) NOT NULL,
            `usuario_id` int(11),
            PRIMARY KEY (id),
            FOREIGN KEY (usuario_id) REFERENCES usuario(id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;'''
                         )

    TABLES['Categoria'] = ('''
        CREATE TABLE `categoria` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `nome` varchar(100) NOT NULL,
            `uri` varchar(100) NOT NULL,
            `img` varchar(1000) NOT NULL,
            `usuario_id` int(11),
            PRIMARY KEY (id),
            FOREIGN KEY (usuario_id) REFERENCES usuario(id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;'''
                           )

    TABLES['CategoriaConsole'] = ('''
            CREATE TABLE `categoria_console` (
                `categoria_id` int(11) NOT NULL,
                `console_id` int(11) NOT NULL,
                FOREIGN KEY (categoria_id) REFERENCES categoria(id),
                FOREIGN KEY (console_id) REFERENCES console(id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;'''
                         )

    TABLES['Jogo'] = ('''
        CREATE TABLE `jogo` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `nome` varchar(100) NOT NULL,
            `img` varchar(1000) NOT NULL,
            `preco` varchar(11) NOT NULL,
            `desconto` int(11),
            `categoria_id` int(11),
            `console_id` int(11),
            `usuario_id` int(11),
            PRIMARY KEY (id),
            FOREIGN KEY (categoria_id) REFERENCES categoria(id),
            FOREIGN KEY (console_id) REFERENCES console(id),
            FOREIGN KEY (usuario_id) REFERENCES usuario(id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;'''
                      )

    TABLES['JogoConsole'] = ('''
        CREATE TABLE `jogo_console` (
            `jogo_id` int(11) NOT NULL,
            `console_id` int(11) NOT NULL,
            FOREIGN KEY (jogo_id) REFERENCES jogo(id),
            FOREIGN KEY (console_id) REFERENCES console(id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;'''
                          )

    TABLES['CategoriaJogo'] = ('''
            CREATE TABLE `categoria_jogo` (
                `categoria_id` int(11) NOT NULL,
                `jogo_id` int(11) NOT NULL,
                FOREIGN KEY (categoria_id) REFERENCES categoria(id),
                FOREIGN KEY (jogo_id) REFERENCES jogo(id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;'''
                             )

    # insere as tabelas no banco
    for tabela_nome in TABLES:
        tabela_sql = TABLES[tabela_nome]

        try:
            print('Foi criada a tabela: {}'.format(tabela_nome), end=' ')
            cursor.execute(tabela_sql)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print('Essa tabela ja existe na base')
            else:
                print(err.msg)
        else:
            print('OK')
