import numpy as np
import pandas as pd

national                 = False
method                   = 'dhondt'
minquota                 = 0.03
minquota_applied_locally = False
detailed                 = False
nSeats                   = 300

def hagenbach(votes,parties,nSeats):
    nParties= len(parties)
    if detailed:
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

    if detailed:
        for idx in range(nParties):
            print("Party: {}  Seats: {}".format(parties[idx],int(distribution[idx])))
    return distribution

def hare(votes,parties,nSeats):
    nParties= len(parties)
    if detailed:
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

    if detailed:
        for idx in range(nParties):
            print("Party: {}  Seats: {}".format(parties[idx],int(distribution[idx])))
    return distribution

def dhondt(votes,parties,nSeats):
    nParties= len(parties)
    if detailed:
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
    if detailed:
        for idx in range(nParties):
            print("Party: {}  Seats: {}".format(parties[idx],distribution[idx]))
    return distribution

def slague(votes,parties,nSeats):
    if detailed:
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
    if detailed:
        for idx in range(nParties):
            print("Party: {}  Seats: {}".format(parties[idx],distribution[idx]))
    return distribution

def mslague(votes,parties,nSeats):
    if detailed:
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
    if detailed:
        for idx in range(nParties):
            print("Party: {}  Seats: {}".format(parties[idx],distribution[idx]))
    return distribution

def danish(votes,parties,nSeats):
    if detailed:
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
    if detailed:
        for idx in range(nParties):
            print("Party: {}  Seats: {}".format(parties[idx],int(distribution[idx])))
    return distribution

df = pd.read_excel('VotosEstadoPartido-2021.xlsx')
models = {'dhondt':dhondt,'slague':slague,'mslague':mslague,'danish':danish,'hare':hare,'hagenbach':hagenbach}
parties = df.columns[2:-2]
nParties= len(parties)
nationalVote = np.zeros(nParties)
for idx,party in enumerate(parties):
    nationalVote[idx]=np.sum(df[party])
totalVotes    = np.sum(nationalVote)

# Nation-wide analysis
if national:
    # Eliminate parties with <3%
    for idx in range(nParties):
        if nationalVote[idx]/totalVotes<minquota:
            nationalVote[idx]=0
    # No vote for the null votes :)
    nationalVote[-1]=0
    models[method](nationalVote,parties,nSeats)

# State wise analysis
else:
    nationalDistribution = np.zeros(nParties)
    if minquota_applied_locally==False:
        # Eliminate parties with <3%
        for idx in range(nParties):
            if nationalVote[idx]/np.sum(nationalVote)<minquota:
                nationalVote[idx]=0

    # Cycle over the states
    for state in df['Estado']:
        votes         = df.loc[df['Estado'] == state]
        seatsForState = votes['Diputados'].values[0]
        votes = np.array(votes.iloc[:,2:-2])
        if minquota_applied_locally:
            # Eliminate parties with <3%
            for idx in range(nParties):
                if votes[0,idx]/np.sum(votes)<minquota:
                    votes[0,idx]=0
        else:
            # Eliminate parties with <3% nationally
            for idx in range(nParties):
                if nationalVote[idx]==0:
                    votes[0,idx]=0

        # No vote for the null votes :)
        votes[0,-1] = 0
        if detailed:
            print('-----------------------')
            print('State: {} {}'.format(state,seatsForState))
            print(votes)
        nationalDistribution += models[method](votes,parties,seatsForState)
    print('---------------')
    print('Method {} '.format(method))
    for idx in range(nParties-1):
        print("Party: {}  Seats: {}".format(parties[idx],int(nationalDistribution[idx])))
    print('Total seats {}'.format(int(np.sum(nationalDistribution))))

print('---------------')
print('Correction ')
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
        print('Adding a seat for {}'.format(parties[mostNeededParty]))
        for idx in range(nParties-1):
            propVote  = nationalVote[idx]/np.sum(nationalVote[:-1])
            overrepresentation[idx] = nationalDistribution[idx]-propVote*np.sum(nationalDistribution)
    else:
        break
print('---------------')
print('After correction ')
print('Over representation {}'.format(overrepresentation))
for idx in range(nParties-1):
    print("Party: {}  Seats: {}".format(parties[idx],int(nationalDistribution[idx])))
print('Total seats {}'.format(int(np.sum(nationalDistribution))))
