from datetime import datetime
import uuid

def create_usuario(driver):
    print('\nInsira as informações do usuário')
    cpf = input('CPF: ')
    nomeCompleto = input('Nome completo: ')

    enderecos = []
    keyEnderecos = 0
    while(keyEnderecos != 'N'):
        print('\nDigite seu endereço: ')
        cep = input('CEP: ')
        rua = input('Rua: ')
        numero = input('Número: ')
        bairro = input('Bairro: ')
        cidade = input('Cidade: ')
        estado = input('Estado: ')

        endereco = {
            "cep": cep,
            "rua": rua,
            "numero": numero,
            "bairro": bairro,
            "cidade": cidade,
            "estado": estado
        }
        enderecos.append(endereco)
        keyEnderecos = input('\nDeseja inserir mais um endereço? S/N ').upper()

    
    telefones = []
    keyTelefones = 0
    while(keyTelefones != 'N'):
        telefone = input('DDD + Telefone: ')
        telefones.append(telefone)
        keyTelefones = input('\nDeseja cadastrar mais um telefone? S/N ').upper()

    email = input('Email: ')
    senha = input('Senha: ')
    favoritos = []
    compras = []

    with driver.session() as session:
        telefones = str(telefones)
        usuario = {"cpf": cpf, "nome": nomeCompleto, "enderecos": enderecos, "telefones": telefones, "email": email, "senha": senha}
        query = (
            "CREATE u:Usuario {cpf: $cpf, nome: $nome, enderecos: $enderecos, telefones: $telefones, email: $email, senha: $senha}"
        )
        session.run(query, usuario)
    
    print(f'\nUsuário cadastrado!')
    return

    cpf = input('\nDigite o cpf do usuário que deseja excluir: ')

    myquery = {"cpf": cpf}
    mycol = db.Usuarios

    mydoc = mycol.delete_one(myquery)
    print(f'Deletando o usuário {mydoc}')
    return

