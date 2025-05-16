# Importação de bibliotecas necessárias
import pandas as pd         # Manipulação de dados tabulares
import os                   # Interação com o sistema operacional (ex: limpar tela, listar arquivos)
import time                 # Controle de tempo (ex: pausas com sleep)
import openpyxl             # Leitura de arquivos Excel (.xlsx)
import json                 # Manipulação de arquivos JSON
import pathlib              # Manipulação de caminhos de arquivos e diretórios

# Exibe um aviso ao usuário sobre o local esperado dos arquivos de dados
def aviso():
    limpar_tela()
    print('|------------------------- ATENÇÃO -------------------------|')
    print('|As bases de dados precisam  estar  na  mesma pasta  onde  o|')
    print('|arquivo  "Tratamento.py"  está localizado, caso contrário o|')
    print('|programa irá exibir uma mensagem de arquivo não encontrado!|')
    print('|-----------------------------------------------------------|')
    input('Pressione ENTER para continuar...')

# Solicita ao usuário o caminho onde deseja salvar o arquivo
def caminho_pasta():
    print('Caminho para salvar arquivo:\n\n\n')
    print('Antes de continuarmos, é necessário indicar o caminho onde\no arquivo será salvo.\n')
    caminho = pathlib.Path(input(r'Entre com o caminho da pasta: '))
    
    if not caminho.exists():  # Verifica se o caminho existe
        print("Caminho inválido. Verifique e tente novamente.")
        return None
    return caminho

# Limpa o terminal (funciona para Windows e Linux/Mac)
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

# Lista arquivos de uma determinada extensão e permite ao usuário selecionar um
def listar_arquivos(extensao):
    limpar_tela()
    arquivos = [f for f in os.listdir() if f.endswith(extensao)]  # Filtra arquivos pela extensão
    print(f'Lista de arquivos tipo {extensao.upper()}:\n')
    if not arquivos:
        print(f'\nNenhum arquivo {extensao.upper()} encontrado.\n')
        time.sleep(2)
        return
    for i, arquivo in enumerate(arquivos, 1):
        print(f'({i}) - {arquivo}')
    try:
        escolha = int(input('\nArquivo a ser importado ou 0 para retornar: '))
        if escolha == 0:
            return
        elif 0 < escolha <= len(arquivos):
            importar_arquivo(arquivos[escolha - 1])
        else:
            print('Opção inválida')
            time.sleep(2)
    except ValueError:
        print('\nDigite apenas números!')
        time.sleep(2)

# Função responsável por importar diferentes tipos de arquivo: CSV, Excel ou JSON
def importar_arquivo(arquivo):
    if arquivo.lower().endswith('.csv'):
        try:
            # Primeira tentativa de leitura básica
            df = pd.read_csv(arquivo, encoding='ISO-8859-1', engine='python', on_bad_lines='skip')
            limpar_tela()
            print('------------------------- Primeira visualização ---------------------------\n')
            print('Nesta etapa, você irá checar os separadores das colunas podem ser: " , ; "!')
            print('O encoding, será necessários em casos como  em  base  de  dados  de  língua')
            print('latina. Neste ultimo caso, se o usuário não inserir  o  código  encoding  o')
            print('programa irá exibir  uma  mensagem de erro e retornar ao  menu principal.\n')
            nome = arquivo
            print(f'Arquivo: {nome}\n')
            print(df.head(1))
            print()
        except Exception as e:
            print(f"Erro ao tentar leitura inicial do arquivo: {e}")
            df = None

        # Solicita separador e encoding personalizados
        separador = input('(Opcional) Digite o separador ou pressione ENTER: ')
        code = input('(Opcional) Digite o código encoding (ex: ISO-8859-1, latin1) ou pressione ENTER: ')
        try:
            leitura_args = {k: v for k, v in zip(['sep', 'encoding'], [separador, code]) if v}
            limpar_tela()
            df = pd.read_csv(arquivo, **leitura_args)
            print(df.head(3))
            print('\nQuando se tem um encoding, é interessante identificar se há colunas numéricas com vírgula como separador decimal.')
            decimal = input('Entre o separador decimal (ex: "," ou ".") ou pressione ENTER: ')
            if decimal:
                leitura_args['decimal'] = decimal
                df = pd.read_csv(arquivo, **leitura_args)
            return sub_menu(df, arquivo)
        except Exception:
            print('ATENÇÃO: Necessário um código "encoding" para visualizar esta base de dados!')
            time.sleep(2)

    # Importa arquivos Excel
    elif arquivo.endswith('.xlsx'):
        df = pd.read_excel(arquivo, engine='openpyxl')
        sub_menu(df, arquivo)

    # Importa arquivos JSON
    elif arquivo.endswith('.json'):
        df = pd.read_json(arquivo)
        sub_menu(df, arquivo)

    # Caso o tipo de arquivo não seja reconhecido
    else:
        print('ATENÇÃO: Houve um erro ao importar o arquivo!!!')
        time.sleep(3)

