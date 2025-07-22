import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

BASE_URL = "https://tabela.autoavaliar.com.br"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
}
FIPE_API_BASE = "https://parallelum.com.br/fipe/api/v1/carros"

def get_estados():
    return [
        {"sigla": "Media Nacional", "nome": "Média Nacional"},
        {"sigla": "AC", "nome": "Acre"},
        {"sigla": "AL", "nome": "Alagoas"},
        {"sigla": "AP", "nome": "Amapá"},
        {"sigla": "AM", "nome": "Amazonas"},
        {"sigla": "BA", "nome": "Bahia"},
        {"sigla": "CE", "nome": "Ceará"},
        {"sigla": "DF", "nome": "Distrito Federal"},
        {"sigla": "ES", "nome": "Espirito Santo"},
        {"sigla": "GO", "nome": "Goias"},
        {"sigla": "MA", "nome": "Maranhão"},
        {"sigla": "MT", "nome": "Mato Grosso"},
        {"sigla": "MS", "nome": "Mato Grosso do Sul"},
        {"sigla": "MG", "nome": "Minas Gerais"},
        {"sigla": "PR", "nome": "Paraná"},
        {"sigla": "PB", "nome": "Paraíba"},
        {"sigla": "PA", "nome": "Pará"},
        {"sigla": "PE", "nome": "Pernambuco"},
        {"sigla": "PI", "nome": "Piauí"},
        {"sigla": "RN", "nome": "Rio Grande do Norte"},
        {"sigla": "RS", "nome": "Rio Grande do Sul"},
        {"sigla": "RJ", "nome": "Rio de Janeiro"},
        {"sigla": "RO", "nome": "Rondônia"},
        {"sigla": "RR", "nome": "Roraima"},
        {"sigla": "SC", "nome": "Santa Catarina"},
        {"sigla": "SE", "nome": "Sergipe"},
        {"sigla": "SP", "nome": "São Paulo"},
        {"sigla": "TO", "nome": "Tocantins"},
    ]

