# Predição de Estrutura Secundária de Proteínas Usando Rede Neuronal

Este repositório contém as ferramentas necessárias para obter e tratar dados de estrutura secundária de proteína para utilização em uma rede neuronal ou outro método de machine-learning.

O script "psstools.py" contém as seguintes funções:

- down_ss -> executa o download e descompactação do arquivo presente em "https://cdn.rcsb.org/etl/kabschSander/ss.txt.gz", um arquivo com os dados de estruturas secundárias de proteínas obtidos experimentalmente, mantido pelo PDB;

- format_ss -> faz a leitura e formatação do arquivo "ss.txt", obtido pela função anterior. Ao executar a "format_ss" é gerado o arquivo "ss2.txt", que tem o formato necessário para rodar as funções posteriores.

Além disso, contém a classe "PSSVect", responsável pela vetorização das estruturas secundárias e aminoácidos de proteínas. Os métodos de vetorização contidos na  classe são baseados no procedimento apresentado pela Mathwork em "https://www.mathworks.com/help/bioinfo/examples/predicting-protein-secondary-structure-using-a-neural-network.html".

A iniciação de um objeto com a classe "PSSVect" pode ser feita sem a inserção de nenhum argumento, uma vez que a única entrada dela ("tamanho_janela_movel") possuí um valor padrão definido. A entrada "tamanho_janela_movel", que tem por padrão o valor 17, é reponsável por especificar o tamanho da janela móvel, que será utilizada para percorrer as sequências no método de vetorização das estruturas secundárias e aminoácidos.

##em atualização##
