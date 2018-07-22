# Protein Secondary Structure Tools

Este repositório contém as ferramentas necessárias para obter e tratar dados de estrutura secundária de proteína para utilização em uma rede neuronal ou outro método de machine-learning. **O conteúdo aqui presente foi desenvolvido para fins didáticos**.

O script "psstools.py" contém as seguintes funções:

- **pss_down** -> executa o download e descompactação do arquivo presente em "https://cdn.rcsb.org/etl/kabschSander/ss.txt.gz", um arquivo com os dados de estruturas secundárias de proteínas obtidos experimentalmente, mantido pelo PDB;

- **pss_format** -> faz a leitura e formatação do arquivo de estrutura secundária formatado, que pode ser obtido pela função anterior. Ao executar a "format_ss" é gerado o arquivo "ss2.txt", que tem o formato necessário para rodar as funções posteriores;

- **pss_load** -> carrega os dados do arquivo formatado pela função anterior. As entradas são:
  - total_de_sequencias -> número de sequências a serem selecionadas. O padrão é 75;
  - tamanho_minimo -> tamanho mínimo para as sequências de entrada. O padrão é 17;
  - random_selection -> deve ser True ou False. Define se a seleção deve ser aleatório ou pela ordem no arquivo. O padrão é True;
  - ssForm_name -> arquivo em que as sequências serão buscadas. O padrão é o arquivo resultante da função anterior, no entanto é possível utilizar também o arquivo 'Ross_Saunder.txt', presente no repositório do git-hub também. O arquivo 'Ross_Saunder.txt' contém dados de estruturas tradicionalmente utilizadas para o aprendizado de máquina;

- **pss_align** -> faz o alinhamento entre duas estruturas secundárias colocadas como entrada. A ssp_align utiliza o script "SSEalign_psstools.pl", uma versão modificada do script "SSEalign_two_groups.pl", disponível em "https://github.com/yangzhiyuansibs/SSEalign". O método de alinhamento utilizado foi desenvolvido por Yang et al. (artigo disponível em: https://www.biorxiv.org/content/biorxiv/early/2017/10/10/200915.full.pdf);

Além disso, contém a classe **"PSSVect"**, responsável pela vetorização das estruturas secundárias e aminoácidos de proteínas. Os métodos de vetorização contidos na  classe são baseados no procedimento apresentado pela Mathwork em "https://www.mathworks.com/help/bioinfo/examples/predicting-protein-secondary-structure-using-a-neural-network.html".

A iniciação de um objeto com a classe "PSSVect" pode ser feita sem a inserção de nenhum argumento, uma vez que a única entrada dela ("tamanho_janela_movel") possuí um valor padrão definido. A entrada "tamanho_janela_movel", que tem por padrão o valor 17, é reponsável por especificar o tamanho da janela móvel, que será utilizada para percorrer as sequências no método de vetorização das estruturas secundárias e aminoácidos. Dentro da "PSSVect" existem os seguintes métodos:

- **pss2vect** -> vetoriza as estruturas secundárias;
- **aa2vect** -> vetoriza os aminoácidos correspondentes aos dados de estrutura secundária;
- **pss_prediction** -> a partir de uma rede neuronal treinada, faz a predição da estrutura secundária de uma sequência de aminoácidos. A primeira entrada é a sequência de aminoácidos. A segunda entrada é uma rede treinada pela MLPClassifier da biblioteca sklearn.neural_network (informações em: http://scikit-learn.org/stable/modules/neural_networks_supervised.html).

**O arquivo "psstools_MLP.ipynb" tem um exemplo de utilização da "psstools.py" para preparação dos dados e análise dos resultados de uma rede neuronal perceptron multicamadas.**

##em atualização##
