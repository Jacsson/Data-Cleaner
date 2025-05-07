
## Projeto de Tratamento de Dados em Python

Este projeto é uma ferramenta para manipulação de dados em arquivos CSV, XLSX e JSON, incluindo funcionalidades como renomear colunas, alterar tipos de dados, tratar valores nulos, criar novas colunas, remover colunas e exportar para diferentes formatos. É uma ferramenta interativa e fácil de usar, ideal para quem precisa de manipulação de dados em Python.

## Funcionalidades

- **Importação de Arquivos:** Importa arquivos nos formatos CSV, XLSX e JSON.
- **Renomear Colunas:** Permite renomear colunas específicas de um DataFrame.
- **Alterar Tipo de Coluna:** Altera o tipo de dados de uma coluna para tipos como `int`, `float`, `str`, `bool` ou `datetime`.
- **Tratar Valores Nulos:** Oferece diferentes opções para lidar com valores nulos, como preencher com valor fixo, média, mediana ou remover as linhas com valores nulos.
- **Criar Novas Colunas:** Permite a criação de novas colunas com base em operações como soma de colunas numéricas, concatenação de textos, preenchimento com valores fixos ou extração de partes de datas (ano, mês, dia).
- **Remover Colunas:** Remove colunas específicas de um DataFrame.
- **Exportação de Arquivos:** Permite exportar os dados manipulados de volta para arquivos CSV, XLSX ou JSON.

## Tecnologias Utilizadas

- **Python 3.2**
- **Pandas** - Biblioteca para manipulação de dados.
- **Openpyxl** - Biblioteca para manipulação de arquivos Excel (.xlsx).
- **JSON** - Para manipulação de dados em formato JSON.

## Instruções de Uso

1. **Pré-requisitos:**
   - Instalar as dependências do projeto com o seguinte comando:
     ```bash
     pip install -r requirements.txt
     ```

2. **Rodando o Programa:**
   - Execute o script `Tratamento.py` no terminal:
     ```bash
     python Tratamento.py
     ```

## Estimativas de Tempo para Desenvolvimento

Tempo estimado para o desenvolvimento de cada parte do projeto:

| Parte do Projeto                                  | Estimativa de Tempo     |
|---------------------------------------------------|-------------------------|
| **1. Preparação do ambiente e instalação**        | 0.5 - 1 hora            |
| **2. Implementação da função de importação de arquivos (CSV, XLSX, JSON)** | 2 - 4 horas             |
| **3. Renomeação de colunas**                      | 1 - 2 horas             |
| **4. Alteração do tipo de dados das colunas**     | 2 - 4 horas             |
| **5. Tratamento de valores nulos**               | 2 - 3 horas             |
| **6. Criação de novas colunas (soma, concatenação, etc.)** | 2 - 3 horas             |
| **7. Remoção de colunas**                        | 1 - 2 horas             |
| **8. Exportação de arquivos (CSV, XLSX, JSON)**  | 1 - 2 horas             |
| **9. Testes e ajustes finais**                   | 2 - 3 horas             |
| **Tempo Total Estimado**                         | **13 - 21 horas**       |

## Contribuições

Sinta-se à vontade para contribuir com melhorias no projeto. Para isso, basta fazer um fork deste repositório, criar uma nova branch, implementar suas alterações e submeter um pull request.

## Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

**Desenvolvedor:** Jacsson Neves Luiz