def read_usuario(driver):
    cpf = input('\nDigite o cpf do usuário que deseja encontrar: ')

    with driver.session() as session:
        query = "MATCH (u:Usuario) WHERE u.cpf = $cpf RETURN u"
        usuarios = session.run(query, {"cpf": cpf})

    usuarios = list(usuarios)

    if not usuarios:
        print('Não foram encontrados usuários com esse CPF')
    else:
        for usuario in usuarios:
            print("\nInformações do usuário:")
            print(f"CPF: {usuario['cpf']}")
            print(f"Nome: {usuario['nome']}")

            print("Endereços:")
            for endereco in usuario['enderecos']:
                print(f"\nCEP: {endereco['cep']}")
                print(f"Rua: {endereco['rua']}")
                print(f"Número: {endereco['numero']}")
                print(f"Bairro: {endereco['bairro']}")
                print(f"Cidade: {endereco['cidade']}")
                print(f"Estado: {endereco['estado']}")

            print("\nContatos:")
            print(f"Email: {usuario['contatos']['email']}")
            print("Telefones:")
            for telefone in usuario['contatos']['telefones']:
                print(telefone)

            print("\nFavoritos:")
            for favorito in usuario['favoritos']:
                print(favorito)

            print("\nCompras:")
            for compra in usuario['compras']:
                print(compra)
    
    return

    cpf = input('\nDigite o cpf do usuário que deseja atualizar: ')

    colunaUsuarios = db.Usuarios
    usuario = {"cpf": cpf}
    mydoc = colunaUsuarios.find_one(usuario)

    if(mydoc):
        print(f'Editando informações de {mydoc["nome"]}. Aperte ENTER para pular um campo')
        nomeCompleto = input('Novo nome: ')
        if len(nomeCompleto):
            mydoc["nome"] = nomeCompleto

        keyUpdateEnderecos = input('\nDeseja atualizar os endereços? S/N ').upper()
        if(keyUpdateEnderecos == 'S'):
            keyOpcaoEnderecos = 0
            while(keyOpcaoEnderecos != 'C'):
                print('1 - Adicionar um endereço')
                print('2 - Remover um endereço existente')
                keyOpcaoEnderecos = input('Escolha uma opção: (C para cancelar) ').upper()

                match keyOpcaoEnderecos:
                    case '1':
                        endereco = {
                            "cep": input('CEP: '),
                            "rua": input('Rua: '),
                            "numero": input('Numero: '),
                            "bairro": input('Bairro: '),
                            "cidade": input('Cidade: '),
                            "estado": input('Estado: ')
                        }

                        mydoc["enderecos"].append(endereco)
                        print('Endereço adicionado!\n')
                    case '2':
                        contadorEndereco = 1
                        for endereco in mydoc["enderecos"]:
                            print(f'\nEndereço {contadorEndereco}')
                            print(f"CEP: {endereco['cep']}")
                            print(f"Rua: {endereco['rua']}")
                            print(f"Número: {endereco['numero']}")
                            print(f"Bairro: {endereco['bairro']}")
                            print(f"Cidade: {endereco['cidade']}")
                            print(f"Estado: {endereco['estado']}")

                            contadorEndereco+=1
                        
                        enderecoEscolhido = input('Escolha o endereço que você deseja remover: ')
                        if enderecoEscolhido.isdigit():
                            enderecoEscolhido = int(enderecoEscolhido)
                            if enderecoEscolhido > contadorEndereco:
                                print('Endereço inválido\n')
                            else:
                                mydoc["enderecos"].pop(enderecoEscolhido - 1)
                                print('Endereço removido!\n')
                        else:
                            print('Endereço inválido\n')

        keyUpdateTelefones = input('\nDeseja atualizar os telefones? S/N ').upper()
        if(keyUpdateTelefones == 'S'):
            keyOpcaoTelefones = 0
            while(keyOpcaoTelefones != 'C'):
                print('1 - Adicionar um telefone')
                print('2 - Remover um telefone existente')
                keyOpcaoTelefones = input('Escolha uma opção: (C para cancelar) ').upper()

                match keyOpcaoTelefones:
                    case '1':
                        novoTelefone = input('Digite o novo telefone (DDD + Número): ')
                        mydoc["contatos"]["telefones"].append(novoTelefone)
                        print('Telefone adicionado!')
                    case '2':
                        contadorTelefones = 1
                        for telefone in mydoc["contatos"]["telefones"]:
                            print(f'Telefone {contadorTelefones}')
                            print(telefone)

                            contadorTelefones+=1

                        telefoneEscolhido = input('Escolha o telefone que você deseja remover: ')
                        if telefoneEscolhido.isdigit():
                            telefoneEscolhido = int(telefoneEscolhido)
                            if telefoneEscolhido > contadorTelefones:
                                print('Telefone inválido\n')
                            else:
                                mydoc["contatos"]["telefones"].pop(telefoneEscolhido - 1)
                                print('Telefone removido!\n')
                        else:
                            print('Telefone inválido\n')

        email = input('Novo email: ')
        if len(email):
            mydoc["contatos"]["email"] = email
        
        keyUpdateFavoritos = input('\nDeseja atualizar os favoritos? S/N ').upper()
        if(keyUpdateFavoritos == 'S'):
            keyOpcaoFavoritos = 0
            while(keyOpcaoFavoritos != 'C'):
                print('1 - Adicionar um favorito')
                print('2 - Remover um item favorito')
                keyOpcaoFavoritos = input('Escolha uma opção: (C para cancelar) ').upper()
                match keyOpcaoFavoritos:
                    case '1':
                        nomeProduto = input('Qual produto você deseja adicionar? ')
                        queryProduto = {"nome": nomeProduto}
                        colunaProdutos = db.Produtos
                        produtos = colunaProdutos.find(queryProduto)

                        produtos = list(produtos)
                        if not(produtos):
                            print('Não foram encontrados produtos com essas informações')
                        else:
                            for produto in produtos:
                                print(f'\nCódigo: {produto["_id"]}')
                                print(f'Nome: {produto["nome"]}')
                                print(f'Descrição: {produto["descricao"]}')
                                print(f'Valor: {produto["valor"]}')

                            idProdutoEscolhido = input('Digite o código do produto escolhido: ')
                            if(idProdutoEscolhido.isnumeric()):
                                produtoEscolhido = next((produto for produto in produtos if produto["_id"] == int(idProdutoEscolhido)), None)
                                if(produtoEscolhido):
                                    favorito = {
                                    "_id": str(uuid.uuid4()),
                                    "id_produto": produtoEscolhido["_id"],
                                    "nome": produtoEscolhido["nome"],
                                    "descricao": produtoEscolhido["descricao"],
                                    "valor": produtoEscolhido["valor"]
                                    }

                                    mydoc["favoritos"].append(favorito)
                                    print(f'{produtoEscolhido["nome"]} adicionado aos favoritos')
                                else:
                                    print('Código inválido')
                            else:
                                print('Código inválido')
                    case '2':
                        if not(mydoc["favoritos"]):
                            print('Não há itens nos favoritos para remover')
                        else:
                            for favorito in mydoc["favoritos"]:
                                print(f'\nCódigo: {favorito["id_produto"]}')
                                print(f'Nome: {favorito["nome"]}')
                                print(f'Descrição: {favorito["descricao"]}')
                                print(f'Valor: {favorito["valor"]}')
                            
                            idFavoritoEscolhido = input('Digite o código do favorito que deseja remover: ')
                            if(idFavoritoEscolhido.isnumeric()):
                                favoritoEscolhido = next((favorito for favorito in mydoc["favoritos"] if favorito["id_produto"] == int(idFavoritoEscolhido)), None)
                                if(favoritoEscolhido):
                                    mydoc["favoritos"].remove(favoritoEscolhido)
                                    print('Favorito removido')
                                else:
                                    print('Código inválido')
                            else:
                                print('Código inválido')

        novasInformacoes = {"$set": mydoc}
        colunaUsuarios.update_one(usuario, novasInformacoes)
        print('\nInformações atualizadas com sucesso!')
    else:
        print("\nNão foram encontrados usuários com esse CPF")

    return

