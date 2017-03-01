#!/usr/bin/env python
#! -*- coding:utf-8 -*-

from Automate import Automate

alphabet = ["0","1","2"]
transitions = ["a","b", ":e:"]

monAutomate = Automate(alphabet, transitions)
monAutomate.ajouterTransition("0","a", ["1"])
monAutomate.ajouterTransition("0","b", ["2"])
monAutomate.ajouterTransition("1",":e:", ["2"])
monAutomate.ajouterTransition("2","b", ["1"])
monAutomate.fixerEtatInitial("0")
monAutomate.fixerEtatsFinaux("1","2")
monAutomate.afficher()
monAutomate.determiniser()
monAutomate.afficherAFD()