# Permite ao usuário renomear colunas do DataFrame
def renomear_coluna(df):
    limpar_tela()
    print('Função: Renomear Coluna\n\n')
    for i, col in enumerate(df.columns, 1):
        print(f'({i}) - {col}')
    try:
        escolha = int(input('\nColuna a ser alterada ou 0 para retornar: '))
        if escolha == 0:
            return
        novo_nome = input('\nDigite o novo nome: ')
        df.rename(columns={df.columns[escolha - 1]: novo_nome}, inplace=True)
    except (ValueError, IndexError):
        print('\nOpção inválida. Digite um número válido.')
        time.sleep(2)

# Permite alterar o tipo de dado de colunas
def alterar_tipo_coluna(df):
    limpar_tela()
    print('Função: Alterar Tipo de Coluna\n\n')
    print(df.info())  # Mostra informações gerais sobre colunas e seus tipos
    colunas = list(df.columns)
    print()
    for i, col in enumerate(colunas, 1):
        print(f"({i}) - {col}")
    
    try:
        # Solicita ao usuário a coluna a ser alterada
        escolha = int(input('\nColuna a ser alterada ou 0 para retornar: '))
        if escolha == 0:
            return
        nome_coluna = colunas[escolha - 1]  # Obtém o nome da coluna selecionada
    except (ValueError, IndexError):
        # Caso o usuário digite algo inválido ou fora do intervalo
        print('Escolha inválida.')
        time.sleep(2)
        return

    limpar_tela()
    print(f'Coluna selecionada: {nome_coluna}')
    print('\nTipos disponíveis:')
    print('1 - int')
    print('2 - float')
    print('3 - str')
    print('4 - bool')
    print('5 - datetime')

    tipo_opcao = input('\nEscolha o tipo de destino: ')

    # Mapeia as opções numéricas para tipos Python/pandas
    tipo_dict = {
        '1': 'int',
        '2': 'float',
        '3': 'str',
        '4': 'bool',
        '5': 'datetime'
    }

    tipo_escolhido = tipo_dict.get(tipo_opcao)
    if not tipo_escolhido:
        # Se o usuário digitar um valor fora das opções
        print('Tipo inválido.')
        time.sleep(2)
        return

    try:
        # Pré-processamento para tipos numéricos
        if tipo_escolhido in ['int', 'float']:
            # Remove símbolos de moeda e separadores de milhar
            df[nome_coluna] = df[nome_coluna].replace({'\$': '', ',': ''}, regex=True)

            # Substitui vírgulas decimais por ponto, se existirem
            df[nome_coluna] = df[nome_coluna].str.replace(',', '.', regex=False)

            # Converte a coluna para numérica, forçando erros para NaN
            df[nome_coluna] = pd.to_numeric(df[nome_coluna], errors='coerce')

            if tipo_escolhido == 'int':
                # Arredonda valores antes de converter para inteiro
                df[nome_coluna] = df[nome_coluna].round().astype(int)

        elif tipo_escolhido == 'str':
            df[nome_coluna] = df[nome_coluna].astype(str)

        elif tipo_escolhido == 'bool':
            df[nome_coluna] = df[nome_coluna].astype(bool)

        elif tipo_escolhido == 'datetime':
            # Solicita o formato de data, caso o usuário queira definir manualmente
            formato = input('Deseja informar o formato da data? (ex: %d/%m/%Y) ou pressione Enter para automático: ')
            if formato.strip():
                df[nome_coluna] = pd.to_datetime(df[nome_coluna], format=formato, errors='coerce')
            else:
                df[nome_coluna] = pd.to_datetime(df[nome_coluna], errors='coerce')

        print('\nColuna alterada com sucesso!')
        time.sleep(2)

    except Exception as e:
        print(f'\nErro ao alterar tipo: {e}')
        time.sleep(3)

