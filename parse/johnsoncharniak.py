'''
Created on 19/02/2013

@author: ilya
'''

import subprocess
import tempfile
import os
import ConfigParser
from nltk.parse.api import ParserI
from nltk.tree import Tree


class JohnsonCharniak(ParserI):


    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read('nltk/parse/johnsoncharniak.ini')
        section = 'Paths'
        modeldir = config.get(section, 'modeldir')
        estimatornickname = config.get(section, 'estimatornickname')
        self.basedir = config.get(section, 'basedir')
        self.features = modeldir + config.get(section, 'features-file')
        self.weights = modeldir + estimatornickname + config.get(section, 'weights-suffix')
        self.firststage = config.get(section, 'firststage')
        self.secondstage = config.get(section, 'secondstage')
        self.datadir = config.get(section, 'datadir')
        

    def parse(self, sent):
        sentfilepath  = self.sent_to_temp(sent)
        jc_parse_string = self.jc_parse(sentfilepath)
        os.remove(sentfilepath)
        return Tree.parse(jc_parse_string)
        
        
    def sent_to_temp(self, sent):
        sentstring = "<s> %s </s>" % ' '.join(sent)
        sentfile = tempfile.NamedTemporaryFile('w', delete=False)
        sentfile.write(sentstring)
        sentfilepath = os.path.abspath(sentfile.name)
        sentfile.close()
        return sentfilepath
    
    
    def jc_parse(self, sentfilepath):
        argsfirst = [self.firststage, "-l399", "-N50", self.datadir, sentfilepath]
        argssecond = [self.secondstage, "-l", self.features, self.weights]
        os.chdir(self.basedir)
        p1 = subprocess.Popen(argsfirst, stdout=subprocess.PIPE)
        p2 = subprocess.Popen(argssecond, stdin=p1.stdout, stdout=subprocess.PIPE)
        p1.stdout.close()
        stdout, stderr = p2.communicate()
        return stdout
    