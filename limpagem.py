import pandas as pd

def definir_estadio(row):
    if row['casa'] == "São Paulo":
        return 'mandante'
    else:
        return 'visitante'
    
def resultado(row):
    if row['estadio'] == 'mandante':
        if row['gol_casa'] > row['gol_visitante']:
            return 'V'
        
        elif row['gol_casa'] < row['gol_visitante']:
            return 'D'
        
        elif row['gol_casa'] == row['gol_visitante']:
            return 'E'
    
    else:
        if row['gol_visitante'] > row['gol_casa']:
            return 'V'

        elif row['gol_visitante'] < row['gol_casa']:
            return 'D'

        elif row['gol_visitante'] == row['gol_casa']:
            return 'E'

def pontos(row):
    if row['rodada'] == 'Brasileirão':
        if row['resultado'] == 'V':
            return 3
        elif row['resultado'] == 'D':
            return 0
        elif row['resultado'] == 'E':
            return 1
    else:
        return None

def gols_marcados(row):
    if row['estadio'] == 'mandante':
        return row['gol_casa']
    else:
        return row['gol_visitante']

def gols_sofridos(row):
    if row['estadio'] == 'mandante':
        return row['gol_visitante']
    else:
        return row['gol_casa']


df = pd.read_csv('dados-spfc.csv', sep=';')


# excluindo colunas sem dados
df.drop(columns=['Unnamed: 9',
       'Unnamed: 10', 'Unnamed: 11', 'Unnamed: 12', 'Unnamed: 13',
       'Unnamed: 14', 'Unnamed: 15', 'Sistema de jogo'], inplace=True)

# renomeando colunas

renomear_colunas = {
    'Rodada': 'rodada',
    'Data': 'data',
    'Horário': 'horario',
    'Time da casa': 'casa',
    'Time visitante': 'visitante',
    'Treinadores': 'treinador',
    'Público': 'publico',
    'Resultado': 'placar'

}

df.rename(columns=renomear_colunas, inplace=True)

# excluindo dia da semana da data

df['data'] = df['data'].str[4:]

# conversão objeto para data dos dias dos jogos

df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')

# arrumando os nomes dos Times

df['casa'] = df['casa'].str.replace(r'\s*\(.*\)', '', regex=True).str.strip()
# \s = qualquer espaço em branco
# * = uma ou mais vezes
# \( = (
# . = qualque caractere
# * = uma ou mais vezes
# \) = )

df['visitante'] = df['visitante'].astype(str).str.replace(r'\s*\(.*\)', '', regex=True)
df['visitante'] = df['visitante'].str.strip()



# separando placares

df[['gol_casa', 'gol_visitante']] = df['placar'].str.split(':', expand=True)

# tranformando em int
df['gol_casa'] = df['gol_casa'].astype(int)
df['gol_visitante'] = df['gol_visitante'].astype(int)

# coluna indicando se o SPFC jogou em casa

df['estadio'] = df.apply(definir_estadio, axis=1)

# resultado do SPFC
df['resultado'] = df.apply(resultado, axis=1)


# pontos acumulados (evolução) brasileirao

df['pontos'] = df.apply(pontos, axis=1)

# gols marcados e sofridos

df['gols_marcados'] = df.apply(gols_marcados, axis=1)
df['gols_sofridos'] = df.apply(gols_sofridos, axis=1)


# saldo de cada partida

df['saldo'] = df['gols_marcados'] - df['gols_sofridos']

df.to_csv('dados-spfc-limpo.csv', index=False)

