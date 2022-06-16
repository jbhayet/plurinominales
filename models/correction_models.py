"""
@author: JBH
@email: jbhayet@cimat.mx
"""

import numpy as np

def sanchez(nationalVote,nationalDistribution,parties,detailed_print=False):
    nParties= len(parties)
    mu0 = np.sum(nationalVote)
    for party in range(len(parties)-1):
        if nationalDistribution[party]>0:
            ri = nationalVote[party]/nationalDistribution[party]
            if ri<mu0:
                mu0 = ri
    for party in range(len(parties)-1):
        nationalDistribution[party] +=int(np.rint((nationalVote[party]-mu0*nationalDistribution[party])/mu0))
    return nationalDistribution

def rojas(nationalVote,nationalDistribution,parties,detailed_print=False):
    nParties= len(parties)
    overrepresentation = np.zeros(nParties)
    for idx in range(nParties-1):
        if nationalVote[idx]>0:
            propSeats = nationalDistribution[idx]/np.sum(nationalDistribution)
            propVote  = nationalVote[idx]/np.sum(nationalVote[:-1])
            overrepresentation[idx] = nationalDistribution[idx]-propVote*np.sum(nationalDistribution)
            print("Party: {}  Over-representation (in seats): {:.3f} or in proportion {:.3f}".format(parties[idx],overrepresentation[idx],propSeats/propVote))

    while True:
        # Check if the largest absolute overrepresentation is superior to one
        if np.max(np.abs(overrepresentation))>1.0:
            mostNeededParty = np.argmin(overrepresentation)
            nationalDistribution[mostNeededParty]+=1
            if detailed_print:
                print('Adding a seat for {}'.format(parties[mostNeededParty]))
            for idx in range(nParties-1):
                propVote  = nationalVote[idx]/np.sum(nationalVote[:-1])
                overrepresentation[idx] = nationalDistribution[idx]-propVote*np.sum(nationalDistribution)
        else:
            break
    print('---------------')
    print('After correction ')
    for idx in range(nParties-1):
        if nationalVote[idx]>0:
            propSeats = nationalDistribution[idx]/np.sum(nationalDistribution)
            propVote  = nationalVote[idx]/np.sum(nationalVote[:-1])
            overrepresentation[idx] = nationalDistribution[idx]-propVote*np.sum(nationalDistribution)
            print("Party: {}  Over-representation (in seats): {:.3f} or in proportion {:.3f}".format(parties[idx],overrepresentation[idx],propSeats/propVote))
    return nationalDistribution

correction_models =  {'rojas':rojas,'sanchez':sanchez}
