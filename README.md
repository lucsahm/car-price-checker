# car-price-checker

Aqui está um README.md inicial para o seu projeto:

markdown
Copiar
Editar
# AutoAvaliar x FIPE - Comparador de Preços de Carros

Este projeto tem como objetivo **comparar o preço de venda de um carro** com as tabelas **AutoAvaliar** e **FIPE**, exibindo a diferença entre o valor informado e as referências de mercado.

## Funcionalidades

- Consulta automática de marcas, modelos, versões e anos no site [AutoAvaliar](https://tabela.autoavaliar.com.br).
- Consulta dos preços na API da [Tabela FIPE](https://deividfortuna.github.io/fipe/).
- Comparação entre:
  - Preço informado pelo usuário.
  - Valor de referência da AutoAvaliar.
  - Valor de referência da FIPE.
- Exibição de tabela final com as diferenças.

## Exemplo de Uso

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/autoavaliar-fipe-compare.git
   cd autoavaliar-fipe-compare
Instale as dependências necessárias:

bash
Copiar
Editar
pip install -r requirements.txt
Execute o script:

bash
Copiar
Editar
python car_price_compare.py
Informe o valor de venda do carro e siga as instruções para escolher marca, modelo, ano e versão.

Exemplo de Saída
sql
Copiar
Editar
Resultado final:

+--------------------------------------+--------------+
|                              Fonte   |        Valor |
+--------------------------------------+--------------+
|                        AutoAvaliar   |     R$ 45.000|
|                               FIPE   |     R$ 46.500|
|                          Valor Loja  |     R$ 47.000|
|   Diferença (Loja - AutoAvaliar)     |     R$  2.000|
+--------------------------------------+--------------+
Dependências
requests

beautifulsoup4

tabulate

Você pode instalar todas de uma vez com:

bash
Copiar
Editar
pip install requests beautifulsoup4 tabulate
Próximas Melhorias (TODO)
 Automatizar a correspondência entre marcas do AutoAvaliar e da FIPE.

 Adicionar opção para exportar os resultados em CSV.

 Criar interface web ou CLI interativa para o projeto.

 Adicionar testes automatizados.

Licença
Este projeto é distribuído sob a licença MIT. Sinta-se livre para usar e modificar.

Autor: Lucas Sahm
