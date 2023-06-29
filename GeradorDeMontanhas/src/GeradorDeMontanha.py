from Reta import Reta
from Enumeradores import PontosCardeais, Posicionamento
from FormatacaoDados import obterDadosFormatados
import random

class GeradorDeMontanha:
    def __init__(self, caminhoMapa, caminhoInfo):
        (dimensoesTerreno, topo, verticesBase, alturaTopo, alturaBase, distanciaVertices, taxaRuido) = obterDadosFormatados(caminhoMapa, caminhoInfo)
        self.dimensoesTerreno = dimensoesTerreno
        self.topo = topo
        self.verticesBase = verticesBase
        self.alturaTopo = alturaTopo
        self.alturaBase = alturaBase
        self.distanciaVertices = distanciaVertices
        self.taxaRuido = taxaRuido
        self.retas = []
        self.criarRetas()

    def criarRetas(self):
        (x0, y0) = self.topo

        pontosReta = [0, 0, 0, 0]
        for ponto in self.verticesBase:
            (x1, y1) = ponto
            if x1 == x0:
                if y1 < y0 and pontosReta[PontosCardeais.Norte] == 0:
                    pontosReta[PontosCardeais.Norte] = ponto
                if y1 > y0 and pontosReta[PontosCardeais.Sul] == 0:
                    pontosReta[PontosCardeais.Sul] = ponto
            if y1 == y0:
                if x1 > x0 and pontosReta[PontosCardeais.Leste] == 0:
                    pontosReta[PontosCardeais.Leste] = ponto
                if x1 < x0 and pontosReta[PontosCardeais.Oeste] == 0:
                    pontosReta[PontosCardeais.Oeste] = ponto

        origem = (x0, y0, self.alturaTopo)

        for (x1, y1) in pontosReta:
            p1 = (x1, y1, self.alturaBase)
            reta = Reta(origem, p1)
            self.retas.append(reta)

    def gerarMontanha(self):
        (qtdLinhas, qtdColunas) = self.dimensoesTerreno
        meshTerreno = []
        for nLinha in range (0, qtdLinhas): # y
            linha = []
            for nColuna in range(0, qtdColunas): # x
                vertice = self.criarVertice(nColuna, nLinha)
                linha.append(vertice)
            meshTerreno.append(linha)
        return meshTerreno

    def criarVertice(self, x, y):
        alturaCalculada = -1
        posicionamentoVertice = self.obterPosicionamentoVertice(x, y)
        
        if posicionamentoVertice == Posicionamento.Topo:
            alturaCalculada = self.alturaTopo
        elif posicionamentoVertice == Posicionamento.Base or posicionamentoVertice == Posicionamento.EntornoMontanha:
            alturaCalculada = self.alturaBase
        elif posicionamentoVertice == Posicionamento.Reta:
            alturaCalculada = self.calcularAlturaVerticePosicionadoNaReta(x, y)
        else:
            alturaCalculada = self.calcularAlturaVerticeEntreRetas(x, y)

        z = self.aplicarRuido(alturaCalculada, posicionamentoVertice)
        
        return [x * self.distanciaVertices, y * self.distanciaVertices, z]
    
    def obterPosicionamentoVertice(self, x, y):
        (xTopo, yTopo) = self.topo

        if xTopo == x and yTopo == y:
            return Posicionamento.Topo
        
        if self.verticesBase.count((x, y)) > 0:
            return Posicionamento.Base
        
        existeVBase = [False, False, False, False]
        for (xVerticeBase, yVerticeBase) in self.verticesBase:
            if xVerticeBase == x:
                if yVerticeBase < y:
                    existeVBase[PontosCardeais.Norte] = True
                else:
                    existeVBase[PontosCardeais.Sul] = True
            if yVerticeBase == y:
                if xVerticeBase > x:
                    existeVBase[PontosCardeais.Leste] = True
                else:
                    existeVBase[PontosCardeais.Oeste] = True

            if existeVBase[PontosCardeais.Norte] and existeVBase[PontosCardeais.Sul] and existeVBase[PontosCardeais.Leste] and existeVBase[PontosCardeais.Oeste]:
                if xTopo == x or yTopo == y:
                    return Posicionamento.Reta
                return Posicionamento.Montanha
            
        return Posicionamento.EntornoMontanha
    
    def calcularAlturaVerticePosicionadoNaReta(self, x, y):
        (xTopo, yTopo) = self.topo
        indiceRetaOposta = -1
        if xTopo == x:
            if yTopo > y:
                indiceRetaOposta = PontosCardeais.Sul
            else:
                indiceRetaOposta = PontosCardeais.Norte
        else:
            if xTopo < x:
                indiceRetaOposta = PontosCardeais.Oeste
            else:
                indiceRetaOposta = PontosCardeais.Leste

        alturaVertice = 0

        for i in range(0, len(self.retas)):
            if i != indiceRetaOposta:
                alturaVertice += self.retas[i].calcularZaPartirDaDistancia(x, y) 

        alturaVertice = alturaVertice/3

        return alturaVertice       
        
    def calcularAlturaVerticeEntreRetas(self, x, y):
        (xTopo, yTopo) = self.topo
        indiceRetaNS = PontosCardeais.Norte if yTopo > y else PontosCardeais.Sul
        indiceRetaLO = PontosCardeais.Leste if xTopo < x else PontosCardeais.Oeste

        alturaCalculadaNS = self.retas[indiceRetaNS].calcularZaPartirDaDistancia(x, y)
        alturaCalculadaLO = self.retas[indiceRetaLO].calcularZaPartirDaDistancia(x, y)

        return (alturaCalculadaNS + alturaCalculadaLO)/2
    
    def aplicarRuido(self, alturaCalculada, posicionamentoVertice):
        parametroRuido = self.taxaRuido * abs(self.alturaTopo - self.alturaBase)/100
        if (posicionamentoVertice == Posicionamento.Montanha or posicionamentoVertice == Posicionamento.Reta) and alturaCalculada < self.alturaBase:
            alturaCalculada = alturaCalculada + parametroRuido
        mode = 0
        if posicionamentoVertice == Posicionamento.EntornoMontanha or posicionamentoVertice == Posicionamento.Base:
            parametroRuido = 20 * parametroRuido / 100 if random.random() < 0.5 else 0
            mode = parametroRuido / 100
        else:
            mode = parametroRuido / 2

        ruido = random.triangular(0, parametroRuido, mode)
        ruido = ruido if random.random() < 0.5 else -1 * ruido
        return alturaCalculada + ruido