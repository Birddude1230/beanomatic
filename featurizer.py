import numpy as np
import glob, pickle

DISCORD_MESSAGE_SIZE = 2000

class Featurizer():
    def __init__(self):
        self.output = None
        for fl in glob.glob("*.dat"):
            with open(fl, "rb") as ds:
                data = pickle.load(ds)
                self.featurize_file(ds)

    def featurize_file(self, data):
        for j in data:
            self.featurize_message(j[0], j[1])

    def featurize_message(self, data):
        """Must take tuples of (message_content, author_id) and featurize them.
        Should return a numpy row to be added to existing data.
    
        Not implemented by default."""
        raise NotImplementedError

    def save(self, fname):
        with open(f"{fname}.npy","wb") as f:
            numpy.save(f, self.output)

class CharFeaturizer(Featurizer):
    def featurize_message(self, mtext, uid):
        nr = np.zeroes(DISCORD_MESSAGE_SIZE + 1)
        for c in range(len(mtext)):
            nr[c] = ord(mtext[c])
        nr[-1] = uid
        if self.output = None:
            self.output = nr
        else:
            self.output = np.vstack([self.output, nr])

