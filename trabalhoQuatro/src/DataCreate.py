import pandas as pd
import re

# Função para gerar o dataframe
def CriarDataframe(file_path):

    # Lista para armazenar os dados
    dados_conversa = []
    linhas_invalidas = []

    # Le o arquivo
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Usa regex para capturar data, hora, remetente e mensagem
            match = re.match(r'(\d{2}/\d{2}/\d{4} \d{2}:\d{2}) - (.*?): (.*)', line)
            if match:
                data_hora, emissor, mensagem = match.groups()
                dados_conversa.append({'data_hora': data_hora, 'emissor': emissor, 'mensagem': mensagem})
            else:
                # Se a linha nao estiver dentro do padrao ela é armazenada
                linhas_invalidas.append(line)

    # Cria um DataFrame
    df = pd.DataFrame(dados_conversa)

    # Converte a coluna data_hora para datetime
    df['data_hora'] = pd.to_datetime(df['data_hora'], format='%d/%m/%Y %H:%M')

    #exibe as linhas para noção dos problemas
    if linhas_invalidas:
        print("Linhas inválidas:")
        for linha in linhas_invalidas:
            print(linha)

    return df

