#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import md5
from unicodedata import normalize

DEBUG = False #False ou True

class arquivoCSV(object):
    """Classe para tratar o arquivo CSV"""

    # Indices dos atributos a serem removidos
    remover = [2,7,9,10,11,12,15,19,40,68]

    def __init__(self, arquivo):
        try:
            self.arquivo = open(arquivo, 'rb')
        except IOError, e:
            print >> sys.stderr, e
            sys.exit()
        self.__readAllFile()

    def __del__(self):
        self.arquivo.close()

    def __readLine(self):
        try:
            line = self.arquivo.readline()
        except IOError, e:
            print >> sys.stderr, e
            sys.exit()

        line = line.rstrip('\r\n')
        line = line.decode('unicode_escape')
        line = self.normalizarNome(line)
        line = line.split(';')
        return line

    def __readHeader(self):
        self.header = []
        for attr in self.__readLine():
            if attr.upper() == 'CAMPO_NAO_INDICADO':
                attr = 'CIDADE'
            if attr.upper() == 'ANO(DATA)':
                attr = 'ANO_DATA'
            if not attr.upper().find('CODDISC'):
                self.ano_referencia = attr.upper().split('CODDISC')[1]
                attr = 'COD_DISCIPLINA'
            if not attr.upper().find('MENCAO'):
                attr = 'MENCAO'
            if not attr.upper().find('NOME_DISCIPLINA'):
                attr = 'NOME_DISCIPLINA'
            self.header.append(attr.upper())
        self.header.append('ANO_SEM_REFERENCIA')
        self.__removeAttributes(self.header)

    def __readAlunos(self):
        self.alunos = []
        while True:
            line = self.__readLine()
            if line != ['']:
                self.__removeAttributes(line)
                self.__hideSensitive(line)
                self.alunos.append(line)
            else:
                break

    def __removeAttributes(self, source):
        c = 0
        for i in self.remover:
            index = int(i - c)
            if DEBUG:
                print 'Removendo atributo: ' + source[index] + '[' + str(i) + ']'
            del source[index]
            c += 1

    def __hideSensitive(self, source):
        matricula = md5.new()
        matricula.update(source[0])
        source[0] = matricula.hexdigest()
        source[3] = source[3].split('/')[2]
        if source[1].upper() == 'Masculino'.upper():
            source[1] = 'M'
        else:
            source[1] = 'F'

    def __readAllFile(self):
        self.arquivo.seek(0)
        self.__readHeader()
        self.__readAlunos()

    def normalizarNome(self, source):
        source = source.rstrip()
        source = source.replace('-','_')
        source = source.replace(',','_')
        source = source.replace(' ','_')
        source = source.replace('.','_')
        source = source.replace('___','_')
        source = source.replace('__','_')
        return normalize('NFKD', source).encode('ASCII','ignore')

    def getAnoRef(self):
        return self.ano_referencia

    def getAlunos(self):
        return self.alunos

    def getHeader(self):
        return self.header

def test():
    csv = arquivoCSV(sys.argv[1])
    print csv.getAlunos()
    print csv.getHeader()

    print 'Quantidade de atributos: %d' % (len(csv.getHeader()) + 1)
    print 'Quantidade de alunos: %d' % len(csv.getAlunos())

    print 'Verificando a consistencia (quantidade de atributos) de cada aluno...'

    erro = 0
    for aluno in csv.getAlunos():
        if len(aluno) + 1 != len(csv.getHeader()):
            print 'Um erro ocorreu! len(aluno) != len(csv.getHeader())!'
            print aluno
            erro = 1

    if erro == 0:
        print 'Todos alunos foram verificados com sucesso!'
    else:
        print 'Erros foram encontrados ao verificar a consistencia de dados dos alunos'

if DEBUG:
    test()
