"""
@author: JBH
@email: jbhayet@cimat.mx
"""

import numpy as np

def sanchez(votes,parties,nSeats,detailed_print=False):
    pass

def hagenbach(votes,parties,nSeats,detailed_print=False):
    nParties= len(parties)
    if detailed_print:
        print("------------------------")
        print("Hagenbach model")
    distribution = np.zeros(nParties)
    remainders   = np.zeros(nParties)
    # Attribution from the quotient
    for idx in range(nParties):
        distribution[idx] = int((nSeats+1)*votes[0,idx])//int(np.sum(votes[0,:-1]))
        remainders[idx]   = nSeats*votes[0,idx]/np.sum(votes[0,:-1]) - distribution[idx]
    sorted = np.argsort(remainders)
    # Attributes remaining seats
    for idx in sorted[::-1]:
        if np.sum(distribution)==nSeats:
            break
        distribution[idx] += 1

    if detailed_print:
        for idx in range(nParties):
            print("Party: {}  Seats: {}".format(parties[idx],int(distribution[idx])))
    return distribution

def hare(votes,parties,nSeats,detailed_print=False):
    nParties= len(parties)
    if detailed_print:
        print("------------------------")
        print("Hare model")
    distribution = np.zeros(nParties)
    remainders   = np.zeros(nParties)
    # Attribution from the quotient
    for idx in range(nParties):
        distribution[idx] = int(nSeats*votes[0,idx])//int(np.sum(votes[0,:-1]))
        remainders[idx]   = nSeats*votes[0,idx]/np.sum(votes[0,:-1]) - distribution[idx]
    sorted = np.argsort(remainders)
    # Attributes remaining seats
    for idx in sorted[::-1]:
        if np.sum(distribution)==nSeats:
            break
        distribution[idx] += 1

    if detailed_print:
        for idx in range(nParties):
            print("Party: {}  Seats: {}".format(parties[idx],int(distribution[idx])))
    return distribution

def dhondt(votes,parties,nSeats,detailed_print=False):
    nParties= len(parties)
    if detailed_print:
        print("------------------------")
        print("D'Hondt model")
    # For D'Hondt model
    denominators_hondt  = range(1,nSeats)
    ratios              = np.zeros([nParties,len(denominators_hondt)])
    # Apply the several rounds (ratio by 1, 2, 3...)
    for idx,denominator in enumerate(denominators_hondt):
        ratios[:,idx] = votes/denominator
    # Sort the values
    sorted = np.sort(np.reshape(ratios,(-1)))
    # Take the nSeats-th largest
    limit  = sorted[-nSeats]
    # Deduce the selected MPs
    selected     = ratios>=limit
    distribution = np.sum(selected,axis=1)
    if detailed_print:
        for idx in range(nParties):
            print("Party: {}  Seats: {}".format(parties[idx],distribution[idx]))
    return distribution

def slague(votes,parties,nSeats,detailed_print=False):
    if detailed_print:
        print("------------------------")
        print("Sainte Lague model")
    # For Sainte Lague model
    denominators_lague  = range(1,2*nSeats,2)
    ratios              = np.zeros([nParties,len(denominators_lague)])
    # Apply the several rounds (Falseratio by 1, 3, 5...)
    for idx,denominator in enumerate(denominators_lague):
        ratios[:,idx] = votes/denominator
    # Sort the values
    sorted = np.sort(np.reshape(ratios,(-1)))
    # Take the nSeats-th largestdhondt
    limit  = sorted[-nSeats]
    # Deduce the selected MPs
    selected     = ratios>=limit
    distribution = np.sum(selected,axis=1)
    if detailed_print:
        for idx in range(nParties):
            print("Party: {}  Seats: {}".format(parties[idx],distribution[idx]))
    return distribution

def mslague(votes,parties,nSeats,detailed_print=False):
    if detailed_print:
        print("------------------------")
        print("Modified Sainte Lague model")
    # For Sainte Lague model
    denominators_lague  = range(1,2*nSeats,2)
    ratios              = np.zeros([nParties,len(denominators_lague)])
    # Apply the several rounds (ratio by 1.4, 3, 5...)
    for idx,denominator in enumerate(denominators_lague):
        if idx==0:
            denominator=1.4
        ratios[:,idx] = votes/denominator
    # Sort the values
    sorted = np.sort(np.reshape(ratios,(-1)))
    # Take the nSeats-th largest
    limit  = sorted[-nSeats]
    # Deduce the selected MPs
    selected     = ratios>=limit
    distribution = np.sum(selected,axis=1)
    if detailed_print:
        for idx in range(nParties):
            print("Party: {}  Seats: {}".format(parties[idx],distribution[idx]))
    return distribution

def danish(votes,parties,nSeats,detailed_print=False):
    if detailed_print:
        print("------------------------")
        print("Danish model")
    # For Danish model
    denominatorms_danish = range(1,6*nSeats,3)
    ratios              = np.zeros([nParties,len(denominatorms_danish)])
    # Apply the several rounds (ratio by 1, 4, 7...)
    for idx,denominator in enumerate(denominatorms_danish):
        ratios[:,idx] = votes/float(denominator)
    # Sort the values
    sorted = np.sort(np.reshape(ratios,(-1)))
    # Take the nSeats-th largest
    limit  = sorted[-nSeats]
    # Deduce the selected MPs
    selected     = ratios>=limit
    distribution = np.sum(selected,axis=1)
    if detailed_print:
        for idx in range(nParties):
            print("Party: {}  Seats: {}".format(parties[idx],int(distribution[idx])))
    return distribution

assignation_models =  {'dhondt':dhondt,'slague':slague,'mslague':mslague,'danish':danish,'hare':hare,'hagenbach':hagenbach}
