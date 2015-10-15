import gzip, os, cPickle
import numpy as np
import tool
from scipy.cluster.vq import kmeans, vq

path = os.path.join(os.path.realpath('..'), "data", 'mnist.pkl.gz')
with gzip.open(path, 'rb') as f:
    train_set, _, _ = cPickle.load(f)

train_count = 100
K = min(train_count, 1000)

train_x, train_y = (train_set[0][:train_count], train_set[1][:train_count])

centroids, _ = kmeans(train_x, K)
groups, _ = vq(train_x, centroids)

mu      = np.zeros((K, train_x.shape[1]))
sigma   = np.zeros((K, train_x.shape[1], train_x.shape[1]))


#
# Training
#
for j in range(K):
    selected = train_x[groups[j]]
    mu[j] = sum(selected)/selected.shape[0]
    sigma[j] = np.cov(selected.transpose()) + 0.1 * np.eye(train_x.shape[1])


H = tool.get_H(train_x, mu, sigma)
Ht = H.transpose()
Y = tool.get_Y(train_y)
W = np.linalg.inv(Ht.dot(H)).dot(Ht).dot(Y) # <- opt
