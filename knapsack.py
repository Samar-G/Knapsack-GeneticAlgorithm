# -- coding: utf-8 --
"""
Created on Wed Apr 21 05:30:43 2021

@author: samar
"""
import random

# Reading of File
my_file = open("Test.txt", "r")
content = my_file.read()
content_list = content.split("\n")
new_list = [e for e in content_list if len(e.strip()) != 0]  # to remove the space
new_list2 = []
for i in new_list:
    Str = i.split(" ")  # to split every character from the string, file gets read as string, and we need each one alone
    new_list2.append(Str)

final = []
for i in new_list2:
    mat = []
    if len(i) == 2:  # weights and benifits
        for j in i:
            new = int(j)
            mat.append(new)  # appended in list of lists, mat is a list
        final.append(mat)
    else:  # knapsack size or items number
        for j in i:
            new = int(j)
        final.append(new)  # appended as int
test_cases = final[0]  # C, first thing in the file so index=0
final.remove(final[0])  # removes it to free space while looping on the rest of the file and avoid complications

sizes = []  # sizes
WB1 = []  # weights and benifits
for i in range(len(final)):
    if (type(final[i]) is int):  # either items or weights
        sizes.append(final[i])  # knapsize, items
    else:
        WB1.append(final[i])  # weights and benifts
items = []  # to separate knapsize and items
knapsizes = []
for i in range(len(sizes)):
    if i % 2 == 0:
        items.append(sizes[i])
    else:
        knapsizes.append(sizes[i])


########################################

# randomization for 0 and 1/ G0
def Random(N):
    n = []
    for x in range(N):
        y = random.random()
        if (y < 0.5):
            n.append(0)
        else:
            n.append(1)
    return n


def check(f, size, W):
    sum1 = 0
    for i, j in enumerate(f):  # 101
        if j == 1:
            sum1 += W[i]
    if (sum1 <= size):
        return True
    else:
        return False


def outOfRange(OfSp1, OfSp2, KnaSize, W):
    sum1 = 0
    sum2 = 0
    for i, j in enumerate(OfSp1):  # 101
        if j == 1:
            sum1 += W[i]
    for m, k in enumerate(OfSp2):
        if k == 1:
            sum2 += W[m]
    if (sum1 > KnaSize or sum2 > KnaSize):
        return True
    else:
        return False


# probability of mutation
def Pm(N):
    x = random.uniform(0.001, 0.1)
    return x


# probability of cross over
def Pc(N):
    x = random.uniform(0.4, 0.7)
    return x


# return the possible genertion "less the knapsack size"
def Solutions(W, N, KnapSize, PopSize):
    possible = []
    while (len(possible) < PopSize):
        randChromosome = Random(N)
        Sum = 0
        for i, cont in enumerate(randChromosome):
            if (cont == 1):
                Sum += W[i]
        if (Sum > KnapSize or Sum == 0):
            continue
        else:
            possible.append(randChromosome)
    return possible


# nzwd boolean lw 1 y7sb benifit, lw 0 y7sb weight
def Fitness(WB, sol):
    sumlist = []
    for i, cont in enumerate(sol):
        Sum = 0
        for y in range(len(cont)):
            if (cont[y] == 1):
                Sum += WB[y][1]
        sumlist.append(Sum)
    return sumlist


def Selection(WB, sol):
    lFit = Fitness(WB, sol)
    lPer = []
    lRange = []
    totFit = sum(lFit)
    z = random.random()
    # for f in lFit:
    #    totFit+=f
    for l in lFit:
        if (totFit != 0 and l != 0):
            per = l / totFit
            lPer.append(per)
        else:
            lPer.append(0)
    start = 0
    end = lPer[0]
    for p in lPer:
        lRange.append([start, end])
        start = end
        end = end + p
    count = 0
    for i, r in enumerate(lRange):
        if r[0] <= z <= r[1]:
            count = i
    return sol[count]


