#!/usr/bin/env python
# -*- coding:utf-8 -*-

from Tkinter import *
from graphviz import Digraph
from Automate import Automate
global automate

class InterfaceGraphique(Frame):
	
	def __init__(self, fenetre, **kwargs):
		self.fromEtat = None
		self.trans = None
		self.toEtat = None
		self.alphabets = []
		self.transitions = []
		self.handlers = {}
		self.etatInitial = None
		self.etatsFinaux = []
		Frame.__init__(self, fenetre, width=768, height=476, **kwargs)
		#self.pack(fill=BOTH)

		self.texte = Label(fenetre, text="NFA-DFA-MINIMIZE")
		self.texte.pack()
		self.inputFrame = Frame(fenetre, width=768, height=300, borderwidth=1)
		self.inputFrame.pack(fill=X)
		self.outputFrame = Frame(fenetre, width=768, height=276, borderwidth=1)
		self.outputFrame.pack(fill=X)
		#self.inputTransitionFrame = Frame(inputFrame, widh
		self.selectAlphabet1 = Listbox(self.inputFrame)
		self.selectTransition = Listbox(self.inputFrame)
		self.selectAlphabet2 = Listbox(self.inputFrame)
		self.boutonAjouterTransition = Button(self.inputFrame, text="AjouterTransition", command=self.ajouterTransition)
		self.recupererEtat1 = Button(self.inputFrame, text="recuperer", command=self.recup1)
		self.recupererTrans = Button(self.inputFrame, text="recuperer", command=self.recup2)
		self.recupererEtat2 = Button(self.inputFrame, text="recuperer", command=self.recup3)
		self.boutonNFA = Button(self.inputFrame, text="NFA", command=self.NFA)
		self.boutonDFA = Button(self.inputFrame, text="DFA", command=self.DFA)
		self.boutonMinimize = Button(self.inputFrame, text="Minimize" ,command=self.Minimize)

		self.alphabetText = Label(self.inputFrame, text="Liste des alphabets")
		self.transitionsText = Label(self.inputFrame, text="Liste des transitions")
		self.texteAlphabets = StringVar()
		self.texteTransitions = StringVar()
		self.ligneAlphabets = Entry(self.inputFrame, textvariable=self.texteAlphabets, width=300)
		self.alphabetText.pack()
		self.ligneAlphabets.pack()
		self.ligneTransitions = Entry(self.inputFrame, textvariable=self.texteTransitions, width=300)
		self.transitionsText.pack()
		self.ligneTransitions.pack()
		self.boutonCreerAutomate = Button(self.inputFrame, text="Creer Automate", command=self.creerAutomate)
		self.boutonCreerAutomate.pack()
	
	def creerAutomate(self):
		global automate
		self.alphabets = self.ligneAlphabets.get().split(',')
		self.transitions = self.ligneTransitions.get().split(',')
		automate = Automate(self.alphabets,self.transitions)
		if len(self.alphabets) < 2 or len(self.transitions) < 1:
			erreur = Label(self.inputFrame, text="Vous devez entrez au moins deux états et une transition")
			erreur.pack()
		else:
			for elt in self.alphabets:
				self.selectAlphabet1.insert(END, str(elt))
			for elt in self.transitions:
				self.selectTransition.insert(END, str(elt))
			for elt in self.alphabets:
				self.selectAlphabet2.insert(END, str(elt))
			
			self.selectAlphabet1.pack()
			self.recupererEtat1.pack()
			self.selectTransition.pack()
			self.recupererTrans.pack()
			self.selectAlphabet2.pack()
			self.recupererEtat2.pack()
			self.boutonAjouterTransition.pack()

			self.boutonNFA.pack()
			self.boutonDFA.pack()
			self.boutonMinimize.pack()
	def recup1(self):
		self.fromEtat = str(self.selectAlphabet1.curselection())
	def recup2(self):
		self.trans = str(self.selectTransition.curselection())
	def recup3(self):
		self.toEtat = str(self.selectAlphabet2.curselection())
	def ajouterTransition(self):
		global automate
		key = (self.fromEtat, self.trans)
		if self.handlers.has_key((key)):
			Successeurs = self.handlers[key]
			if self.toEtat not in Successeurs:
				Successeurs.append(self.toEtat)
			self.handlers[key] = Successeurs
			automate.ajouterTransition(self.fromEtat, self.trans, Successeurs)
		
		else:
			self.handlers[key] = self.toEtat
			automate.ajouterTransition(self.fromEtat,self.trans,self.toEtat)
		
	def NFA(self):
		global automate
		automate.afficher()
	def DFA(self):
		global automate
		automate.determiniser()
		automate.afficherAFD()
	def Minimize(self):
		print("")
