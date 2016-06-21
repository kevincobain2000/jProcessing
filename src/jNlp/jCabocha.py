#! /usr/bin/env python                                                        
# -*- coding: utf-8 -*-
import sys, subprocess, os
from subprocess import call
from tempfile import NamedTemporaryFile

def formdamage(sent):
    rectify = []
    for ch in sent:
        try: rectify.append(ch.encode('utf-8'))
        except: pass
    return ''.join(rectify)
        
def cabocha(sent):
    if os.path.exists('/home_lab_local/s1010205/tmp/'):
        temp = NamedTemporaryFile(delete=False, dir='/home_lab_local/s1010205/tmp/')
    else:
        temp = NamedTemporaryFile(delete=False)
    try: sent = sent.encode('utf-8')
    except: sent = formdamage(sent)
    temp.write(sent)
    temp.close()
    command = ['cabocha', '-f', '3']
    process = subprocess.Popen(command, stdin=open(temp.name,'r'), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    os.unlink(temp.name)
    return unicode(output, 'utf-8')

def main():
    pass

if __name__ == '__main__':
    input_sentence = u'私が五年前にこの団体を仲間たちと結成したのはマルコス疑惑などで日本のＯＤＡ（政府開発援助）が問題になり、国まかせでなく、民間による国際協力が必要だと痛感したのが大きな理由です。'
    print cabocha(input_sentence).encode('utf-8')


    
    
    
