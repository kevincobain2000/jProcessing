#! /usr/bin/env python                                                        
# -*- coding: utf-8 -*-
import sys, subprocess, os
from subprocess import call
from tempfile import NamedTemporaryFile
"""
def cabocha_on_sparc(sent):
    if os.path.exists('/home_lab_local/s1010205/tmp/'):
        temp = NamedTemporaryFile(delete=False, dir='/home_lab_local/s1010205/tmp/')
    else:
        temp = NamedTemporaryFile(delete=False)
    temp.write(sent.encode('eucjp'))
    temp.close()
    #subprocess.call(['scp',temp.name,'taal:~/tmp/'+temp.name.split('/')[-1]])
    copy = ['scp',temp.name,'taal:~/tmp/'+temp.name.split('/')[-1]]
    subprocess.Popen(copy, stdout=subprocess.PIPE).communicate()[0]

    command = ['ssh','taal','cabocha', '-f','3 <', '~/tmp/'+temp.name.split('/')[-1]]
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    output = process.communicate()[0]
    remove_remote_temp = ['ssh','taal','rm','~/tmp/'+temp.name.split('/')[-1]]
    subprocess.Popen(remove_remote_temp, stdout=subprocess.PIPE).communicate()[0]
    os.unlink(temp.name)
    return unicode(output, 'eucjp')
"""
def cabocha(sent):
    if os.path.exists('/home_lab_local/s1010205/tmp/'):
        temp = NamedTemporaryFile(delete=False, dir='/home_lab_local/s1010205/tmp/')
    else:
        temp = NamedTemporaryFile(delete=False)
    temp.write(sent.encode('eucjp'))
    temp.close()
    command = ['cabocha', '-f','3 <', temp.name]
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    output = process.communicate()[0]
    os.unlink(temp.name)
    return unicode(output, 'eucjp')

def main():
    pass

if __name__ == '__main__':
    input_sentence = u'私は彼を５日前、つまりこの前の金曜日に駅で見かけた'
    #print cabocha(input_sentence).encode('utf-8')

    
    
    