def CrossOver(p1, p2, N, sol, KnaSize):
    pc = Pc(N)
    Pos = random.randint(1, N - 1)
    rand = random.random()
    OfSp1 = []
    OfSp2 = []
    if (rand <= pc):
        OfSp1 = p1[:Pos] + p2[Pos:]
        OfSp2 = p2[:Pos] + p1[Pos:]
    else:
        OfSp1 = p1
        OfSp2 = p2
    return OfSp1, OfSp2


def Mutation(aftCross, N):
    pm = Pm(N)
    for i in range(len(aftCross)):
        for x in range(N):
            rand = random.random()
            if (rand <= pm):
                if (aftCross[i][x] == 0):
                    aftCross[i][x] = 1
                else:
                    aftCross[i][x] = 0
    return aftCross


def Replacement(aftMut, sol, Wb, W, KnaSize, N):
    replace = []
    fsol = Fitness(WB, sol)
    faftMut = Fitness(WB, aftMut)
    replacement = []
    for i in range(len(fsol)):
        for j in range(len(faftMut)):
            if faftMut[j] >= fsol[i]:
                if check(aftMut[j], KnaSize, W):
                    replacement = aftMut[j]
                elif (check(sol[i], KnaSize, W)):
                    replacement = sol[i]
            elif (check(sol[i], KnaSize, W)):
                replacement = sol[i]
            else:
                replacement = sol[0]
        replace.append(replacement)
    return replace


def GA(C, sol, W, N, KnaSize, G):
    coSol = sol
    ans = ConvertToReal(coSol, N, KnaSize)
    maxi = ans
    for x in range(G):
        newGen = []
        sel1 = []
        sel2 = []
        cross = []
        mut = []
        for i in range(0, len(coSol), 2):
            sel1 = Selection(WB, coSol)
            sel2 = Selection(WB, coSol)
            while (sel1 == sel2):
                sel2 = Selection(WB, coSol)
            cross = CrossOver(sel1, sel2, N, sol, KnaSize)
            mut = Mutation(cross, N)

            if (not outOfRange(mut[0], mut[1], KnaSize, W)):
                newGen.append(mut[0])
                newGen.append(mut[1])
            else:
                newGen.append(sol[0])
                newGen.append(sol[1])
        rep = Replacement(newGen, coSol, WB, W, KnaSize, N)
        coSol = rep
        ans = ConvertToReal(coSol, N, KnaSize)
        if (maxi[0] < ans[0] and calcW(ans[2], KnaSize)):
            maxi = ans
        else:
            maxi = maxi
    return maxi


# return the actual values that had 1 as a gene
def ConvertToReal(mut, N, KnapSize):
    mat = []
    fit = Fitness(WB, mut)
    maxi = fit[0]
    i = 0
    cnt = 0
    for z, x in enumerate(fit):
        if (maxi < x and maxi <= KnapSize):
            maxi = x
            i = z
    for i, j in enumerate(mut[i]):  # returns weights and number of items selected
        if (j == 1):
            mat.append(WB[i])
            cnt += 1
    return maxi, cnt, mat


def calcW(M, k):
    sum = 0
    for i in range(len(M)):
        sum += M[i][0]
    if (sum <= k):
        return True
    else:
        return False


# C=int(input("Enter the Number of Test Cases without exceeding 20: "))
# if(C>20):
#    C=int(input("Enter the Number of Test Cases without exceeding 20: "))
GenNum = 500
PopSize = 250
# Final=[] 50,350
for i in range(test_cases):  # loops number of testcases(C)
    Size = knapsizes[i]  # knapsacksize
    N = items[i]  # items
    # print(N)
    # print(Size)
    WB = []
    for k in range(N):  # to append benifits and weights of current case
        WB.append(WB1[k])
    del WB1[0:N]  # to make it easier to read for next case, and doesn't cause conflicts
    weights = []
    for index, List in enumerate(WB):  # to take weights only
        # for i in range(len(List)):
        weights.append(List[0])
    # print(WB)
    solFin = Solutions(weights, N, Size, PopSize)
    rslt = GA(test_cases, solFin, weights, N, Size, GenNum)
    # finRes=ConvertToReal(rslt,N,Size)
    # Final.append(finRes)
    print(rslt)
