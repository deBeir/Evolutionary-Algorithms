from random import randint, random, shuffle, choice
from abc import ABC, abstractmethod


class Indiv():

    def __init__(self, size, genes=[], lowerLim=0, upperLim=1):
        self.lowerLim = lowerLim
        self.upperLim = upperLim
        self.genes = genes
        if not self.genes:
            self.initRandom(size)
          
    
    def __eq__(self, solution):
        if isinstance(solution, self.__class__):
            return self.genes.sort() == solution.genes.sort()
        return False

    def __gt__(self, solution):
        if isinstance(solution, self.__class__):
            return self.fitness > solution.fitness
        return False

    def __lt__(self, solution):
        if isinstance(solution, self.__class__):
            return self.fitness < solution.fitness
        return False

    def __ge__(self, solution):
        if isinstance(solution, self.__class__):
            return self.fitness >= solution.fitness
        return False

    def __le__(self, solution):
        if isinstance(solution, self.__class__):
            return self.fitness <= solution.fitness
        return False

    def setFitness(self, fit):
        self.fitness = fit

    def getFitness(self):
        return self.fitness

    def getGenes(self):
        return self.genes

    def initRandom(self, size):
        self.genes = []
        for _ in range(size):
            self.genes.append(randint(0, 1))

    def mutation(self):
        s = len(self.genes)
        pos = randint(0, s-1)
        if self.genes[pos] == 0:
            self.genes[pos] = 1
        else:
            self.genes[pos] = 0

    def inversionMutation(self):
        # Given 2 random positions (p1<p2), swaps all values in between p1 and p2.

        size = len(self.genes)
        position1 = randint(0, size-2)
        position2 = randint(position1+1, size-1)

        for i in range(position2-position1):
            genei = self.genes[i]
            self.genes[i] = self.genes[position2-i]
            self.genes[position2-i] = genei

    def swapMutation(self):
        # Given 2 random positions (p1<p2), swaps those values.

        size = len(self.genes)
        position1 = randint(0, size-2)
        position2 = randint(pos1+1, size-1)

        genePos1 = self.genes[position1]
        self.genes[position1] = self.genes[position2]
        self.genes[position2] = genePos1
        
    def scrambleMutation(self):
        # Applies a random mutation to a (random) position range.
        
        size = len(self.genes)
        pos1 = randint(0, size-2)
        pos2 = randint(pos1+1, size-1)
        
        list_pos = list(range(pos1, pos2))
        list_pos_unused = list(range(pos1, pos2))

        for i in range(len(list_pos)):
            pos_selected = choice(list_pos_unused)
            list_pos_unused.remove(pos_selected)
            pos_to_change = list_pos[i]
            self.genes[pos_to_change] = self.genes[pos_selected]

    def crossover(self, indiv2):
        return self.crossover(indiv2)

    def one_pt_crossover(self, indiv2):
        offsp1 = []
        offsp2 = []
        s = len(self.genes)
        pos = randint(0, s-1)
        for i in range(pos):
            offsp1.append(self.genes[i])
            offsp2.append(indiv2.genes[i])
        for i in range(pos, s):
            offsp2.append(self.genes[i])
            offsp1.append(indiv2.genes[i])
        return self.__class__(s, offsp1, self.lowerLim, self.upperLim), self.__class__(s, offsp2, self.lowerLim, self.upperLim)
    
    def two_pt_crossover(self, indiv2):
        # Recombination between 2 individuals given 2 random points (p1<p2).
        # Everything in between p1 and p2 swaps. 
       
        offsp1 = []
        offsp2 = []
        size = len(self.genes)

        # Position selection
        position1 = randint(0, size-2)
        position2 = randint(pos1+1, size-1)

        # Ranges to be used in each for loop
        headRange = range(position1) # 0 to recombinant region
        middleRange = range(position1, position2+1) # recombinant region
        tailRange = range(position2+1, size) # from recombinant region to final position
        
        for i in headRange:
            offsp1.append(self.genes[i])
            offsp2.append(indiv2.genes[i])

        # Recombinant region == offsprings genetically differ from their parants
        for i in middleRange:
            offsp1.append(indiv2.genes[i])
            offsp2.append(self.genes[i])

        for i in tailRange:
            offsp1.append(self.genes[i])
            offsp2.append(indiv2.genes[i])

        return self.__class__(size, offsp1, self.lowerLim, self.upperLim), self.__class__(size, offsp2, self.lowerLim, self.upperLim)
    
    def uniform_crossover(self, indiv2):
        if len(self.genes) != len(indiv2.genes):
            return False
        randomG = []
        size = len(self.genes)
        for i in range(len(self.genes)):
            randomG.append(randint(0, 1))
        offsp1 = []
        offsp2 = []
        for k in range(len(randomG)):
            if randomG[k] == 0:
                offsp1.append(self.genes[k])
                offsp2.append(indiv2.genes[k])
            else:
                offsp1.append(indiv2.genes[k])
                offsp2.append(self.genes[k])
        
        return self.__class__(size, offsp1), self.__class__(size, offsp2)
    
   def discrete_crossover(self, indiv2):
        # Applies discret recombination between two different individuals through random selection of which parent 
        # will provide the genes.
        
        offsp1 = []
        offsp2 = []
        size = len(self.genes)

        genesParent1 = self.genes
        genesParent2 = indiv2.getGenes()

        randomOffS1 = []
        randomOffS2 = []

        for i in range(size):
            randomOffS1.append(randint(0, 1))
            randomOffS2.append(randint(0, 1))

        for i,k in enumerate(randomOffS1):
            if k == 0:
                offsp1.append(genesParent1[i])
            else:
                offsp1.append(genesParent2[i])

        for i,k in enumerate(randomOffS2):
            if k == 0:
                offsp2.append(genesParent1[i])
            else:
                offsp2.append(genesParent2[i])

        return self.__class__(size, offsp1, self.lowerLim, self.upperLim), self.__class__(size, offsp2, self.lowerLim, self.upperLim) 

  
    def ringCrossover(self, indiv2):
        # Recombination between 2 individuals by selecting a random point
        # Returns 2 offsprings with the genes from the random position

        offsp1 = []
        offsp2 = []
        size = len(self.genes)

        # Joins genes from 2 individuals
        joinGenes = self.genes + indiv2.getGenes()
        joinSize = len(joinGenes)

        position = randint(0, size-1) # Random position

        # 1st offspring ==  random position + list length
        offsp1 = joinGenes[position:position+size]

        head = joinGenes[:position] # list (what's left) head
        tail = joinGenes[position+size:joinSize] # list (what's left) tail

        # 2nd offspring == head+tail reversed lists 
        headRev = list(reversed(head))
        tailRev = list(reversed(tail))
        offsp2 = headRev + tailRev
        
        return self.__class__(size, offsp1, self.lowerLim, self.upperLim), self.__class__(size, offsp2, self.lowerLim, self.upperLim)

class IndivInt (Indiv):

    def initRandom(self, size):
        self.genes = []
        for _ in range(size):
            self.genes.append(randint(0, self.upperLim))

    def mutation(self):
        s = len(self.genes)
        pos = randint(0, s-1)
        self.genes[pos] = randint(0, self.upperLim)


class IndivReal (Indiv):

    def initRandom(self, size):
        self.genes = []
        for _ in range(size):
            delta = self.upperLim-self.lowerLim
            self.genes.append(random()*delta+self.lowerLim)

    def mutation(self):
        s = len(self.genes)
        pos = randint(0, s-1)
        delta = self.upperLim-self.lowerLim
        self.genes[pos] = random()*delta+self.lowerLim
