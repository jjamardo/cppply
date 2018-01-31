#!/usr/bin/python

from ply.lex import lex
from ply.yacc import yacc

from lexer_rules import *
from parser_rules import *

import sys, getopt

def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print('SLSParser.py -i <inputfile> -o <outputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('SLSParser.py -i <inputfile> -o <outputfile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   if(inputfile == '' or outputfile == ''):
      print('SLSParser.py -i <inputfile> -o <outputfile>')
      sys.exit()

   print('Archivo entrada: ' + inputfile)
   print('Archivo salida: ' + outputfile)

   with open(inputfile, 'r') as content_file:
      content = content_file.read()

   parser = yacc()
   lexer = lex()
   try:
      output = parser.parse(content, lexer)
   except TypeError as e:
      print("Error de tipo:\n\t" + str(e))
      sys.exit()
   except SyntaxError as e:
      print("Error de sintaxis:\n\t" + str(e))
      sys.exit()

   f = open(outputfile, 'w+')

   f.write(output.formatted_code)

if __name__ == "__main__":
   main(sys.argv[1:])