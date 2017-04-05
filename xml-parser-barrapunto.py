#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Simple XML parser for the RSS channel from BarraPunto
# Jesus M. Gonzalez-Barahona
# jgb @ gsyc.es
# TSAI and SAT subjects (Universidad Rey Juan Carlos)
# September 2009
#
# Just prints the news (and urls) in BarraPunto.com,
#  after reading the corresponding RSS channel.

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
import urllib2


# Para ejecutarlo:
# python2.7 xml-parser-barrapunto.py >barrapunto.html
# lo ultimo es para que la salida estandar la guarde
# en un fichero

class myContentHandler(ContentHandler):

    def __init__(self):
        self.inItem = False
        self.inContent = False
        self.theContent = ""

    def startElement(self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.inContent = True

    def endElement(self, name):
        if name == 'item':
            self.inItem = False
        elif self.inItem:
            if name == 'title':
                line = "<p>Title: " + self.theContent + ".</p>"
                # To avoid Unicode trouble
                print line.encode('utf-8')
                self.inContent = False
                self.theContent = ""
            elif name == 'link':
                print "Link: " + "<a href=" + self.theContent + ">" + self.theContent + "</a>"
                self.inContent = False
                self.theContent = ""

    def characters(self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars
# --- Main prog
# Load parser and driver

theParser = make_parser()
theHandler = myContentHandler()
theParser.setContentHandler(theHandler)

# Ready, set, go!
url = "http://barrapunto.com/index.rss"
f = urllib2.urlopen(url)
html = f.read().decode("utf-8")  # esto es la html de la pag
# Creamos el fichero donde se guarde el html de URL (ENTERO)
outfile = open('prueba.txt', 'w')  # Indicamos el valor 'w'.
outfile.write(html)
outfile.close()
# Abrir el fichero para hacer el parse de HTML
xmlFile = open('prueba.txt', "r")
theParser.parse(xmlFile)

print "Parse complete"
