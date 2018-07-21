# predicao-de-estrutura-secundaria-de-proteinas-usando-rede-neuronal

Este repositório contém as ferramentas necessárias para obter e tratar dados de estrutura secundária de proteína para utilização em uma rede neuronal ou outro método de machine-learning.

O script "psstools.py" contém as seguintes funções:

down_ss -> executa o download e descompactação do arquivo presente em "https://cdn.rcsb.org/etl/kabschSander/ss.txt.gz", um arquivo com os dados de estruturas secundárias de proteínas obtidos experimentalmente, mantido pelo PDB;
format_ss -> faz a leitura e formatação do arquivo "ss.txt", obtido pela função anterior. Ao executar a "format_ss" é gerado o arquivo "ss2.txt", que tem o formato necessário para rodar as funções posteriores.

##em atualiuzação##
