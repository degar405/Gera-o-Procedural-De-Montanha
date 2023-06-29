# Geração procedural de montanhas usando Python e Blender
Conjunto de scripts escritos em Python para uso no Blender que, a partir de um arquivo de imagem e de um arquivo de texto contendo informações, produzem o mesh de um terreno formado por uma montanha simples e o seu entorno.

![Mapa de exemplo](https://github.com/degar405/Gera-o-Procedural-De-Montanha/assets/46822609/1fce21a7-0991-4da2-8053-04bb0e2cebcf) ![Terreno gerado](https://github.com/degar405/Gera-o-Procedural-De-Montanha/assets/46822609/493ddc24-15f4-4afb-a1b2-02aa82dcaa95)

Exemplo de terreno gerado com a ferramenta.

É necessária a instalação da biblioteca [scikit-image](https://scikit-image.org/).
## Parâmetros de entrada
O terreno é formado a partir de um mapa como o da imagem acima, à esquerda, com um fundo branco, o topo na cor preta e a base da montanha numa cor qualquer diferente destas duas, e por um arquivo de texto contendo parâmetros para a construção do mesh. Cada um desses parâmetros é um número inteiro que ocupa uma linha, são eles: a quantidade *n* de pixels por lado do vértice (cada vértice agrupa *n***n* pixels), a altura do topo, a altura da base e a taxa de ruído nesta ordem.
