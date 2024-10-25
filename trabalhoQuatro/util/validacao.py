
def pegarOpcao():
    while True:
        try:
            opcao = int(input('Digite a opção desejada: '))
            return opcao
        except ValueError:
            print('Opção inválida, tente novamente.')