def verificar_nulos(df):
    limpar_tela()
    print('Função: Verifica Nulos\n\n')
    print('Valores nulos por coluna:\n')

    # Conta os valores nulos em cada coluna
    nulos = df.isnull().sum()
    print(nulos[nulos > 0])  # Exibe apenas colunas com nulos

    if nulos.sum() == 0:
        # Se não houver valores nulos
        print('\nNenhum valor nulo encontrado.')
        time.sleep(2)
        return

    # Exibe opções para tratamento dos valores nulos
    print('\n1 - Preencher nulos com um valor específico')
    print('2 - Preencher nulos com a média da coluna (numérico)')
    print('3 - Preencher nulos com a mediana da coluna (numérico)')
    print('4 - Remover linhas com valores nulos')
    print('0 - Retornar')

    opcao = input('\nEscolha uma opção: ')

    if opcao == '1':
        coluna = input('\nNome da coluna a preencher: ')
        if coluna not in df.columns:
            print('Coluna não encontrada.')
            time.sleep(2)
            return
        valor = input('Digite o valor com que deseja preencher: ')
        df[coluna].fillna(valor, inplace=True)
        print('Nulos preenchidos com sucesso.')
    
    elif opcao == '2':
        # Preencher nulos com a média da coluna (apenas para colunas numéricas)
        coluna = input('\nNome da coluna a preencher com média: ')
        if coluna not in df.columns:
            print('Coluna não encontrada.')
            time.sleep(2)
            return
        try:
            media = df[coluna].astype(float).mean()  # Converte e calcula a média
            df[coluna].fillna(media, inplace=True)
            print('Nulos preenchidos com a média com sucesso.')
        except Exception as e:
            print(f'Erro: {e}')
        time.sleep(2)

    elif opcao == '3':
        # Preencher nulos com a mediana da coluna (apenas para colunas numéricas)
        coluna = input('\nNome da coluna a preencher com mediana: ')
        if coluna not in df.columns:
            print('Coluna não encontrada.')
            time.sleep(2)
            return
        try:
            mediana = df[coluna].astype(float).median()  # Converte e calcula a mediana
            df[coluna].fillna(mediana, inplace=True)
            print('Nulos preenchidos com a mediana com sucesso.')
        except Exception as e:
            print(f'Erro: {e}')
        time.sleep(2)

    elif opcao == '4':
        # Remove todas as linhas que contêm valores nulos
        df.dropna(inplace=True)
        print('Linhas com valores nulos removidas com sucesso.')
        time.sleep(2)

    elif opcao == '0':
        # Retorna ao menu anterior
        return

    else:
        # Caso o usuário insira uma opção inválida
        print('Opção inválida.')
        time.sleep(2)

