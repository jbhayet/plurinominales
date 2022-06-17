# Import Library
import matplotlib.pyplot as plt
import numpy as np

def visualizeParliament(parties,nationalDistribution,args):
    # Create Subplot
    fig = plt.figure(figsize=(8,6),dpi=100)
    ax = fig.add_subplot(1,1,1)
    seats = nationalDistribution[nationalDistribution>0].tolist()
    names = parties[nationalDistribution>0].tolist()
    colors = ['blue', 'red', 'yellow','green','red','orange','purple','white']
    explodeTuple = (0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.0)
    for i in range(len(names)):
        names[i] += ": {}".format(int(seats[i]))
    # Colors
    seats.append(sum(nationalDistribution))
    names.append("")
    # Plot
    ax.pie(seats, colors=colors, explode=explodeTuple)
    ax.legend(bbox_to_anchor=(1, 1), loc='upper left', labels=names)
    ax.set_title('Composition of the Parliament')
    # Add artist
    ax.add_artist(plt.Circle((0, 0), 0.6, color='white'))
    plt.figtext(0.3,0.35,"Method for assignation: {}".format(args.method))
    plt.figtext(0.3,0.3,"Method for correction: {}".format(args.correction_method))
    plt.figtext(0.3,0.25,"Total number of MPs: {}".format(int(np.sum(nationalDistribution))))

    # Display
    plt.show()
