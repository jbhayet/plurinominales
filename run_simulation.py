import numpy as np
import pandas as pd
from models.assignation_models import *

national                 = False
method                   = 'dhondt'
minquota                 = 0.03
minquota_applied_locally = False
detailed                 = False
nSeats                   = 300

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
