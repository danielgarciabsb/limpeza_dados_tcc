#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import MySQLdb
from arquivo_csv import arquivoCSV

DEBUG = False #False ou True

csv = arquivoCSV(sys.argv[1])
if DEBUG:
    print csv.getAlunos()
    print csv.getHeader()
    print 'Ano sem referencia: ' + csv.getAnoRef()

db = MySQLdb.connect(host="localhost", user="root", passwd="", db="DADOS_ALUNOS_LICMAT")
cur = db.cursor()

def gerarInsert(aluno):
    query = 'INSERT INTO ALUNO VALUES (NULL,'
    for item in aluno:
        if item == '':
            query += 'NULL,'
        else:
            query += '"' + str(item) + '",'
    query += '"' + csv.getAnoRef() + '"'
    query += ')'
    return query

print '\n---\nINSERINDO DADOS NO BANCO DE DADOS\n---\n'
print 'Arquivo: ' + csv.getAnoRef() + '.csv'

num_aluno = 1

for aluno in csv.getAlunos():
    try:
        cur.execute(gerarInsert(aluno))
        db.commit()
        if DEBUG:
            print 'INSERINDO ALUNO: '+ str(num_aluno)
        num_aluno += 1
    except IOError, e:
        db.rollback()
        print 'ERRO!'
        print >> sys.stderr, e
        sys.exit()

if DEBUG:
    print 'ULTIMO INSERT:'
    print gerarInsert(csv.getAlunos()[len(csv.getAlunos()) - 1])
