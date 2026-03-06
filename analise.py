import pandas as pd

df = pd.read_csv('dados-spfc-limpo.csv')
print(df.head(1))
print(df.columns)
# Vitórias, Empates e Derrotas

vitorias = (df['resultado'] == 'V').sum()
derrotas = (df['resultado'] == 'D').sum()
empates = (df['resultado'] == 'E').sum()

print(f'O total de vitorias é : {vitorias}')
print(f'O total de derrotas é : {derrotas}')
print(f'O total de empates é : {empates}')

# Saldo de gols

saldo = df['saldo'].sum()

print(f'O saldo de gols é: {saldo}')

# aproveitamento

pontos_conquistados = (vitorias * 3) + (empates*1)
pontos_disputados = (df['rodada'].value_counts()) * 3
aproveitamento = (pontos_conquistados / pontos_disputados) * 100
print(aproveitamento)

