#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 19:48:44 2026

@author: tercio
"""

import os
import re

pasta = "data"

sujeitos = set()

for arquivo in os.listdir(pasta):
    match = re.search(r"suj(\d+)", arquivo)
    if match:
        sujeitos.add(match.group(1))

print("Número de sujeitos:", len(sujeitos))
print("Sujeitos encontrados:", sorted(sujeitos))