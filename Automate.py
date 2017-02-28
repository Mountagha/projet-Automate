#!/usr/bin/env python
# -*-  coding:utf-8 -*-

import graphviz

class Automate:

	def __init__(self, listeAlphabets, listeTransitions):
		self.listeAlphabets = listeAlphabets
		self.listeTransitions = listeTransitions
		self.etatInitial = None
		self.handlers = {}
		self.AFDHandlers = {}
		self.AFDEtatInitial = None
		self.AFDListeAlphabets = []
		self.etatsFinaux = []
		self.AFDEtatsFinaux = []
	
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
		graphAFN = graphviz.Digraph(format='png')
		for lettre in self.listeAlphabets:
			if lettre in self.etatsFinaux:
				graphAFN.node(lettre, label=lettre, shape="doublecircle")
			elif lettre == self.etatInitial:
				graphAFN.node(lettre, label=lettre, color="red")
			else:
				grapheAFN.node(lettre)

		for cle, valeur in self.handlers.items():
			for etatSuivant in valeur:
				etatPrecedent = str(cle[0])
				nomTransition = str(cle[1])
				graphAFN.edge(etatPrecedent, str(etatSuivant), label=nomTransition)
		print("[+] Graphe AFN généré : {}".format(graphAFN.source))
		output = graphAFN.render(filename='imageGraphAFN')

	def determiniser(self):
		deterministe = True
		cas = tuple(self.etatInitial) 
		casATraiter = []
		casTraites = []
		transitionsEntreCas = {}
		casATraiter.append(cas)

		print("Les transitions avec epsilons transitions non traites: {}".format(self.handlers))

		#on verifie si l'automate est déterministe en verifiant s'il y'a epsilon transition ou bien une transition ambigue

		for key,value in self.handlers.items():
			if len(value) > 1 or key[1] == ":e:": 
				deterministe = False
				break
		if deterministe == False:

			#on traite d'abord les epsilons transitions avant de passer à la determinisation proprement dite
			#les transitions notamment on applique l'algorithme suivant: 
			#Pour tout état p et pour epsilon-successeur q de p on ajoute une transition qui part et qui va au même endroit .
			epsilonTransition = False
			for key in self.handlers.keys():
				if key[1] == ":e:":
					epsilonTransition = True
			if epsilonTransition:
			#on a des epsilons dans l'automate donc on les supprime via l'algorithme ci-dessus
				listeTransitionsSansEpsilon = []
				for elt in self.listeTransitions:
					if elt != ":e:":
						listeTransitionsSansEpsilon.append(elt)

				for key,value in self.handlers.items():
					new_Successeurs = []
					if key[1] == ":e:":
						e_Successeurs = value
						for e_Etat in e_Successeurs:
							for transition in listeTransitionsSansEpsilon:
								current_key = (e_Etat, transition)
								if self.handlers.has_key(current_key):
									for etat in self.handlers[current_key]:
										new_Successeurs.append(etat)
							print("les successeurs: {}".format(new_Successeurs))
							if len(new_Successeurs) > 0:
								self.handlers[key[0],transition] = new_Successeurs
						del self.handlers[key]
				print("Les transitions avec epsilons transitions supprimés: {}".format(self.handlers))
				
				#on supprime à present le ":e:" dans la liste des transitions pour les traitements avenir
				self.listeTransitions = listeTransitionsSansEpsilon			
		
			#et là on traite les transitions cas à cas après avoir reglé le problème des epsilons transitions
		
			
			for cas in casATraiter:
				if cas not in casTraites:
					casTraites.append(tuple(cas))
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
						if casSuivants not in casATraiter and len(casSuivants) > 0:
							casATraiter.append(tuple(casSuivants))
			print("les transitions du tableau de determinisation: {}".format(transitionsEntreCas))
			print("Les nouveaux états : {}".format(casTraites))
			print("Les nouveaux états non traités encore :{}".format(casATraiter))

			#on crée un nouveau alphabet pour notre automate determinisé étant donné que ce dernier peut avoir moins
			#d'états que l'automate d'origine ainsi que de nouvelles transitions.

			dictNewAlphabets = {}
			i = 0
			for elt in casTraites:
				dictNewAlphabets[elt] = chr(65+i)
	       			self.AFDListeAlphabets.append(chr(65+i))
				for ss_elt in elt:
					if ss_elt in self.etatsFinaux:
						self.AFDEtatsFinaux.append(chr(65+i))
					elif ss_elt == self.etatInitial:
						self.AFDEtatFinal = ss_elt
				i = i+1
			print("Le nouveau alphabet de l'AFD: {} ".format(self.AFDListeAlphabets))
			print("le dicNewAlphabets de l'AFD : {} ".format(dictNewAlphabets))
			for cle, valeur in transitionsEntreCas.items():
				print("cas : {} via transition , label=noeud: {} --> {}".format(cle[0],cle[1], valeur))
				cas = cle[0]
				transition = cle[1]
				casSuivant = valeur
				if cas in dictNewAlphabets.keys() and casSuivant in dictNewAlphabets.keys():
					newCas = dictNewAlphabets[cas]
					newCasSuivant = dictNewAlphabets[casSuivant]
					self.AFDHandlers[newCas,transition] = newCasSuivant
		else: #automate déjà deterministe
			print("Cet automate est déjà déterministe\n")

	def afficherAFD(self):
		graphAFD = graphviz.Digraph(format='png')
		print(self.AFDListeAlphabets)
		for a in self.AFDListeAlphabets:
			if a in self.AFDEtatsFinaux:
				graphAFD.node(a, label=a, shape="doublecircle")
			elif a == self.etatInitial:
				graph.node(a, label=a, color="red")
			else:
				graphAFD.node(a)
		for cle, valeur in self.AFDHandlers.items():
			graphAFD.edge(str(cle[0]), str(valeur), label=str(cle[1]))
		print("graphe AFD généré : {}".format(graphAFD.source))
		filenameAFD = graphAFD.render(filename='imageGraphAFD')
			
