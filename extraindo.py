import pandas as pd

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
    'Resultado': 'resultado'

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


# ajustando placares de penalti

# Onde houver o número '5' no resultado, vira '1:1'
df.loc[df['resultado'].str.contains('5', na=False), 'resultado'] = '01:01'

# Onde houver o número '4' no resultado, vira '1:0'
df.loc[df['resultado'].str.contains('4', na=False), 'resultado'] = '01:00'

# loc = [condição, resultado] = alterar dados no pandas

# separando placares

df[['gol_casa', 'gol_visitante']] = df['resultado'].str.split(':', expand=True)

# tranformando em int
df['gol_casa'] = df['gol_casa'].astype(int)
df['gol_visitante'] = df['gol_visitante'].astype(int)


print(df.info())


#Vitórias
# Empates
# Derrotas
# Saldo
# Aproveitamento
# Evolução de pontos
# Casa x Fora
# Ataque x Defesa