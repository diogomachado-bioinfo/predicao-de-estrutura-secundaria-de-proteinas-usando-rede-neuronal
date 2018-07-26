# Protein Secondary Structure Tools

Este repositório contém as ferramentas necessárias para obter e tratar dados de estrutura secundária de proteína para utilização em uma rede neuronal ou outro método de machine-learning. **O conteúdo aqui presente foi desenvolvido para fins didáticos**.

O script "psstools.py" contém as seguintes funções:

**OBS.: Para utilizar as funções execute: from psstools import \***

- **pss_down** -> executa o download e descompactação do arquivo presente em "https://cdn.rcsb.org/etl/kabschSander/ss.txt.gz", um arquivo com os dados de estruturas secundárias de proteínas obtidos experimentalmente, mantido pelo PDB. **Exemplo de execução: pss_down()**;

- **pss_format** -> faz a leitura e formatação do arquivo de estrutura secundária formatado, que pode ser obtido pela função anterior. Ao executar a "format_ss" é gerado o arquivo "ss2.txt", que tem o formato necessário para rodar as funções posteriores. **Exemplo de execução: pss_format()**;

- **pss_load** -> carrega os dados do arquivo formatado pela função anterior. As entradas são:
  - total_de_sequencias -> número de sequências a serem selecionadas. O padrão é 75;
  - tamanho_minimo -> tamanho mínimo para as sequências de entrada. O padrão é 17;
  - random_selection -> deve ser True ou False. Define se a seleção deve ser aleatório ou pela ordem no arquivo. O padrão é True;
  - ssForm_name -> arquivo em que as sequências serão buscadas. O padrão é o arquivo resultante da função anterior, no entanto é possível utilizar também o arquivo 'Ross_Saunder.txt', presente no repositório do git-hub também. O arquivo 'Ross_Saunder.txt' contém 75 dados de sequências de estruturas tradicionalmente utilizadas para o aprendizado de máquina;
  - **Exemplo de execução: randon_pss = pss_load (total_de_sequencias = 125, tamanho_minimo = 100, random_selection = False, ssForm_name = 'ss2.txt')**; Ao executar esse exemplo 'randon_pss[0]' recebe os aminoácidos e 'randon_pss[1]' as estruturas secundárias;
  - **OBS.: É possível concatenar matrizes geradas com a pass_load usando: "dataset_pss=np.concatenate((matriz_1, matriz_2), axis=1)", sendo que 'dataset_pss' recebe os dados de matriz_1 e matriz_2 concatenados**

- **pss_align** -> faz o alinhamento entre duas estruturas secundárias colocadas como entrada. A ssp_align utiliza o script "SSEalign_psstools.pl", uma versão modificada do script "SSEalign_two_groups.pl", disponível em "https://github.com/yangzhiyuansibs/SSEalign". O método de alinhamento utilizado foi desenvolvido por Yang et al. (artigo disponível em: https://www.biorxiv.org/content/biorxiv/early/2017/10/10/200915.full.pdf). **Exemplo de execução: 'pss_align(pss1,pss2)', sendo pss1 e pss2 representações de estruturas secundárias de proteínas no formato de string**;

As funções a seguir foram baseadas no procedimento apresentado pela Mathwork em "https://www.mathworks.com/help/bioinfo/examples/predicting-protein-secondary-structure-using-a-neural-network.html".

- **pss2vect** -> vetoriza as estruturas secundárias. **Exemplo de execução: 'ss_vect = pss2vect(randon_pss[1])', onde 'ss_vect' recebe os dados de 'randon_pss[1]' vetorizados**;

- **aa2vect** -> vetoriza os aminoácidos correspondentes aos dados de estrutura secundária. **Exemplo de execução: 'aa_vect = aa2vect(randon_pss[0])', onde 'aa_vect' recebe os dados de 'randon_pss[0]' vetorizados**;

- **pss_prediction** -> a partir de uma rede neuronal treinada, faz a predição da estrutura secundária de uma sequência de aminoácidos. A primeira entrada é a sequência de aminoácidos. A segunda entrada é uma rede treinada pela MLPClassifier da biblioteca sklearn.neural_network (informações em: http://scikit-learn.org/stable/modules/neural_networks_supervised.html). **Exemplo de execução: 'predita1=pss_prediction(seq1,mlp)', onde 'seq1' é uma sequência de aminoácidos em formato de string e mlp é uma rede treinada**;

------------------------------------------------------------------------------

# COMO TREINAR A REDE?

**Exemplo de pipeline para treinamento de rede neuronal MLP com python:**
  - from sklearn.neural_network import MLPClassifier #importando da biblioteca sklearn a ferramenta de MLP
  - mlp = MLPClassifier(hidden_layer_sizes=(10,10,10),max_iter=100,learning_rate_init=0.01,momentum=1,activation='relu')     #criando a rede
  - mlp.fit(x_train,y_train) #treinando a rede, sendo x_train os atributos e y_train os rótulos

**Pode ser optado por alocar parte do conjunto para teste:**
  - from sklearn.model_selection import train_test_split #importar as dependências
  - x=np.array(x) #preparar dados para as funções posteriores
  - y=np.array(y) #preparar dados para as funções posteriores
  - x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.10) #separar 10% de x e y para teste
  - print ('Conjunto para treino: ',len(x_train)) #exibir tamanho do conjunto reservado para treino
  - print ('Conjunto para teste: ',len(x_test)) #exibir tamanho do conjunto reservado para teste

**Se optado por alocar o conjunto de testes, é possível fazer a predição do conjunto de teste e executar as funções de métrica para verificar os acertos:**
  - predictions = mlp.predict(x_test) #faz a predição para os valores no conjunto de testes
  - from sklearn.metrics import confusion_matrix,classification_report,accuracy_score #importa as dependências para as métricas
  - print(classification_report(y_test,predictions,target_names=['C','E','H']),'\n') #exibe tabela com os resultados
  - acuracia = accuracy_score(y_test, predictions) #calcula acurácia
  - print('Acurácia: ',acuracia,'\n') #exibe acurácia
  - pd.DataFrame(confusion_matrix(y_test.astype(int).argmax(axis=1), predictions.argmax(axis=1))) #exibe matriz de confusão

------------------------------------------------------------------------------

**O arquivo "psstools_MLP.ipynb" tem um exemplo de utilização da "psstools.py" para preparação dos dados e análise dos resultados de uma rede neuronal perceptron multicamadas.**

No link "https://docs.google.com/presentation/d/1AWHLiiD0_tLBXpGButXjAvTlrUHGzcOHzgyHmBOnD04/edit?usp=sharing" há o arquivo de uma apresentação introdutória sobre proteínas, redes neuronais e predição de estruturas secundárias de proteínas. 

##em atualização##
