'''
Created on 19/02/2013

@author: ilya
'''

import subprocess
import tempfile
import os
from nltk.parse.api import ParserI
from nltk.tree import Tree


class JohnsonCharniak(ParserI):


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
        basedir = "/mnt/hgfs/workspace/johnsoncharniak/reranking-parser/"
        modeldir = "second-stage/models/ec50spfinal/"
        estimatornickname = "cvlm-l1c10P1"
        features = modeldir + "/features.gz"
        weights = modeldir + estimatornickname + "-weights.gz"
        firststage = "first-stage/PARSE/parseIt"
        secondstage = "second-stage/programs/features/best-parses"
        datadir = "first-stage/DATA/EN/"
#        testfile = "sample-data.txt"
        argsfirst = [firststage, "-l399", "-N50", datadir, sentfilepath]
        argssecond = [secondstage, "-l", features, weights]
        os.chdir(basedir)
        p1 = subprocess.Popen(argsfirst, stdout=subprocess.PIPE)
        p2 = subprocess.Popen(argssecond, stdin=p1.stdout, stdout=subprocess.PIPE)
        p1.stdout.close()
        stdout, stderr = p2.communicate()
        return stdout
    