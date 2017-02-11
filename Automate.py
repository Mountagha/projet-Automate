#!/usr/bin/env python
# -*-  coding:utf-8 -*-

from graphviz import Digraph

class Automate:

	def __init__(self, listeAlphabets, listeTransitions):
		self.listeAlphabets = listeAlphabets
		self.listeTransitions = listeTransitions
		self.etatInitial = None
		self.handlers = {}
		self.AFDHandlers = {}
		self.AFDListeAlphabets = []
		self.etatsFinaux = []
	
	def ajouterTransition(self, fromEtat, transition, toEtats):
		if transition not in self.listeTransitions and fromEtat not in self.listeAlphabets:
			raise("Les transitions et états doivent figurer dans la liste des valeurs définis ")
		for elt in toEtats:
			if elt not in self.listeAlphabets:
				raise("Les états choisis doivent figurer dans l'alphabet defini")
		self.handlers[fromEtat,transition] = toEtats

	def fixerEtatInitial(self, name):
		if name not in  self.listeAlphabets:
			raise("l'état initial doit figurer dans l'alphabet defini")
		self.etatInitial = name
	
	def fixerEtatsFinaux(self, *names):
		for etat in names:
			if etat not in self.listeAlphabets:
				raise("les états doivent figurés dans la liste des alphabets")
		for etat in names:
			self.etatsFinaux.append(etat)
	
	def afficher(self):
		print("Les différentes transitions avant la determinisation ")
		print(self.handlers)
		graph = Digraph(comment="l'affichage du graphe")
		for lettre in self.listeAlphabets:
			graph.node(lettre)

		for cle, valeur in self.handlers.items():
			for etatSuivant in valeur:
				etatPrecedent = str(cle[0])
				nomTransition = str(cle[1])
				graph.edge(etatPrecedent, str(etatSuivant), label=nomTransition)
		graph.render('output.gv', view=True)

	def determiniser(self):
		cas = ("0",)
		casATraiter = []
		casTraites = []
		transitionsEntreCas = {}
		casATraiter.append(cas)
		
		for cas in casATraiter:
			if cas not in casTraites:
				for a in self.listeTransitions:
					casSuivants = []
					for etat in cas:
						tupleEtatTransition = (etat,a)
						if self.handlers.has_key(tupleEtatTransition):
							tempList = self.handlers[tupleEtatTransition]
							for etatSuivant in tempList:
								if etatSuivant not in casSuivants:
									casSuivants.append(etatSuivant)
					casSuivants.sort()
					transitionsEntreCas[(cas,a)] = tuple(casSuivants)
					if casSuivants not in casATraiter:
						casATraiter.append(tuple(casSuivants))
					if cas not in casTraites:
						casTraites.append(tuple(cas))
		print("les transitions : {}".format(transitionsEntreCas))
		print("Les cas Traites : {}".format(casTraites))
		print("Les cas à Traiter:{}".format(casATraiter))

		dictNewAlphabets = {}
		i = 0
		for elt in casTraites:
			dictNewAlphabets[elt] = chr(65+i)
	       		self.AFDListeAlphabets.append(chr(65+i))
			i = i+1
		print("Le nouveau alphabet : {} ".format(self.AFDListeAlphabets))
		print("le dicNewAlphabets : {} ".format(dictNewAlphabets))
		for cle, valeur in transitionsEntreCas.items():
			print("cas : {} via transition : {} --> {}".format(cle[0],cle[1], valeur))
			cas = cle[0]
			transition = cle[1]
			casSuivant = valeur
			if cas in dictNewAlphabets.keys() and casSuivant in dictNewAlphabets.keys():
				newCas = dictNewAlphabets[cas]
				newCasSuivant = dictNewAlphabets[casSuivant]
				self.AFDHandlers[newCas,transition] = newCasSuivant


	def afficherAFD(self):
		graphAFD = Digraph(comment="le graphe determinisé", encoding="utf-8")
		for a in self.AFDListeAlphabets:
			print("Alphabet : {} ".format(a))
			graphAFD.node(a)
		print(self.AFDHandlers)
		for cle, valeur in self.AFDHandlers.items():
	        	print("cas : {} via transition : {} --> {} ".format(cle[0], cle[1], valeur))		
			graphAFD.edge(str(cle[0]), str(valeur), label=str(cle[1]))
		
		#graphAFD.render('outputAFD.gv', view=True)



			