def compra_usuario(db):
    cpf = input('Digite o cpf do usuário realizando a compra: ')
    colunaUsuarios = db.Usuarios
    queryUsuario = {"cpf": cpf}
    usuario = colunaUsuarios.find_one(queryUsuario)

    if not(usuario):
        print('Usuário não encontrado')
    else:
        nomeProduto = input('Qual produto deseja comprar? ')
        colunaProdutos = db.Produtos
        queryProduto = {"nome": {"$regex": nomeProduto, "$options": "i"}}
        produtos = colunaProdutos.find(queryProduto)
        produtos = list(produtos)

        if not(produtos):
            print('Produto não encontrado')
        else:
            for produto in produtos:
                print('\nProdutos encontrados:')
                print(f'\nCódigo: {produto["_id"]}')
                print(f'Nome: {produto["nome"]}')
                print(f'Descrição: {produto["descricao"]}')
                print(f'Valor: {produto["valor"]}')

            verificacaoCodigoProduto = 0
            produtoEscolhido = {}
            while(verificacaoCodigoProduto != 1):
                idProdutoEscolhido = input('Digite o código do produto que deseja comprar: ')
                if(idProdutoEscolhido.isnumeric()):
                    produtoEscolhido = next((produto for produto in produtos if produto["_id"] == int(idProdutoEscolhido)), None)
                    if(produtoEscolhido):
                        verificacaoCodigoProduto = 1
                    else:
                        print('Código inválido')
                else:
                    print('Código inválido')

            verificacaoQuantidadeProduto = 0
            quantidadeDisponivel = produtoEscolhido["quantidade"]
            while(verificacaoQuantidadeProduto != 1):
                print(f'\nQuantidade disponível: {quantidadeDisponivel}')
                quantidadeEscolhida = input('Quantas unidades deseja comprar? ')

                if(quantidadeEscolhida.isnumeric()):
                    quantidadeEscolhida = int(quantidadeEscolhida)
                    if(quantidadeEscolhida > quantidadeDisponivel):
                        print('Quantidade indisponível')
                    else:
                        verificacaoQuantidadeProduto = 1
                else:
                    print('Digite uma quantidade válida.')

            print(f'\nCompra no nome de {usuario["nome"]}')
            print(f'Produto: {produtoEscolhido["nome"]}')
            print(f'Quantidade: {quantidadeEscolhida}')
            print(f'Valor: {produtoEscolhido["valor"] * quantidadeEscolhida}')

            confirmarCompra = input('\nConfirmar compra? S/N ').upper()
            if(confirmarCompra == 'S'):
                dataAtual = datetime.now()
                compra = {
                    "_id": str(uuid.uuid4()),
                    "id_produto": produtoEscolhido["_id"],
                    "nome_produto": produtoEscolhido["nome"],
                    "descricao_produto": produtoEscolhido["descricao"],
                    "quantidade": quantidadeEscolhida,
                    "valor_compra": produtoEscolhido["valor"] * quantidadeEscolhida,
                    "data_compra": dataAtual.strftime('%d/%m/%Y %H:%M')
                }


                usuario["compras"].append(compra)
                novasInformacoes = {"$set": usuario}
                colunaUsuarios.update_one(queryUsuario, novasInformacoes)

                queryProduto = {"_id": produtoEscolhido["_id"]}
                novasInformacoes = {"$set": {
                    "quantidade": produtoEscolhido["quantidade"] - quantidadeEscolhida
                }}
                colunaProdutos.update_one(queryProduto, novasInformacoes)

                print('Compra realizada com sucesso! ')

            elif(confirmarCompra == 'N'):
                print('Compra cancelada.')

    return