import dill as pickle
import os

train_dataset = os.path.join(os.getcwd(),"totalSegmentator_mergedLabel_samples/")

with open('train_dataset.pkl', 'wb') as f:
    pickle.dump(train_dataset, f)

