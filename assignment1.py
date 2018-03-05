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
    # Examples: training examples
    # Target_Attribute: predicted by the tree
    # Attributes: list of other attributes, tested by the learned decision tree (list of indices of the attributes)

    # Create a node     ??   node.type = root
    #
    Root = Node(None, False)

    # if all Examples are positive
    #   Root.label <-- +
    #   return the single-node tree
    counters = classcounter(Examples)
    if counters[1] == counters[2]:
    # if counters[-1] + counters[0] == 0:
        Root.leaf = True
        Root.label = "+"
        return Root
    #
    # if all Examples are negative
    #   Rode.label <-- -
    #   return the single-node tree root
    if counters[-1] == counters[2]:
    # if counters[1] + counters[0] == 0:
        Root.leaf = True
        Root.label = "-"
        return Root
    if counters[0] == counters[2]:
    # if counters[1] + counters[-1] == 0:
        Root.leaf = True
        Root.label = "0"
        return Root

    #
    # if attributes is empty
    #   Node.label <-- most common value of Target_Attribute in Examples
    #   return the single-node tree root
    if not Attributes:
        Root.leaf = True
        Root.label = mostcommon(Examples)
        # print("most common: in ", Examples , Root.label)
        return Root
    #
    # else
    #   A  <-- Maximum information gain attr
    #   Root.label <-- A
    #   the decision attribute for Root <-- A
    else:
        # attribute = bestclf(S,A)
        A = bestclf(Examples, Attributes)
        Root.label = attributes[A][0]
        subsets = subset(Examples, A)
        Root.branches = attributes[A][1:]
        # print("Subsets of attribute:", attributes[A][0])
        # print(subsets)
        for example in subsets:
            if not example:
                leaf = Node(Root, True)
                leaf.label = mostcommon(Examples)
                Root.children.append(leaf)
            else:
                # print("Examples for", attributes[A][subsets.index(example)+1])
                # print(example)
                # print("Attributes:")
                # print(Attributes)
                # print("A:", A)
                attributesleft = [a for a in Attributes if a != A]
                # print("Attributes left")
                # print(attributesleft)
                subtree = ID3(example, example, attributesleft)
                Root.children.append(subtree)

        # print("Best attribute:" , Root.label)
        # if A <= 1:
        #     newnode = Node(Root, True)
        #     newnode.label = mostcommon(Examples)
        #     print("Leaf node with" , newnode.label)
        # else:
        #     for example in subset(Examples,A):
        #         subtree = ID3(example, Target_Attribute, Attributes[:A] + Attributes[A+1:])
        #         Root.children.append(subtree)
        #         print(subtree.label)
    return Root


#
#   foreach possible value, V_i, of A
#       create a branch     ??   Branch.condition = V_i
#       Root.childnum++
#
#       foreach example in Examples
#           if  Example.value = V_i
#               Examples_Vi.add(example)
#           if Examples_Vi is empty
#               create a Node
#               Node.label <-- most common value of Target_attr in Examples
#               Node.type <-- leaf
#               Branch.link(Node)
#           else
#               new Node <-- constructree(Examples_Vi, Target_Attr, Attributes - {A})
#               Branch.link(Node)
#
# end
# Return Root


# def constructree (Examples, target_attr, Attributes):



class Node:
    'Common base class for all nodes'

    def __init__(self, parent, leaf):
        #        self.label = label  #Name of the attribute
        self.parent = parent
        self.leaf = leaf    # true if leaf, false if nonleaf
        self.children = []
        self.branches = []


def gain(samples, attribute):
    informationgain = entropy(samples)
    for s in subset(samples, attribute):
        reduced = (len(s) / len(samples)) * entropy(s)
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


def bestclf(S,A):

    gains = [];
    for a in A:
        gains.append(gain(S, a))
    b = 0
    for i in range(len(gains)):
        if gains[i] > gains[A.index(A[b])]:
            b = i
    return A[b]

    # gains = [];
    # for a in A:
    #     gains.append(gain(S, a))
    # maxgain = 0
    # b = 0
    # for i in range(len(gains)):
    #     if gains[i] > maxgain:
    #         maxgain = gains[i]
    #         b = i
    # return A[b]


def entropy(samples):
    # S is a sample of training examples
    # S stores the indices in decisions which corresponds the sample value's index (row number)
    entropi = 0.0000
    counter = classcounter(samples)
    # print(counter)
    if not samples:
        return entropi
    fractions = [counter[0] / counter[2], counter[1] / counter[2], counter[-1] / counter[2]]
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

    counter = [0.0, 0.0, 0.0, 0.0]
    for s in S:
        if decisions[s] == ("yes" or "win"):
            counter[1] += 1
        elif decisions[s] == ("no" or "lose" or "loose"):
            counter[-1] += 1
        else:
            counter[0] += 1
        counter[2] += 1
    return counter


def initialize(dataset):
    global attributes
    global examples
    global decisions
    global targettrb
    global line_cntr
    global sampleset

    attributes = []
    examples = []
    decisions = []
    targettrb = []
    line_cntr = 0
    with open(dataset, "r") as datafile:
        for line in datafile:
            values = line.split(', ')

            if line_cntr is 0:
                for v in values[:-1]:
                    attributes.append([v])
                targettrb.append(values[-1][:-1])
            else:

                examples.append(values[:-1])
                decisions.append(values[-1][:-1])
                for i in range(len(attributes)):
                    if values[i] not in attributes[i]:
                        attributes[i].append(values[i])

            line_cntr += 1
    datafile.close()
    sampleset = [i for i in range(len(decisions))]


def printTree(tree):
    print(tree.label)
    for child in tree.children:
        print(tree.branches[tree.children.index(child)])
        printTree(child)


initialize("dataset1.txt")

nd = ID3(sampleset, sampleset, [j for j in range(len(attributes))])
printTree(nd)



