from skimage import io

def determinarPreenchimentoQuadrante(mapa, linha, coluna, razaoPixelVertice):
    valorVertice = -1
    topoEncontrado = False
    for i in range(razaoPixelVertice * linha, razaoPixelVertice * (linha + 1)):
        if topoEncontrado:
            break
        for o in range(razaoPixelVertice * coluna, razaoPixelVertice * (coluna + 1)):
            [r, g, b] = mapa[i,o]
            if r != 255 or g != 255 or b != 255:
                if r == 0 and g == 0 and b == 0:
                    valorVertice = 1
                    topoEncontrado = True
                    break
                else:
                    valorVertice = 0
    return valorVertice

def obterInformacoesMapa(caminhoInfo):
    arquivoInfo = open(caminhoInfo, "r")
    linhasInfo = arquivoInfo.readlines()
    arquivoInfo.close()

    razaoPixelVertice = int(linhasInfo[0])
    valorTopo = int(linhasInfo[1])
    valorBase = int(linhasInfo[2])
    taxaRuido = int(linhasInfo[3])
    return (razaoPixelVertice, valorTopo, valorBase, taxaRuido)

def obterDadosFormatados(enderecoMapa, enderecoInfo):
    (razaoPixelVertice, alturaTopo, alturaBase, taxaRuido) = obterInformacoesMapa(enderecoInfo)

    mapa = io.imread(enderecoMapa)
    larguraMapa = len(mapa[0])
    alturaMapa = len(mapa)

    larguraTerreno = int(larguraMapa/razaoPixelVertice)
    alturaTerreno = int(alturaMapa/razaoPixelVertice)

    verticesBase = []
    topo = (-1, -1)
    centroEncontrado = False
    for linha in range(0, alturaTerreno):
        for coluna in range(0, larguraTerreno):
            preenchimentoQuadrante = determinarPreenchimentoQuadrante(mapa, linha, coluna, razaoPixelVertice)
            if preenchimentoQuadrante == 1 and not centroEncontrado:
                topo = (coluna, linha)
                centroEncontrado = True
            if preenchimentoQuadrante == 0:
                verticesBase.append((coluna, linha))
    
    dimensoesTerreno = (alturaTerreno, larguraTerreno)
    return (dimensoesTerreno, topo, verticesBase, alturaTopo, alturaBase, razaoPixelVertice, taxaRuido)