def criar_coluna(df):
    limpar_tela()
    print('Função: Criar Coluna\n\n')
    colunas = list(df.columns)
    
    # Menu de opções para o usuário escolher o tipo de nova coluna que deseja criar
    print('Criar nova coluna\n')
    print('1 - Soma de duas colunas numéricas')
    print('2 - Multiplicação de uma coluna por outra')
    print('3 - Concatenação de duas colunas de texto')
    print('4 - Preencher com valor fixo')
    print('5 - Extrair ano, mês ou dia de coluna de datas')
    print('0 - Retornar')
    
    opcao = input('\nEscolha uma opção: ')
    
    limpar_tela()
    for i, coluna in enumerate(colunas):
        print(f'({i}) - {coluna}')  # Exibe as colunas disponíveis no DataFrame

    # Caso o usuário queira criar uma nova coluna como soma de duas colunas numéricas
    if opcao == '1':
        col1 = input('Nome da primeira coluna numérica: ')
        col2 = input('Nome da segunda coluna numérica: ')
        nova = input('Nome da nova coluna: ')
        try:
            # Converte as colunas para numéricas e realiza a soma
            df[nova] = pd.to_numeric(df[col1], errors='coerce') + pd.to_numeric(df[col2], errors='coerce')
            print('Coluna criada com sucesso.')
        except Exception as e:
            print(f'Erro ao criar coluna: {e}')
    elif opcao == '2':
        col1 = input('Nome da primeira coluna numérica: ')
        col2 = input('Nome da segunda coluna numérica: ')
        nova = input('Nome da nova coluna: ')
        try:
            # Converte as colunas para numéricas e realiza a soma
            df[nova] = pd.to_numeric(df[col1], errors='coerce') * pd.to_numeric(df[col2], errors='coerce')
            print('Coluna criada com sucesso.')
        except Exception as e:
            print(f'Erro ao criar coluna: {e}')

    # Caso o usuário queira concatenar duas colunas de texto
    elif opcao == '3':
        col1 = input('Nome da primeira coluna de texto: ')
        col2 = input('Nome da segunda coluna de texto: ')
        nova = input('Nome da nova coluna: ')
        separador = input('Deseja um separador entre os valores? (ex: espaço, hífen, etc): ')
        try:
            # Concatena as colunas convertidas para string, com separador definido
            df[nova] = df[col1].astype(str) + separador + df[col2].astype(str)
            print('Coluna criada com sucesso.')
        except Exception as e:
            print(f'Erro ao criar coluna: {e}')

    # Caso o usuário queira criar uma nova coluna preenchida com um valor fixo
    elif opcao == '4':
        nova = input('Nome da nova coluna: ')
        valor = input('Valor fixo a ser preenchido: ')
        df[nova] = valor  # Preenche a coluna inteira com o mesmo valor
        print('Coluna criada com sucesso.')

    # Caso o usuário queira extrair ano, mês ou dia de uma coluna de datas
    elif opcao == '5':
        col_data = input('Nome da coluna com datas: ')
        if col_data not in df.columns:
            print('Coluna não encontrada.')
            time.sleep(2)
            return
        try:
            # Converte a coluna para datetime, tratando erros
            df[col_data] = pd.to_datetime(df[col_data], errors='coerce')
        except Exception as e:
            print(f'Erro ao converter coluna para datetime: {e}')
            time.sleep(2)
            return
        
        # Menu para o usuário escolher o que extrair da data
        print('\nExtrair:')
        print('1 - Ano')
        print('2 - Mês')
        print('3 - Dia')
        tipo = input('Escolha uma opção: ')
        nova = input('Nome da nova coluna: ')
        try:
            # Usa os atributos do datetime para extrair a parte desejada
            if tipo == '1':
                df[nova] = df[col_data].dt.year
            elif tipo == '2':
                df[nova] = df[col_data].dt.month
            elif tipo == '3':
                df[nova] = df[col_data].dt.day
            else:
                print('Opção inválida.')
                time.sleep(2)
                return
            print('Coluna criada com sucesso.')
        except Exception as e:
            print(f'Erro ao extrair dado: {e}')

    # Caso o usuário deseje retornar ao menu anterior
    elif opcao == '0':
        return

    else:
        print('Opção inválida.')  # Caso a entrada seja inválida

    time.sleep(2)  # Pequena pausa antes de voltar ao menu

def remover_coluna(df):
    limpar_tela()
    print('Função: Remover Coluna\n\n')
    colunas = list(df.columns)
    for i, coluna in enumerate(colunas, 1):  # Mostra as colunas disponíveis numeradas a partir de 1
        print(f'({i}) - {coluna}')
    try:
        user_input = int(input('\nColuna a ser removida ou 0 para retornar: '))
        if user_input > 0 and user_input <= len(colunas):  # Valida a escolha
            nome_coluna = colunas[user_input - 1]
            del df[nome_coluna]  # Remove a coluna selecionada
            return df
    except ValueError:
        print('\nErrO: Digite apenas numeros inteiros!')
        time.sleep(2)
        return
    
def save_json(df, nome_arquivo):
    # Salva o DataFrame no formato JSON
    df.to_json(nome_arquivo, orient='records', indent=4)
    print('Arquivo salvo com sucesso ;)')
    time.sleep(2)

