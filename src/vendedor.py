import json

def create_vendedor(driver):
    print('\nInsira as informações do vendedor')
    nome = input('Nome do vendedor ou da loja: ')

    verificacaoVendedor = 0
    while(verificacaoVendedor != 1):
        pessoaFisicaOuJuridica = input('Pessoa Física ou Jurídica? F/J ').upper()
        if(pessoaFisicaOuJuridica == 'F'):
            documento = input('CPF: ')
            verificacaoVendedor = 1
        elif(pessoaFisicaOuJuridica == 'J'):
            documento = input('CNPJ: ')
            verificacaoVendedor = 1
        else:
            print('Opção inválida. Selecione F para pessoa física ou J para pessoa jurídica.')

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
        vendedor = {
            "nome": nome,
            "documento": documento,
            "enderecos": enderecos,
            "telefones": telefones,
            "email": email,
            "senha": senha
        }

        query = (
            "CREATE (v:Vendedor {documento: $documento, nome: $nome, enderecos: $enderecos, telefones: $telefones, email: $email, senha: $senha})"
        )

        session.run(query, vendedor)
    
    print(f'\nVendedor cadastrado!')

    return

def read_vendedor(driver):
    cpfOuCnpj = input('Digite o cpf ou cnpj do vendedor que deseja encontrar: ')

    with driver.session() as session:
        query = (
            "MATCH (v:Vendedor {documento: $documento}) "
            "OPTIONAL MATCH (v)<-[:VENDIDO_POR]-(p:Produto) "
            "RETURN v, COLLECT(p) as produtosVendidos"
        )

        vendedores = session.run(query, {"documento": cpfOuCnpj})
    
        if vendedores.peek() is None:
            print('Não foram encontrados vendedores com essas informações')
        else:
            record = vendedores.single()
            vendedor = record["v"]
            produtosVendidos = record["produtosVendidos"]

            enderecos = json.loads(vendedor["enderecos"])
            
            print("\nInformações do vendedor:")
            print(f"Documento: {vendedor['documento']}")
            print(f"Nome: {vendedor['nome']}")

            print("\nEndereços:")
            for endereco in enderecos:
                print(f"\nCEP: {endereco['cep']}")
                print(f"Rua: {endereco['rua']}")
                print(f"Número: {endereco['numero']}")
                print(f"Bairro: {endereco['bairro']}")
                print(f"Cidade: {endereco['cidade']}")
                print(f"Estado: {endereco['estado']}")

            print("\nContatos:")
            print(f"Email: {vendedor['email']}")
            print("\nTelefones:")
            for telefone in vendedor['telefones']:
                print(telefone)

            print("\nProdutos Vendidos:")
            for produto in produtosVendidos:
                print(f"\nNome: {produto['nome']}")
                print(f"Descrição: {produto['descricao']}")
                print(f"Valor: {produto['valor']}")
                print(f"Quantidade: {produto['quantidade']}")

    return

def read_all_vendedor(driver):
    with driver.session() as session:
        query = "MATCH (v:Vendedor) RETURN v.documento as documento, v.nome as nome"
        vendedores = session.run(query)

        if vendedores.peek() is None:
            print("Não há vendedores cadastrados")
        else:
            print("\nVendedores:")
            for vendedor in vendedores:
                print(f"\nDocumento: {vendedor['documento']}")
                print(f"Nome: {vendedor['nome']}")
    return