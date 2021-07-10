# Evolutionary Algorithms
Implementation of novel mutation, selection and crossover operators to the previously developed EA.

### About
Evolutionary Algorithms (EA) are stochastic algorithms based on natural phenomena: genetic inheritance and natural selection that allows the survival of the fittest individuals.

During Advanced Algorithms for Bioinformatics' classes an EA with all the basic tasks this type of algorithm is expected to perform was developed. This Genetic Algorithm (GA) is thus capable of initialize a population, select individuals according to their fitnessess, apply the recombinant operators to the selected set and finally attain the new population, finalizing the whole iteration. 

By adding new functionalities to this GA, it is possible to diversify even more the population, which will make for better and more interesting results. To that end, I decided to add the following features to the _```Indiv```_ and _```Popul```_ classes. 

#### Selection Operators

- _```tournamentSelection```_: this function applies the Tournament Algorithm (TA) in order to randomly select _k_ random individuals from an also random population. From those k individuals, one is selected – the one with the best fitness value. As the algorithms’ name suggests, the  TA runs ‘tournaments’ among the selected indiviuals. The best one is then signaled for ‘reprodution’ (the crossover process).

#### Mutation Operators
- _```inversionMutation```_: this type of mutation operator swaps all values (that is, genes) in between two randomly generated positions, where position one comes before position two.
- _```swapMutation```_: the swap mutation switches the position of two genes from two random positions. Applying this mutation will make the gene in position one swap with the one in position two.
- _```scrambleMutation```_: this mutation type enforces a random mutation between a position range, i.e., selects two distinct random positions (where pos1 < pos2), and swaps the values between said positions in the [pos1,pos2] range.

#### Crossover Operators
- _```two_pt_crossover```_: this operator recombines two individuals after selecting two random positions, where position one appears before position two and everything in between these two points swaps. This recombinant region will thus make sure that the offsprings genetically differ from the parent individuals.
- _```ringCrossover```_: the crossover operator starts with two random individuals being randomly chosen and all their genes are then grouped together. Afterwards, a random position is selected as a cutting point.  Another random point is chosen so that it is possible to obtain the offsprings. The length of the sequence between both points will be equal to the one of the parent gene set.  One offspring is produced in a counterclockwise direction and the other in a clockwise direction. By using this specific crossover method, it is possible to get a more diverse set of offsprings.
- _```discreteCrossover```_: discrete crossover applies a discrete recombination between two parent individuals through random selection of which parent the gene will be selected from. 
