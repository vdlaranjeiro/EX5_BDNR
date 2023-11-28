import json
from produto import read_all_produto

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

    with driver.session() as session:
        enderecos = json.dumps(enderecos)
        usuario = {"cpf": cpf, "nome": nomeCompleto, "enderecos": enderecos, "telefones": telefones, "email": email, "senha": senha}
        query = (
            "CREATE (u:Usuario {cpf: $cpf, nome: $nome, enderecos: $enderecos, telefones: $telefones, email: $email, senha: $senha})"
        )
        session.run(query, usuario)

    print("Usuário cadastrado!")
    return

def read_usuario(driver):
    cpf = input('\nDigite o cpf do usuário que deseja encontrar: ')

    with driver.session() as session:
        query = (
            "MATCH (u:Usuario {cpf: $cpf}) "
            "OPTIONAL MATCH (u)-[:COMPROU]->(p:Produto) "
            "RETURN u, COLLECT(p) as compras"
        )

        usuarios = session.run(query, {"cpf": cpf})
        
        if usuarios.peek() is None:
            print('Não foram encontrados usuários com esse CPF')
        else:
            record = usuarios.single()
            usuario = record["u"]
            compras = record["compras"]
            enderecos = json.loads(usuario["enderecos"])

            print("\nInformações do usuário:")
            print(f"CPF: {usuario['cpf']}")
            print(f"Nome: {usuario['nome']}")

            print("\nEndereços:")
            for endereco in enderecos:
                print(f"\nCEP: {endereco['cep']}")
                print(f"Rua: {endereco['rua']}")
                print(f"Número: {endereco['numero']}")
                print(f"Bairro: {endereco['bairro']}")
                print(f"Cidade: {endereco['cidade']}")
                print(f"Estado: {endereco['estado']}")

            print("\nContatos:")
            print(f"Email: {usuario['email']}")
            print("\nTelefones:")
            for telefone in usuario['telefones']:
                print(telefone)

            print("\nProdutos comprados:")
            for produto in compras:
                print(f"\nNome: {produto['nome']}")
                print(f"Descrição: {produto['descricao']}")
                print(f"Valor: {produto['valor']}")
        
    return

def read_all_usuario(driver):
    with driver.session() as session:
        query = "MATCH (u:Usuario) RETURN u.cpf as cpf, u.nome as nome"
        usuarios = session.run(query)

        if usuarios.peek() is None:
            print("Não há usuários cadastrados")
        else:
            print("\nUsuários:")
            for usuario in usuarios:
                print(f"\nCPF: {usuario['cpf']}")
                print(f"Nome: {usuario['nome']}")
    return

def compra_usuario(driver):
    cpfUsuario = input("Digite o cpf do usuário efetuando a compra: ")
    read_all_produto(driver)

    while True:
        idProduto = int(input("Escolha o código do produto que deseja comprar: "))
        if(idProduto.isnumeric()):
            idProduto = int(idProduto)
            break
        else:
            print('Insira um valor válido')
    

    with driver.session() as session:
        query = (
            "MATCH (u:Usuario) WHERE u.cpf = $cpf "
            "MATCH (p:Produto) WHERE id(p) = $idProduto "
            "MERGE (u)-[:COMPROU]->(p)"
        )

        try:
            result = session.run(query, {"cpf": cpfUsuario, "idProduto": idProduto})
            summary = result.consume()
            if summary.counters.relationships_created == 0:
                raise Exception(f"Usuário ou produto não encontrado(a).")
            else:
                print("Compra realizada!")
        except Exception as e:
            print(f"Ocorreu um erro durante o cadastro do produto: {e}")
    
    return