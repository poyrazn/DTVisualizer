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
    # Attributes: list of other attributes, tested by the learned decision tree

    # Create a node     ??   node.type = root
    #
    Root = Node(None, "root")

    # if all Examples are positive
    #   Root.label <-- +
    #   return the single-node tree
    counters = classcounter(decisions)
    if counters[-1] + counters[0] == 0:
        Root.label = "+"
        return Root
    #
    # if all Examples are negative
    #   Rode.label <-- -
    #   return the single-node tree root
    if counters[1] + counters[0] == 0:
        Root.label = "-"
        return Root

    if counters[1] + counters[-1] == 0:
        Root.label = "0"
        return Root

    #
    # if attributes is empty
    #   Node.label <-- most common value of Target_Attribute in Examples
    #   return the single-node tree root
    if not Attributes:
        Root.label = mostcommon()
        return Root
    #
    # else
    #   A  <-- Maximum information gain attr
    #   Root.label <-- A
    #   the decision attribute for Root <-- A
    else:
        Root.label


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

    def __init__(self, parent, type):
        #        self.label = label  #Name of the attribute
        self.parent = parent
        self.type = type    # root,
        self.branch = []



def gain(samples, attribute):
    informationgain = entropy(samples)

    for v in attributes[attributes.index(attribute)][1:]:
        S_v = []  #
        for i in range(len(samples)):
            if samples[i][1] == v:
                S_v.append((attributes.index(attribute), v, decisions[i]))

        informationgain -= (classcounter(S_v)[2] / len(samples)) * entropy(S_v)

    return informationgain



# def bestclf:


def entropy(samples):
    # S is a sample of training examples
    # S stores the indices in decisions which corresponds the sample value's index (row number)
    entropi = 0.0000
    counter = classcounter(samples)
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

    counter= [0.0, 0.0, 0.0, 0.0]
    for s in S:
        if s[2] == ("yes" or "win"):
            counter[1] += 1
        elif s[2] == ("no" or "lose" or "loose"):
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

    attributes = []
    examples = []
    decisions = []
    targettrb = ""
    line_cntr = 0
    with open(dataset, "r") as datafile:
        for line in datafile:
            values = line.split(', ')

            if line_cntr is 0:
                for v in values[:-1]:
                    attributes.append([v])
                targettrb = values[-1][:-1]
            else:

                examples.append(values[:-1])
                decisions.append(values[-1][:-1])
                for i in range(len(attributes)):
                    if values[i] not in attributes[i]:
                        attributes[i].append(values[i])

            line_cntr += 1
    datafile.close()




#
# def attrindex(attribute):
#     for i in range(len(features)):
#         if features[i][0] == attribute:
#             return i
#     return -1


initialize("dataset1.txt")


for i in range(len(attributes)):
    S = []
    for j in range(len(examples)):
        S.append((j, examples[j][i], decisions[j]))
    print("Entropy: %.3f" % entropy(S))
    print("Gain on ", attributes[i][0], " %.4f" % gain(S, attributes[i]))