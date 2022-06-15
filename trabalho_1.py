#Programa que simula um aplicativo de música

lista_de_musicas = []
memoria_acoes = []
lista_sem_musica_tocando = []
musicas_deletadas = []
posicao_musicas_deletadas = []
posicao_musicas_deletadas_base = []
posicao_antes_do_next = []
posicao_pos_next = []
lista_base = []
musicas_terminadas = []
play = False
acabou = False
musica_tocando = ''

#Adicionar músicas no final da lista
def adicionar(musica):
    global lista_de_musicas
    global memoria_acoes
    global lista_base
    memoria_acoes = memoria_acoes + ['adicionar']
    
    lista_de_musicas.append(musica)
    lista_base.append(musica)
    
    return lista_de_musicas
#Começa a tocar a música
def turn_on():
    global play
    global memoria_acoes
    global musica_tocando
    global lista_de_musicas
    memoria_acoes = memoria_acoes + ['turn_on']
    if musica_tocando == '' and len(lista_de_musicas) > 0:
        musica_tocando = lista_de_musicas[0]
    
    play = True
    
    return play
#Para de tocar a música
def turn_off():
    global play
    
    play = False
    
    return play
#Deleta uma música
def deletar(musica):
    global lista_de_musicas
    global memoria_acoes
    global musicas_deletadas
    global posicao_musicas_deletadas
    global lista_base
    global posicao_musicas_deletadas_base
    
    if play and musica in lista_de_musicas[1:]:
        posicao = lista_de_musicas[1:].index(musica) + 1
        posicao_musicas_deletadas.append(posicao)
        posicao_musicas_deletadas_base.append(lista_base.index(musica))
        
        memoria_acoes.append('deletar')
        musicas_deletadas.append(musica)
        
        lista_de_musicas.pop(posicao)
        lista_base.remove(musica)
        
    elif not play and musica in lista_de_musicas:
        posicao_musicas_deletadas.append(lista_de_musicas.index(musica))
        posicao_musicas_deletadas_base.append(lista_base.index(musica))
        memoria_acoes.append('deletar')
        musicas_deletadas.append(musica)
        
        lista_de_musicas.remove(musica)
        lista_base.remove(musica)
       
    return lista_de_musicas 
#Coloca uma música na fila para ser a próxima a ser tocada
def next(musica):
    global lista_de_musicas
    global memoria_acoes
    global lista_sem_musica_tocando
    global musicas_terminadas
    
    if musica in lista_base:
        if play and musica in lista_de_musicas[1:] or musica_tocando != '' and musica in lista_de_musicas[1:]:
            primeira_ocorrencia = (lista_de_musicas[1:].index(musica)) + 1
            memoria_acoes.append('next')
            posicao_antes_do_next.append(primeira_ocorrencia)
            posicao_pos_next.append(1)
            
            lista_de_musicas.pop(primeira_ocorrencia)
            lista_de_musicas.insert(1,musica)
            
        elif play and musica in musicas_terminadas and musica not in lista_de_musicas[1:] or musica_tocando != '' and musica in musicas_terminadas and musica not in lista_de_musicas[1:]:
            memoria_acoes.append('next_p')
            lista_de_musicas.insert(1,musica)
            
            
        elif not play and musica in lista_de_musicas and musica_tocando == '':
            memoria_acoes.append('next')
            posicao_antes_do_next.append(lista_de_musicas.index(musica))
            posicao_pos_next.append(0)
            
            lista_de_musicas.remove(musica)
            lista_de_musicas.insert(0,musica)
            
        elif not play and musica in musicas_terminadas and musica not in lista_de_musicas and musica_tocando == '':
            memoria_acoes.append('next_np')
            lista_de_musicas.insert(0,musica)
        
        return lista_de_musicas
#Imprime a lista de músicas
def listar():
    global lista_de_musicas
    
    if len(lista_de_musicas) > 0:
        contador = len(lista_de_musicas)
        for i in lista_de_musicas:
            if contador == 1:
                print(i)
            else:
                print(f'{i},',end="")
                
            contador = contador - 1
    else:
        print('[vazia]')
