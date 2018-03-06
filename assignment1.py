#
#  assignment1.py
#  DECISION TREE IMPLEMENTATION
#
#  Created by Nehir Poyraz on 02.03.2018.
#  Copyright © 2018 Nehir Poyraz. All rights reserved.
#

import math


def ID3(Examples, Target_Attribute, Attributes):
    # ID3 (Examples, Target_Attribute, Attributes)
    # Examples: training examples  (List of indices of the training example set)
    # Target_Attribute: predicted by the tree (List of indices of the target attribute set)
    # Attributes: list of other attributes, tested by the learned decision tree (list of indices of the attributes)


    # Create a node
    #
    Root = Node(None, False)

    # if all Examples are the same class
    counters = classcounter(Examples)

    for count in counters:
        if count == len(Examples):
            Root.leaf = True
            Root.label = target[counters.index(count) +1]
            return Root

    #
    # if attributes is empty
    if not Attributes:
        Root.leaf = True
        Root.label = mostcommon(Examples)
        return Root

    else:
        A = bestclf(Examples, Attributes)
        Root.label = attributes[A][0]
        subsets = subset(Examples, A)
        #   foreach possible value, V_i, of A
        #       create a branch     |   Branch.condition = V_i
        Root.branches = attributes[A][1:]
        # for each branch create a new Node
        for sets in subsets:
            subtree = ID3(sets, sets, [a for a in Attributes if a != A])
            Root.children.append(subtree)

    return Root


class Node:
    'Common base class for all nodes'

    def __init__(self, parent, leaf):
        #        self.label = label  #Name of the attribute
        self.parent = parent
        self.leaf = leaf    # true if leaf, false if nonleaf
        self.children = []
        self.branches = []

class Branch:

    def __init__(self,  name, parent):
        self.name = name
        self.parent = parent
        self.children = []


def gain(S, A):
    informationgain = entropy(S)
    for s in subset(S, A):
        reduced = (len(s) / len(S)) * entropy(s)
        informationgain -= reduced
    return informationgain


def subset(S, A):
    subsets = []
    # j = attributes.index(A)  ||  j = A (attribute index is given as parameter)
    for v in attributes[A][1:]:
        S_v = []
        for s in S:
            if examples[s][A] == v:
                S_v.append(s)
        subsets.append(S_v)
    return subsets


def bestclf(S, A):

    # S(list): Elements of the list are the indices of elements in Examples (corresponds to the rows in dataset.txt)
    # A(list): Elements of the list are the indices of elements in attributes (index of the list (attribute and values))
    gains = [];
    for a in A:
        gains.append(gain(S, a))
    b = 0
    for i in range(len(gains)):
        if gains[i] > gains[A.index(A[b])]:
            b = i
    return A[b]



def entropy(samples):
    # S is a sample of training examples
    # S stores the indices in decisions which corresponds the sample value's index (row number)
    entropi = 0.0000
    counter = classcounter(samples)

    # print(counter)
    if not samples:
        return entropi

    fractions = [count / len(samples) for count in counter]
    for f in fractions:
        if f != 0:
            entropi -= f * math.log(f, 2)

    return entropi


def mostcommon(S):
    counters = classcounter(S)

    if counters[1] >= counters[-1]:
        if counters[0] >= counters[0]:
            return "+"
    else:
        if counters[-1] >= counters[0]:
            return "-"
    return "0"


def classcounter(S):
    counter = [0.0] * (len(target)-1)
    for s in S:
        if decisions[s] in target:
            counter[target.index(decisions[s])-1] += 1
    return counter


def main(dataset):
    global attributes
    global examples
    global decisions
    global target
    global line_cntr
    global sampleset
    global decisionTree

    attributes = []
    examples = []
    decisions = []
    target = []
    line_cntr = 0
    with open(dataset, "r") as datafile:
        for line in datafile:
            values = line.split(', ')
            decision = values[-1].replace("\n", "")
            if line_cntr is 0:
                for v in values[:-1]:
                    attributes.append([v])

                target.append(decision)

            else:
                examples.append(values[:-1])
                decisions.append(decision)
                if decision not in target:
                    target.append(decision)
                for i in range(len(attributes)):
                    if values[i] not in attributes[i]:
                        attributes[i].append(values[i])

            line_cntr += 1
    datafile.close()
    sampleset = [i for i in range(len(decisions))]
    decisionTree = ID3(sampleset, sampleset, [j for j in range(len(attributes))])



def printTree(tree):
    for b in range(len(tree.children)):
        print(tree.label, "=", tree.branches[b], "--> ", end="")
        if tree.children[b].leaf:
            print("OUTPUT =", tree.children[b].label)
        else:
            printTree(tree.children[b])

main("dataset1.txt")


# printTree(decisionTree)
