# -*- coding: utf-8 -*-

from Indiv import Indiv, IndivInt, IndivReal
from random import random, choices, randint


class Popul:

    def __init__(self, popsize, indsize, indivs=[], elitism=0):
        self.popsize = popsize
        self.indsize = indsize
        self.elitism = elitism
        if indivs:
            self.indivs = indivs
        else:
            self.initRandomPop()

    def getIndiv(self, index):
        return self.indivs[index]

    def initRandomPop(self):
        self.indivs = []
        for _ in range(self.popsize):
            indiv_i = Indiv(self.indsize, [])
            self.indivs.append(indiv_i)

    def getFitnesses(self, indivs=None):
        fitnesses = []
        if not indivs:
            indivs = self.indivs
        for ind in indivs:
            fitnesses.append(ind.getFitness())
        return fitnesses

    def bestFitness(self):
        return max(self.getFitnesses())

    def bestSolution(self):
        # self.indivs.sort(reverse=True)
        # return self.indivs[0], self.indivs[0].fitness
        fitnesses = self.getFitnesses()
        bestf = fitnesses[0]
        bestsol = 0
        for i in range(1, len(fitnesses)):
            if fitnesses[i] > bestf:
                bestf = fitnesses[i]
                bestsol = i
        return self.getIndiv(bestsol), bestf

    def selection(self, n, indivs=None):
        res = []
        fitnesses = list(self.linscaling(self.getFitnesses(indivs)))

        if self.elitism != 0:
            self.indivs.sort(reverse=True)
            res += list(range(self.elitism))

            for _ in range(n-self.elitism):
                sel = self.roulette(fitnesses)
                while sel in res:
                    sel = self.roulette(fitnesses)
                fitnesses[sel] = 0.0
                res.append(sel)
        else:
            for _ in range(n):
                sel = self.roulette(fitnesses)
                fitnesses[sel] = 0.0
                res.append(sel)

        return res

    def tournamentSelection(self, n, indivs=None):
        # Applies tournament algorithm to select k random individuals.
        # From those, the individual with best fitness is selected.

        if not indivs:
            indivs = self.indivs
        res = []
        indivsList = []
        size = len(indivs)

        k = randint(1, n) # k random individuals

        indivsList = list(range(size)) # positions of the individuals

        for _ in range(n):
            indexesComparison = choices(indivsList, k=k) # selects k random indexes
            indivsComparison = []

            for ind in indexesComparison: # selects individuals (+ their indexes) to compare 
                indivsComparison.append((indivs[ind], ind))

            indivsComparison.sort(key=lambda tup: tup[0], reverse=True) # sorts by fitnessess

            bestIndiv = indivsComparison[0][1] # best individual
            indivsComparison.remove(bestIndiv) #removes the best one from the list
            res.append(bestIndiv) # adds the best's index to the result.

        return res

    def roulette(self, f):
        tot = sum(f)
        val = random()
        acum = 0.0
        ind = 0
        while acum < val:
            acum += (f[ind] / tot)
            ind += 1
        return ind-1

    def linscaling(self, fitnesses):
        mx = max(fitnesses)
        mn = min(fitnesses)
        res = []
        for f in fitnesses:
            val = (f-mn)/(mx-mn)
            res.append(val)
        return res

    def recombination(self, parents, noffspring):
        offspring = []
        new_inds = 0
        while new_inds < noffspring:
            parent1 = self.indivs[parents[new_inds]]
            parent2 = self.indivs[parents[new_inds+1]]
            offsp1, offsp2 = parent1.ringCrossover(parent2)
            offsp1.inversionMutation()
            offsp2.inversionMutation()
            offspring.append(offsp1)
            offspring.append(offsp2)
            new_inds += 2
        return offspring

    def reinsertion(self, offspring):
        tokeep = self.selection(self.popsize-len(offspring))
        ind_offsp = 0
        for i in range(self.popsize):
            if i not in tokeep:
                self.indivs[i] = offspring[ind_offsp]
                ind_offsp += 1


class PopulInt(Popul):

    def __init__(self, popsize, indsize, maxValue, indivs=[], elitism=0):
        self.maxValue = maxValue
        Popul.__init__(self, popsize, indsize, indivs, elitism)

    def initRandomPop(self):
        self.indivs = []
        for _ in range(self.popsize):
            indiv_i = IndivInt(self.indsize, [], 0, self.maxValue)
            self.indivs.append(indiv_i)


class PopulReal(Popul):

    def __init__(self, popsize, indsize, lowerLim=0.0, upperLim=1.0, indivs=[], elitism=0):
        self.upperLim = upperLim
        self.lowerLim = lowerLim
        Popul.__init__(self, popsize, indsize, indivs, elitism)

    def initRandomPop(self):
        self.indivs = []
        for _ in range(self.popsize):
            indiv_i = IndivReal(self.indsize, [], self.lowerLim, self.upperLim)
            self.indivs.append(indiv_i)
