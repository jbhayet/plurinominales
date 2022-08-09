"""
@author: JBH
@email: jbhayet@cimat.mx
"""

import numpy as np

def sanchez(nationalVote,nationalDistribution,parties,max_seats=327,detailed_print=False):
    nParties= len(parties)

    # Initialize q0
    q0 = np.sum(nationalVote)
    V  = 0
    N  = 0
    for party in range(len(parties)-1):
        # Determine the cost of adquiring one seat (in votes)
        if nationalDistribution[party]>0:
            ri = nationalVote[party]/nationalDistribution[party]
            if ri<q0:
                q0 = ri
            V += nationalVote[party]
            N += nationalDistribution[party]
    if N>=max_seats:
        print("[ERR] Correction canot be applied")
        return nationalDistribution
    if (V/max_seats<=q0):
        print("Sanchez method: 1st case")
        for party in range(len(parties)-1):
            correction  = np.rint((nationalVote[party]/q0-nationalDistribution[party]))
            nationalDistribution[party] += correction
    else:
        print("[INFO] Sanchez method: 2nd case")
        q = (V-q0*N)/(max_seats-N)
        for party in range(len(parties)-1):
            nationalDistribution[party] +=int(np.rint((nationalVote[party]-q0*nationalDistribution[party])/q))
    return nationalDistribution

def rojas(nationalVote,nationalDistribution,parties,max_seats=500,detailed_print=False):
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
