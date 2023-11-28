from neo4j import GraphDatabase

from usuario import *
from vendedor import *
from produto import *

URI = ""
AUTH = ("neo4j", "")

driver = GraphDatabase.driver(URI, auth=AUTH)

opcao = 0
while(opcao != 'S'):
    print("\n1 - Manipulação de Usuários")
    print("2 - Manipulação de Vendedores")
    print("3 - Manipulação de Produtos")
    opcao = input("Selecione uma opção. (S para sair) ").upper()

    acao = 0
    match opcao:
        case '1':
            while(acao != 'V'):
                print("\n --- Manipulação de Usuários ---")
                print("1 - Cadastrar um novo usuário")
                print("2 - Listar todos os usuários")
                print("3 - Listar informações de um usuário")
                print("4 - Realizar uma compra")
                acao = input("Selecione uma ação. (V para voltar) ").upper()
                match acao:
                    case '1':
                        create_usuario(driver)
                    case '2':
                        read_all_usuario(driver)
                    case '3':
                        read_usuario(driver)
                    case '4':
                        compra_usuario(driver)

        case '2':
             while(acao != 'V'):
                print("\n --- Manipulação de Vendedores ---")
                print("1 - Cadastrar um novo vendedor")
                print("2 - Listar todos os vendedores")
                print("3 - Listar informações de um vendedor")
                acao = input("Selecione uma ação. (V para voltar) ").upper()
                match acao:
                    case '1':
                        create_vendedor(driver)
                    case '2':
                        read_all_vendedor(driver)
                    case '3':
                        read_vendedor(driver)
            
        case '3':
             while(acao != 'V'):
                print("\n --- CRUD de Produtos ---")
                print("1 - Cadastrar um novo produto")
                print("2 - Listar todos os produtos")
                print("3 - Listar informações de um produto")
                acao = input("Selecione uma ação. (V para voltar) ").upper()
                match acao:
                    case '1':
                        create_produto(driver)
                    case '2':
                        read_all_produto(driver)
                    case '3':
                        read_produto(driver)
                        
driver.close()