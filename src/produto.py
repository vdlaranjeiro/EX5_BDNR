def create_produto(driver):
    print('\nInsira as informações do produto')
    nome = input('Nome: ')
    descricao = input('Descrição: ')

    validacaoValor = 0
    while(validacaoValor != 1):
        valor = input('Valor: ')
        try:
            valor = float(valor)
            validacaoValor = 1
        except ValueError:
            print('Insira um valor válido')
    
    validacaoQuantidade = 0
    while(validacaoQuantidade != 1):
        quantidade = input('Quantidade disponível: ')
        if(quantidade.isnumeric()):
            quantidade = int(quantidade)
            validacaoQuantidade = 1
        else:
            print('Insira um valor válido')

    with driver.session() as session:
        produto = {
            "nome": nome,
            "descricao": descricao,
            "valor": valor,
            "quantidade": quantidade
        }
        vendedor = {"documento": input('\nDigite o cpf ou cnpj do vendedor: ')}
        params = {**produto, **vendedor}

        query = (
            "MATCH (v:Vendedor {documento: $documento}) "
            "CREATE (p:Produto {nome: $nome, descricao: $descricao, valor: $valor, quantidade: $quantidade})"
            "MERGE (p)-[:VENDIDO_POR]->(v)"
            )
        
        try:
            result = session.run(query, params)
            summary = result.consume()
            if summary.counters.nodes_created == 0 and summary.counters.relationships_created == 0:
                raise Exception(f"Não foram encontrados vendedores com o documento especificado.")
            else:
                print("Produto cadastrado!")
        except Exception as e:
            print(f"Ocorreu um erro durante o cadastro do produto: {e}")
    return

def read_produto(driver):
    read_all_produto(driver)

    idProduto = int(input('\nDigite o código do produto que deseja encontrar: '))

    with driver.session() as session:
        query = "MATCH (p:Produto) WHERE id(p) = $idProduto RETURN p"
        produtos = session.run(query, {"idProduto": idProduto})

        if produtos.peek() is None:
            print('Código de produto inválido.')
        else:
            produto = produtos.single()["p"]
            print("\nInformações do produto:")
            print(f'Nome: {produto["nome"]}')
            print(f'Descrição: {produto["descricao"]}')
            print(f'Valor: {produto["valor"]}')
            print(f'Quantidade disponível: {produto["quantidade"]}')
    
    return

def read_all_produto(driver):
    with driver.session() as session:
        query = "MATCH (p:Produto) RETURN p.nome as nome, id(p) as NodeID"
        produtos = session.run(query)

        if produtos.peek() is None:
            print("Não há produtos cadastrados")
        else:
            print("\nProdutos:")
            for produto in produtos:
                print(f"\nCódigo: {produto['NodeID']}")
                print(f"Nome: {produto['nome']}")

    return