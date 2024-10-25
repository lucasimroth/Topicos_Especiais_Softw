import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


"""
funcao que mostra o resumo das conversas, mostrando o total de mensagens por remetente
"""
def resumo_conversas(df):
    resumo = df.groupby('emissor').size().reset_index(name='total_conversas')
    resumo = resumo.sort_values(by='total_conversas', ascending=False)
    print("\n")
    print(resumo.to_string(index=False, justify='left', formatters={
        'emissor': '{:<20}'.format,
        'total_conversas': '{:<10}'.format
    }))
    print("\n")


"""
funcao que filtra o historico de mensagens por remetente
"""
def filtrar_historico_remetente(df, remetente):

    # Filtra pelo remetente
    historico = df[df['emissor'] == remetente].copy()  # Faz uma cópia explícita

    return historico[['data_hora', 'mensagem']]


"""
funcao que separa por pagina as mensagens do usuario escolhido, mostrando 15 mensagens por pagina
e dando a opcao de ir para a proxima pagina, pagina anterior ou sair
"""
def mostrar_mensagens_paginadas(df, remetente, page_size=15):
    historico = filtrar_historico_remetente(df, remetente)
    total_mensagens = len(historico)
    total_paginas = (total_mensagens // page_size) + (1 if total_mensagens % page_size != 0 else 0)
    current_page = 0

    while True:
        start = current_page * page_size
        end = start + page_size
        print(f"\nPágina {current_page + 1} de {total_paginas}")
        print(historico.iloc[start:end])

        print("\nOpções de navegação:")
        print("n - Próxima página")
        print("p - Página anterior")
        print("q - Sair")

        opcao = input("Escolha uma opção: ").strip().lower()

        if opcao == 'n' and current_page < total_paginas - 1:
            current_page += 1
        elif opcao == 'p' and current_page > 0:
            current_page -= 1
        elif opcao == 'q':
            break
        else:
            print("Opção inválida. Tente novamente.")

"""
funcao que mostra um grafico de barras, onde o eixo x é a data e o eixo y é a quantidade de mensagens
"""
def grafico_historico_remetente(df, remetente):
    # Filtra o DataFrame pelo remetente
    historico = df[df['emissor'] == remetente].copy()

    # Calcula o número de dias no histórico
    num_dias = (historico['data_hora'].max() - historico['data_hora'].min()).days

    # Define a granularidade com base no número de dias
    if num_dias <= 500:
        historico['periodo'] = historico['data_hora'].dt.date
        label = 'Data'
    elif num_dias <= 1000:
        historico['periodo'] = historico['data_hora'].dt.to_period('W').apply(lambda r: r.start_time).dt.date
        label = 'Semana'
    else:
        historico['periodo'] = historico['data_hora'].dt.to_period('M').apply(lambda r: r.start_time).dt.date
        label = 'Mês'

    # Conta o número de mensagens por período
    mensagens_por_periodo = historico.groupby('periodo').size()

    # Plota o histograma
    plt.figure(figsize=(15, 9))
    mensagens_por_periodo.plot(kind='bar')
    plt.title(f'Histórico de mensagens por {label.lower()} - {remetente}')
    plt.xlabel(label)
    plt.ylabel('Quantidade de mensagens')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

"""
grafico de pizza, que mostra o percentual de mensagens por remetente.
tendo uma legenda com a quantidade de mensagens por remetente
"""
def grafico_pizza(df):
    # Conta o número de mensagens por remetente
    resumo = df['emissor'].value_counts()

    # Plota o gráfico de pizza
    fig, ax = plt.subplots(figsize=(15, 9))
    wedges, texts, autotexts = ax.pie(resumo, labels=resumo.index, autopct='%1.1f%%', startangle=140)

    # Adiciona a legenda ao lado do gráfico
    ax.legend(wedges, [f"{label} - {pct}" for label, pct in zip(resumo.index, resumo)], title="Remetentes", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    plt.title('Percentual de Mensagens por Remetente')
    plt.axis('equal')
    fig.tight_layout(rect=[0, 0, 0.75, 1])
    plt.show()

"""
grafico que mostra uma linha para cada usuario, onde o eixo x é a data e o eixo y é a quantidade de mensagens
aqui para que nao de problema, se a diferença de meses for menor que 3, o grafico é feito por dia, senao por mes
"""
def grafico_linha(df):

    # Verificar a data mínima e máxima
    data_min = df['data_hora'].min()
    data_max = df['data_hora'].max()

    # Calcular a diferença em meses
    diff_meses = (data_max.year - data_min.year) * 12 + (data_max.month - data_min.month)

    # Condição para agrupar por dia ou mês
    if diff_meses <= 3:
        # Agrupar por dia
        mensagens_por_periodo = df.groupby([pd.Grouper(key='data_hora', freq='D'), 'emissor']).size().reset_index(
            name='quantidade')
    else:
        # Agrupar por mês
        mensagens_por_periodo = df.groupby([pd.Grouper(key='data_hora', freq='ME'), 'emissor']).size().reset_index(
            name='quantidade')

    # Pivotar o DataFrame
    pivot_df = mensagens_por_periodo.pivot(index='data_hora', columns='emissor', values='quantidade').fillna(0)

    # Plotar o gráfico
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=pivot_df, dashes=False)
    plt.title('Quantidade de Mensagens ao Longo do Tempo por Emissor')
    plt.xlabel('Data')
    plt.ylabel('Quantidade de Mensagens')
    plt.legend(title='Remetente', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
