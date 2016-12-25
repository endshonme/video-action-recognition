import os
from optical_flow_prep import writeOpticalFlow
import pickle
import sys

# Creates a dictionary of the Classes of Videos present in the database
# and assigns them value starting from 0 alphabetically
def CreateDict(filename):
    f = open(filename,'r')
    a = f.readlines()
    d = {}
    count = 1
    for i in a:
        temp = i.split()
        i = temp[-1]
        d[i] = int(temp[0])
        count += 1
    return d

# Produces optical flow images and creates a dictionary of the files present
# with their respective classes
def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        pickleFile = "../dataset/temporal_test_data.pickle"
        print "Saving data at: ",pickleFile
    else:
        pickleFile = "../dataset/temporal_train_data.pickle"
        print "Saving data at: ",pickleFile
    training_data = {}
    types = CreateDict("../dataset/ucfTrainTestlist/classInd.txt")
    rootDir = '../dataset/ucf101'
    for root,directory,files in os.walk(rootDir):
        for filename in files:
            if '.avi' in filename:
                count = writeOpticalFlow(root,filename,150,150,1)
                print count
                folder = root.split('/')[-1]
                blockno = int(count/50)
                key = filename + '@' + str(blockno)
                training_data[key] = types[folder]
    print training_data
    with open(pickleFile,'wb') as f:
        pickle.dump(training_data,f)


if __name__ == '__main__':
    main()