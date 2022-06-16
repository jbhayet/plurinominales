"""
@author: JBH
@email: jbhayet@cimat.mx
"""
import numpy as np
import pandas as pd
import argparse
from models.assignation_models import *

minquota_applied_locally = False

# Parser arguments
parser = argparse.ArgumentParser(description='Simulate the assignation of MPs in the Mexican Parliament based on different models')
parser.add_argument('--national',
                    action='store_true',
                    help='does the assignation nation-wide (and not state-wide)')
parser.add_argument('--method',
                    default='dhondt',
                    choices=['dhondt', 'slague', 'mslague', 'danish','hare','hagenbach'],
                    help='specify the assignation method (default: "D Hondt")')
parser.add_argument('--detailed_output',
                    action='store_true',
                    help='prints intermediate results in each method')
parser.add_argument('--apply_correction',
                    action='store_true',
                    help='apply a correction process')
parser.add_argument('--minpc',
                    type=float, default=.03, metavar='N',
                    help='minimal percentage of the expressed votes to be eligible for the MPs assignation (default: .03)')
parser.add_argument('--seats',
                    type=int,
                    default=300,
                    help='base number of seats to be assigned (default: 300)')
args = parser.parse_args()


df = pd.read_excel('data/VotosEstadoPartido-2021.xlsx')
parties = df.columns[2:-2]
nParties= len(parties)
nationalVote = np.zeros(nParties)
for idx,party in enumerate(parties):
    nationalVote[idx]=np.sum(df[party])
totalVotes    = np.sum(nationalVote)

# Nation-wide analysis
if args.national:
    # Eliminate parties with <3%
    for idx in range(nParties):
        if nationalVote[idx]/totalVotes<args.minpc:
            nationalVote[idx]=0
    # No vote for the null votes :)
    nationalVote[-1]=0
    # Apply the assignation method
    nationalDistribution = assignation_models[args.method](nationalVote,parties,args.seats)

# State wise analysis
else:
    nationalDistribution = np.zeros(nParties)
    if minquota_applied_locally==False:
        # Eliminate parties with <3%
        for idx in range(nParties):
            if nationalVote[idx]/np.sum(nationalVote)<args.minpc:
                nationalVote[idx]=0

    # Cycle over the states
    for state in df['Estado']:
        votes         = df.loc[df['Estado'] == state]
        seatsForState = votes['Diputados'].values[0]
        votes = np.array(votes.iloc[:,2:-2])
        if minquota_applied_locally:
            # Eliminate parties with <3%
            for idx in range(nParties):
                if votes[0,idx]/np.sum(votes)<args.minpc:
                    votes[0,idx]=0
        else:
            # Eliminate parties with <3% nationally
            for idx in range(nParties):
                if nationalVote[idx]==0:
                    votes[0,idx]=0

        # No vote for the null votes :)
        votes[0,-1] = 0
        if args.detailed_output:
            print('-----------------------')
            print('State: {} {}'.format(state,seatsForState))
            print(votes)
        nationalDistribution += assignation_models[args.method](votes,parties,seatsForState)

print('---------------')
print('Method {} '.format(args.method))
for idx in range(nParties-1):
    print("Party: {}  Seats: {}".format(parties[idx],int(nationalDistribution[idx])))
print('Total seats {}'.format(int(np.sum(nationalDistribution))))


if args.apply_correction:
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
            if args.detailed_output:
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
