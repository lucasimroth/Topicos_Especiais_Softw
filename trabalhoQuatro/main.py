import src.DataCreate as dc
import util.validacao as val
import requisitos.gerenciadorDados as gd

df = dc.CriarDataframe('data/raw/whatsapp_chat.txt')

while True:

    print("\nEscolha uma opção:")
    print("1. Resumo das conversas")
    print("2. Histórico do remetente")
    print("3. Gráfico do histórico do remetente")
    print("4. Gráfico de pizza")
    print("5. Gráfico de linhas")
    print("6. Sair")

    opcao = val.pegarOpcao()

    if opcao == 1:
        gd.resumo_conversas(df)
    elif opcao == 2:
        remetente = input("Digite o nome do remetente: ")
        gd.mostrar_mensagens_paginadas(df, remetente)
    elif opcao == 3:
        remetente = input("Digite o nome do remetente: ")
        gd.grafico_historico_remetente(df, remetente)
    elif opcao == 4:
        gd.grafico_pizza(df)
    elif opcao == 5:
        gd.grafico_linha(df)
    elif opcao == 6:
        break
    else:
        print("Opção inválida. Digite novamente")
