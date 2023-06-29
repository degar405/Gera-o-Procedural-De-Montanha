import bpy
import os
import sys
diretorioBase = os.path.dirname(bpy.data.filepath)
diretorioSrc = os.path.join(diretorioBase, "src")
diretorioData = os.path.join(diretorioBase, "data")
if diretorioSrc not in sys.path:
    sys.path.append(diretorioSrc)
    
from GeradorDeMontanha import GeradorDeMontanha

caminhoMapa = os.path.join(diretorioData, "mapa_exemplo.png")
caminhoInfo = os.path.join(diretorioData, "info_exemplo.txt")
geradorDeMontanha = GeradorDeMontanha(caminhoMapa, caminhoInfo)

matriz_vertices = geradorDeMontanha.gerarMontanha()

def transforma_matriz_em_vetor(matriz):
    vetor = []
    for i in range(0, len(matriz)):
        vetor.extend(matriz[i])
    
    return vetor

def cria_vetor_de_faces(matriz):
    quantidade_vetores_por_linha = len(matriz[0])
    vetor = []
    for i_eixo_y in range(1, len(matriz)):
        for i_eixo_x in range(1, quantidade_vetores_por_linha):
                indice_vetor_0 = ((i_eixo_y - 1) * quantidade_vetores_por_linha) + i_eixo_x - 1
                indice_vetor_1 = ((i_eixo_y - 1) * quantidade_vetores_por_linha) + i_eixo_x
                indice_vetor_2 = (i_eixo_y * quantidade_vetores_por_linha) + i_eixo_x - 1
                indice_vetor_3 = (i_eixo_y * quantidade_vetores_por_linha) + i_eixo_x
                
                vetor.append([indice_vetor_0, indice_vetor_1, indice_vetor_2])
                vetor.append([indice_vetor_1, indice_vetor_2, indice_vetor_3])
    return vetor

name = "Montanha"
mesh = bpy.data.meshes.new(name)
obj = bpy.data.objects.new(name, mesh)
col = bpy.data.collections[0]
col.objects.link(obj)
bpy.context.view_layer.objects.active = obj

vertices = transforma_matriz_em_vetor(matriz_vertices)

faces = cria_vetor_de_faces(matriz_vertices)

mesh.from_pydata(vertices, [], faces)