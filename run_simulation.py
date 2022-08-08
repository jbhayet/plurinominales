"""
@author: JBH
@email: jbhayet@cimat.mx
"""
import numpy as np
import pandas as pd
import argparse, sys
from models.assignation_models import *
from models.correction_models import *
from utils.graphs import *

minquota_applied_locally = False

# Parser arguments
parser = argparse.ArgumentParser(description='Simulate the assignation of MPs in the Mexican Parliament based on different models')
parser.add_argument('--national',
                    action='store_true',
                    help='does the assignation nation-wide (and not state-wide)')
parser.add_argument('--method','-m',
                    default='dhondt',
                    choices=['dhondt', 'slague', 'mslague', 'danish','hare','hagenbach','majority'],
                    help='specify the assignation method (default: "D Hondt")')
parser.add_argument('--correction_method','-c',
                    default='none',
                    choices=['rojas', 'sanchez','none'],
                    help='specify the correction method (default: "none")')
parser.add_argument('--detailed_output',
                    action='store_true',
                    help='prints intermediate results in each method')
parser.add_argument('--minpc',
                    type=float, default=.03, metavar='N',
                    help='minimal percentage of the expressed votes to be eligible for the MPs assignation (default: .03)')
parser.add_argument('--seats',
                    type=int,
                    default=300,
                    help='base number of seats to be assigned (default: 300)')
parser.add_argument('--max_seats',
                    type=int,
                    default=500,
                    help='maximum number of seats to be assigned. used by sanchez correction method (default: 500)')
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
    # Apply the assignation method nation-wide
    nationalDistribution = assignation_models[args.method](nationalVote,parties,args.seats,args.detailed_output)

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
print('Initial assignation with {} method'.format(args.method))
for idx in range(nParties-1):
    print("Party: {}  Seats: {}".format(parties[idx],int(nationalDistribution[idx])))
print('Total seats {}'.format(int(np.sum(nationalDistribution))))


if args.correction_method!='none':
    print('---------------')
    print('Correction with {} method'.format(args.correction_method))
    nationalDistribution = correction_models[args.correction_method](nationalVote,nationalDistribution,parties,max_seats=args.max_seats,detailed_print=args.detailed_output)
    print('---------------')
    print('Final distribution')
    for idx in range(nParties-1):
        print("Party: {}  Seats: {}".format(parties[idx],int(nationalDistribution[idx])))
    print('Total seats {}'.format(int(np.sum(nationalDistribution))))

visualizeParliament(parties,nationalDistribution,args)
