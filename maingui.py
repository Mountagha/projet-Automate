#!/usr/bin/env python
#! -*- coding:utf-8 -*-

from Automate import Automate
from Tkinter import * 
from gui import InterfaceGraphique
#on crée une interface graphique minimale pour récupérer les input des utilisateurs et afficher les automates

#on crée notre fenêtre principale 
window = Tk()
interface = InterfaceGraphique(window)
interface.mainloop()