#Imprime a música tocando ou (se não estiver tocando) a próxima música que vai tocar
def status():
    if len(lista_de_musicas) > 0 and play or len(lista_de_musicas) > 0 and musica_tocando == '':
        print(lista_de_musicas[0])
    elif len(lista_de_musicas) > 1 and musica_tocando != '':
        print(lista_de_musicas[1])
    else:
        print("Toque! Toque, Dijê!")
#Desfaz instruções (Ctrl + Z)
def desfazer(tudo=False):
    global lista_de_musicas
    global memoria_acoes
    global musicas_deletadas
    global posicao_musicas_deletadas
    global lista_base
    global posicao_musicas_deletadas_base
    
    if len(memoria_acoes) > 0:
        if tudo:
            while len(memoria_acoes) > 0:
                desfazer(False)
        else:
            ultima_acao = memoria_acoes[(len(memoria_acoes)) - 1]

            if ultima_acao == 'adicionar':
                lista_de_musicas.pop(len(lista_de_musicas) - 1)
                lista_base.pop(len(lista_base) - 1)

                memoria_acoes.pop(len(memoria_acoes) - 1)

            elif ultima_acao == 'turn_on':
                turn_off()

                memoria_acoes.pop(len(memoria_acoes) - 1)

            elif ultima_acao == 'deletar':
                musica_deletada = musicas_deletadas.pop(len(musicas_deletadas) - 1)
                posicao = posicao_musicas_deletadas.pop(len(posicao_musicas_deletadas) - 1)
                posicao_2 = posicao_musicas_deletadas_base.pop(len(posicao_musicas_deletadas_base) - 1)
                lista_de_musicas.insert(posicao,musica_deletada)
                lista_base.insert(posicao_2,musica_deletada)

                memoria_acoes.pop(len(memoria_acoes) - 1)

            elif ultima_acao == 'next':
                ultima_posicao = posicao_pos_next.pop(len(posicao_pos_next) - 1)
                ult_pos = posicao_antes_do_next.pop(len(posicao_antes_do_next) - 1)
                musica = lista_de_musicas.pop(ultima_posicao)
                lista_de_musicas.insert(ult_pos,musica)

                memoria_acoes.pop(len(memoria_acoes) - 1)
                
            elif ultima_acao == 'next_p':
                lista_de_musicas.pop(1)
                
                memoria_acoes.pop(len(memoria_acoes) - 1)
                
            elif ultima_acao == 'next_np':
                lista_de_musicas.pop(0)
                
                memoria_acoes.pop(len(memoria_acoes) - 1)

        return lista_de_musicas
#Indica que uma música acabou, assim, começando a próxima
def terminar():
    global play
    global musica_tocando
    global lista_de_musicas
    global memoria_acoes
    global musicas_terminadas
    global lista_base

    if play and len(lista_de_musicas) > 1:
        terminada = lista_de_musicas.pop(0)
        musicas_terminadas.append(terminada)
        musica_tocando = lista_de_musicas[0]
       
        memoria_acoes = []
    elif play and len(lista_de_musicas) == 1:
        lista_de_musicas = lista_base.copy()
        musica_tocando = lista_de_musicas[0]
        
        musicas_terminadas = []
        memoria_acoes = []
#Finaliza o programa
def desligar():
    print("Jedi Wagner, assuma o comando!")
    
#Entrada:      
while not acabou:
    entrada = input().split()
    
    if len(entrada) > 1:
        acao = entrada[0]
        item = entrada[1]
        if acao == 'add':
            adicionar(item)
        elif acao == 'del':
            deletar(item)
        elif acao == 'next':
            next(item)
        elif acao == 'undo':
            desfazer(True)
        
    elif len(entrada) == 1:
        acao = entrada[0]
        if acao == 'play':
            turn_on()
        elif acao == 'stop':
            turn_off()
        elif acao == 'list':
            listar()
        elif acao == 'current':
            status()
        elif acao == 'ended':
            terminar()
        elif acao == 'undo':
            desfazer()
        elif acao == 'fight':
            desligar()
            acabou = True
            