def get_marcas():
    response = requests.get(BASE_URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    select = soup.find("select", {"id": "carBrand"})
    marcas = []
    for opt in select.find_all("option"):
        if opt.get("value") and " - " in opt["value"]:
            code, name = opt["value"].split(" - ")
            marcas.append({"id": code, "nome": name})
    return marcas

def get_modelos(marca_id):
    url = f"{BASE_URL}/getModels?make={marca_id}"
    r = requests.get(url, headers=HEADERS)
    return r.text

def get_anos(model_id):
    url = f"{BASE_URL}/getYears?model={model_id}"
    r = requests.get(url, headers=HEADERS)
    return r.text

def get_versoes(model_id, ano):
    url = f"{BASE_URL}/getVersions?year={ano}&model={model_id}"
    r = requests.get(url, headers=HEADERS)
    return r.text

def get_preco_autoavaliar(version_id, uf, version_desc, ano):
    url = f"{BASE_URL}/getPrices?version={version_id}&state={uf}&versionDesc={version_desc}&year={ano}"
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")
    price_tag = soup.find("p", class_="subtitle has-cash-mark has-text-weight-bold")
    return price_tag.text.strip() if price_tag else None

def fipe_get_marcas():
    r = requests.get(f"{FIPE_API_BASE}/marcas")
    return r.json()

def fipe_get_modelos(codigo_marca):
    r = requests.get(f"{FIPE_API_BASE}/marcas/{codigo_marca}/modelos")
    return r.json()

def fipe_get_anos(codigo_marca, codigo_modelo):
    r = requests.get(f"{FIPE_API_BASE}/marcas/{codigo_marca}/modelos/{codigo_modelo}/anos")
    return r.json()

def fipe_get_preco(codigo_marca, codigo_modelo, codigo_ano):
    url = f"{FIPE_API_BASE}/marcas/{codigo_marca}/modelos/{codigo_modelo}/anos/{codigo_ano}"
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        return data.get("Valor", None)
    return None

def parse_price_to_float(price_str):
    if not price_str:
        return None
    price_str = price_str.replace("R$", "").replace(".", "").replace(",", ".").strip()
    try:
        return float(price_str)
    except:
        return None

def find_fipe_brand_code(marcas_fipe, nome_marca_autoavaliar):
    nome_marca_autoavaliar = nome_marca_autoavaliar.lower()
    for marca in marcas_fipe:
        if marca["nome"].lower() == nome_marca_autoavaliar:
            return marca["codigo"]
    return None

def find_fipe_year_code(anos_fipe, ano_autoavaliar):
    ano_str = str(ano_autoavaliar)
    for ano in anos_fipe:
        if ano_str in ano["nome"]:
            return ano["codigo"]
    return None

def main():
    print("Digite o valor que a loja está vendendo (ex: 45000,00): ", end="")
    valor_loja_input = input().strip()
    valor_loja = parse_price_to_float(valor_loja_input)
    if valor_loja is None:
        print("Valor da loja inválido!")
        return

    # AutoAvaliar
    marcas = get_marcas()
    print("\n=== Marcas Disponíveis (AutoAvaliar) ===")
    for i, m in enumerate(marcas):
        print(f"{i + 1} - {m['nome']}")
    escolha = int(input("\nEscolha a marca: ")) - 1
    marca_id = marcas[escolha]["id"]
    nome_marca = marcas[escolha]["nome"]

    print("\n=== Modelos ===")
    html_modelos = get_modelos(marca_id)
    soup = BeautifulSoup(html_modelos, "html.parser")
    modelos = []
    for opt in soup.find_all("option"):
        if opt.get("value") and " - " in opt["value"]:
            code, name = opt["value"].split(" - ")
            modelos.append({"id": code, "nome": name})
    for i, m in enumerate(modelos):
        print(f"{i + 1} - {m['nome']}")
    escolha = int(input("\nEscolha o modelo: ")) - 1
    modelo_id = modelos[escolha]["id"]
    nome_modelo = modelos[escolha]["nome"]

    print("\n=== Anos ===")
    html_anos = get_anos(modelo_id)
    soup = BeautifulSoup(html_anos, "html.parser")
    anos = [opt["value"] for opt in soup.find_all("option") if opt.get("value")]
    for i, a in enumerate(anos):
        print(f"{i + 1} - {a}")
    escolha = int(input("\nEscolha o ano: ")) - 1
    ano = anos[escolha]

    print("\n=== Versões ===")
    html_versoes = get_versoes(modelo_id, ano)
    soup = BeautifulSoup(html_versoes, "html.parser")
    versoes = []
    for opt in soup.find_all("option"):
        if opt.get("value") and " - " in opt["value"]:
            code, name = opt["value"].split(" - ", 1)
            versoes.append({"id": code, "nome": name})
    for i, v in enumerate(versoes):
        print(f"{i + 1} - {v['nome']}")
    escolha = int(input("\nEscolha a versão: ")) - 1
    version_id = versoes[escolha]["id"]
    version_desc = versoes[escolha]["nome"]

    estados = get_estados()
    print("\n=== Estados (UF) ===")
    for i, e in enumerate(estados):
        print(f"{i + 1} - {e['nome']} ({e['sigla']})")
    escolha = int(input("\nEscolha o estado: ")) - 1
    uf = estados[escolha]["sigla"]

    preco_autoavaliar_str = get_preco_autoavaliar(version_id, uf, version_desc, ano)
    preco_autoavaliar = parse_price_to_float(preco_autoavaliar_str)
    if preco_autoavaliar_str is None:
        preco_autoavaliar_str = "Não encontrado"

    # FIPE - busca marca FIPE pelo nome da marca selecionada no AutoAvaliar
    print("\nConsultando FIPE, aproveitando marca e ano selecionados...")

    marcas_fipe = fipe_get_marcas()
    marca_fipe_id = find_fipe_brand_code(marcas_fipe, nome_marca)
    if marca_fipe_id is None:
        print(f"Marca FIPE '{nome_marca}' não encontrada! Será necessário escolher manualmente.")
        for i, m in enumerate(marcas_fipe):
            print(f"{i + 1} - {m['nome']}")
        escolha = int(input("\nEscolha a marca FIPE: ")) - 1
        marca_fipe_id = marcas_fipe[escolha]["codigo"]
    else:
        print(f"Marca FIPE encontrada: {nome_marca}")

    # Pedir para escolher modelo FIPE (única seleção extra)
    modelos_fipe = fipe_get_modelos(marca_fipe_id)["modelos"]
    print("\n=== Modelos FIPE ===")
    for i, m in enumerate(modelos_fipe):
        print(f"{i + 1} - {m['nome']}")
    escolha = int(input("\nEscolha o modelo FIPE: ")) - 1
    modelo_fipe_id = modelos_fipe[escolha]["codigo"]

    # Ano FIPE automático baseado no ano do AutoAvaliar
    anos_fipe = fipe_get_anos(marca_fipe_id, modelo_fipe_id)
    ano_fipe_id = None
    for ano_item in anos_fipe:
        if str(ano) in ano_item["nome"]:
            ano_fipe_id = ano_item["codigo"]
            break
    if ano_fipe_id is None:
        print("Ano FIPE correspondente não encontrado, escolhendo o primeiro ano disponível.")
        ano_fipe_id = anos_fipe[0]["codigo"]

    preco_fipe_str = fipe_get_preco(marca_fipe_id, modelo_fipe_id, ano_fipe_id)
    preco_fipe = parse_price_to_float(preco_fipe_str)
    if preco_fipe_str is None:
        preco_fipe_str = "Não encontrado"

    diff_loja_autoavaliar = None
    if preco_autoavaliar is not None:
        diff_loja_autoavaliar = valor_loja - preco_autoavaliar

    tabela = [
        ["AutoAvaliar", preco_autoavaliar_str],
        ["FIPE", preco_fipe_str],
        ["Valor Loja", f"R$ {valor_loja:,.2f}"],
    ]
    if diff_loja_autoavaliar is not None:
        tabela.append(["Diferença (Loja - AutoAvaliar)", f"R$ {diff_loja_autoavaliar:,.2f}"])

    print("\nResultado final:\n")
    print(tabulate(tabela, headers=["Fonte", "Valor"], tablefmt="grid", stralign="right"))

if __name__ == "__main__":
    main()