def save_csv(df, nome_arquivo):
    # Salva o DataFrame no formato CSV
    df.to_csv(nome_arquivo, index=False)        
    print('Arquivo salvo com sucesso ;)')
    time.sleep(2)

def save_xlsx(df, nome_arquivo):
    # Salva o DataFrame no formato Excel (XLSX)
    df.to_excel(nome_arquivo, index=False) 

def exportar_arquivo(df, nome):
    limpar_tela()
    print('Função: Exportar Arquivo\n\n')

    # Remove extensão antiga para evitar duplicações
    nome = nome.replace('.csv', '').replace('xlsx', '').replace('.json', '')

    print(f'Escolha a extensão do arquivo: {nome}\n')
    print('(1) - .json')
    print('(2) - .csv')
    print('(3) - .xlsx')

    tipo_arquivo = input('Digite a opção desejada ou 0 para retornar: ')
    if tipo_arquivo == '0':
        return '0'

    nome_do_arquivo = input('Digite o nome do arquivo: ')

    # Adiciona a extensão e salva o arquivo
    if tipo_arquivo == '1':
        nome_do_arquivo += '.json'
        nome_do_arquivo = caminho_pasta() / nome_do_arquivo
        save_json(df, nome_do_arquivo)
    elif tipo_arquivo =='2':
        nome_do_arquivo += '.csv'
        nome_do_arquivo = caminho_pasta() / nome_do_arquivo
        save_csv(df, nome_do_arquivo)
    elif tipo_arquivo == '3':
        nome_do_arquivo += '.xlsx'
        nome_do_arquivo = caminho_pasta() / nome_do_arquivo
        save_xlsx(df, nome_do_arquivo)
    else:
        print('Opção inválida!')
        time.sleep()
        return

def sub_menu(df, nome):
    while True:
        limpar_tela()
        print(f'Base de dados: {nome.replace(".csv", "").replace(".xlsx", "")}\n')
        print(df)  # Mostra o DataFrame

        # Menu de opções
        print('\n1 - Renomear Coluna')
        print('2 - Tipo de coluna e informações')
        print('3 - Alterar tipo da coluna')
        print('4 - Verificar valores nulos')
        print('5 - Criar Coluna')
        print('6 - Remover coluna')
        print('7 - Exportar arquivo')
        print('\n0 - Sair sem salvar')

        escolha = input('\nOpção: ')

        # Direciona para a função correspondente
        if escolha == '1':
            renomear_coluna(df)
        elif escolha == '2':
            limpar_tela()
            print(df.info())  # Mostra informações do DataFrame
            input('\nPressione enter para continuar...')
        elif escolha == '3':
            alterar_tipo_coluna(df)
        elif escolha == '4':
            verificar_nulos(df)
        elif escolha == '5':
            criar_coluna(df)
        elif escolha == '6':
            remover_coluna(df)
        elif escolha == '7':
            exportar_arquivo(df, nome)
        elif escolha == '0':
            print('Retornando ao menu principal...')
            time.sleep(2)
            return
        else:
            print("\nOpção inválida! Tente novamente.")
            time.sleep(2)

def main():
    while True:
        limpar_tela()
        print('----------- Menu Principal -----------\n')
        print('1 - Visualizar arquivos CSVs')
        print('2 - Visualizar arquivos XLSX')
        print('3 - Visualizar arquivos JSON')
        print('\n0 - Sair do programa')

        escolha = input('\nOpção: ')

        # Executa a função conforme o tipo de arquivo escolhido
        if escolha == '1':
            listar_arquivos('.csv')
        elif escolha == '2':
            listar_arquivos('.xlsx')
        elif escolha == '3':
            listar_arquivos('.json')
        elif escolha == '0':
            # Contagem regressiva para saída do programa
            [print(f'\rEncerrando o programa... {i}', end='', flush=True) or time.sleep(1) for i in range(5, 0, -1)]
            print('\n\nPrograma encerrado.')
            break
        else:
            print('Opção inválida.')
            time.sleep(1)

if __name__ == "__main__":
    aviso()  # Mensagem de boas-vindas (função definida antes)
    main()   # Inicia o menu principal