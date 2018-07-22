# coding: utf-8

import re
import numpy as np
import pandas as pd
from scipy.linalg import hankel
import urllib.request
import gzip
import shutil
import math
import os
import random
import shutil


class PSSVect:
    def __init__(self, tamanho_janela_movel=17):
        self.tamanho_janela_movel = tamanho_janela_movel

    def aa2vect(self,aa):
        aa_dict = {'A':0,'R':1,'N':2,'D':3,'B':4,'C':5,'E':6,'Q':7,'Z':8,'G':9,
            'H':10,'I':11,'L':12,'K':13,'M':14,'F':15,'P':16,'S':17,'T':18,
            'W':19,'Y':20,'V':21,'?':22}
        aa_num=[]
        for i,w in enumerate(aa):
            aa_num.append(np.array([aa_dict.get(x) for x in aa[i]]))

        base_indexador = np.arange(self.tamanho_janela_movel)*23
        self.sequencias = []
        total_de_sequencias=len(aa)
        for i in range (0,total_de_sequencias): #para % cada sequencia
            seq = aa_num[i] #obter sequencia atual
            janelas = hankel(seq[:self.tamanho_janela_movel],seq[self.tamanho_janela_movel-1:]) #obter todas as janelas moveis para a sequencia, cada coluna forma uma
            #print (i)
            #23 colunas para cada janela; uma linha  para cada janela:
            matriz_binaria=np.full((np.size(janelas,1),23*self.tamanho_janela_movel), False, dtype=float)    
            for k in range (0,np.size(janelas,1)): #para cada janela movel, ou seja, cada coluna
                #print(k)
                indexador = np.array(base_indexador + janelas[:,k])
                matriz_binaria[k,indexador] = True #marca como True o valor de cada posição
            for j in matriz_binaria:
                self.sequencias.append(j)
        return self.sequencias

    def pss2vect(self,ss):
        dssp_dict = {'C':0,'E':1,'H':2}
        ss_num=[]
        for i,w in enumerate(ss):
            ss_num.append(np.array([dssp_dict.get(x) for x in ss[i]]))

        residuo_central = math.ceil(self.tamanho_janela_movel/2) #central residue position
        self.estruturas=[]
        total_de_sequencias=len(ss)
        for i in range (0,total_de_sequencias):
            #print(i)
            estrutura = ss_num[i] #obter a estrutura
            janelas = hankel(estrutura[:self.tamanho_janela_movel],estrutura[self.tamanho_janela_movel-1:])
            matriz_binaria = np.full((3,np.size(janelas,1)), False, dtype=float)
            matriz_binaria[0]=janelas[residuo_central]==0 #C
            matriz_binaria[1]=janelas[residuo_central]==1 #E
            matriz_binaria[2]=janelas[residuo_central]==2 #H

            for j in matriz_binaria.T:
                self.estruturas.append(j)
        return self.estruturas

    def pss_prediction(self,seq,mlp):
        vect = self.aa2vect(seq)
        predictions = mlp.predict(vect)
        self.ss_predic=''
        
        #inserir Cs nas primeirs posições:
        aa_num = math.ceil((self.tamanho_janela_movel/2))
        newaa='C'
        self.ss_predic=(self.ss_predic+newaa*aa_num)
        
        #inserir SSEs com base na predição da rede
        for i in predictions:
            if i[0]==1:
                newaa='C'
            elif i[1]==1:
                newaa='E'
            elif i[2]==1:
                newaa='H'
            else:   
                newaa='C'
            self.ss_predic=(self.ss_predic+newaa)
                
        #inserir Cs nas últimas posições:
        aa_num = math.ceil((self.tamanho_janela_movel/2))
        newaa='C'
        if self.tamanho_janela_movel % 2 == 0:
            aa_num = math.ceil(self.tamanho_janela_movel/2)-1
        else:
            aa_num = math.ceil((self.tamanho_janela_movel/2))-2
        self.ss_predic=(self.ss_predic+newaa*aa_num)
        
        return self.ss_predic

def pss_down():
    urllib.request.urlretrieve ("https://cdn.rcsb.org/etl/kabschSander/ss.txt.gz", "ss.txt.gz")
    with gzip.open('ss.txt.gz', 'rb') as f_in:
        with open('ss.txt', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

#função para formatar os dados do arquivo ss do PDB (https://www.rcsb.org/pdb/static.do?p=download/http/index.html)
def pss_format():
    ss_name='ss.txt'
    ssForm_name='ss2.txt'
    file = open (ss_name,'r')
    out = open (ssForm_name,'w')
    verificador = 0
    amino = ''
    estrut = ''
    for i in file:
        i = re.sub('\n','',i)
        if re.search('>',i):
            if verificador == 2:
                verificador = 1
                out.write (amino+','+estrut+'\n')
                amino = ''
                estrut = ''
            else:
                s=re.split('>|:',i)
                #name=(s[1]+':'+s[2])
                verificador += 1
        elif verificador == 1:
            i = re.sub('[^ARNDBCEQZGHILKMFPSTWYV]','?',i) #https://molbiol-tools.ca/Amino_acid_abbreviations.htm
            amino=amino+i
        elif verificador == 2:
            i = re.sub('\s|S|T','C',i)
            i = re.sub('G|I','H',i)
            i = re.sub('B','E',i)
            estrut=estrut+i
    out.write (amino+','+estrut+'\n')
    file.close()
    out.close()

#função para carregar os dados do arquivo ss formatado
def pss_load(total_de_sequencias=75,tamanho_minimo = 17,random_selection=True,ssForm_name='ss2.txt'):
    #total_de_sequencias recebe o número de sequência que serão carregadas
    #tamanho_minimo recebe o número mínimo de aminoácidos para aceitar uma sequência
    #ssForm_name='ss2.txt'
    file = open (ssForm_name,'r')
    aa_total=[]
    ss_total=[]
    c=0
    for i in file:
        i=re.sub('\n','',i)
        s=re.split(',',i)
        if len(s[0]) >= tamanho_minimo:
            aa_total.append(s[0])
            ss_total.append(s[1])
            c+=1
        if c == total_de_sequencias and random_selection == False:
            return aa_total,ss_total
    index = random.sample(range(0, c), total_de_sequencias)
    aa=[]
    ss=[]
    for i in index:
        aa.append(aa_total[i])
        ss.append(ss_total[i])
    return aa,ss
    
def pss_hitRate (ss_real,ss_predic):
    pont=0
    for i,w in enumerate(ss_predic):
        if ss_predic[i] == ss_real[i]:
            pont+=1
    return pont/len(ss_predic)*100
    
def pss_align (query,subject):
    try: 
        os.mkdir('tmp')
    except:
        pass
    query=query.upper()
    subject=subject.upper()
    query_file = open ('tmp/temp_ss_align_query','w')
    query_file.write('>query\n')
    for i in query:
        query_file.write(i)
    query_file.close()
    subject_file = open ('tmp/temp_ss_align_subject','w')
    subject_file.write('>subject\n')
    for i in subject:
        subject_file.write(i)
    subject_file.close()
    result=os.popen('perl SSEalign_psstools.pl tmp/temp_ss_align_query tmp/temp_ss_align_subject').read()
    shutil.rmtree('tmp')
    return result
