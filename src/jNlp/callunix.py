#! /usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
from subprocess import call
def _checklist(argument):
    if not type(argument) is list:
        return argument.split()
    else: return argument

def shell_out(command):
    command = _checklist(command)
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    return process.communicate()[0]

def shell_call(command):
    command = _checklist(command)
    subprocess.Popen(command, stdout=subprocess.PIPE)
    return ''
    
    
