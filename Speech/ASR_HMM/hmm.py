import numpy as np
import scipy.stats as stats

np.seterr(divide="ignore", invalid="ignore")
np.random.seed(42)

class HMM:
    def __init__(self, n_states):
        self.N = n_states
    
    def _init_params(self):
        self.transition = np.random.randn(self.N, self.N)
        self.prior = np.random.randn(self.N, 1)

    

class HMM:
    def __init__(self, transition, emission, prior):
        """
        N : number of states (hidden states)
        M : number of observation.
        T : length of observation sequences.
        Transition matrix : (NxN) State transition matrix.
        Emission matrix   : (MxN) Emission probabilites matrix, prob of N hidden state follow visible observation
        Initial states    : (N, ) Initial states probabilites.
        """
        self.transition = transition
        self.emission = emission
        self.prior = prior
        self.N = len(transition)
        self.M = len(emission)

    def _normalize(self, x):
        return (x + (x == 0)) / np.sum(x)

    def _stochasticize(self, x):
        return x / np.sum(x, axis=1)

    def _forward(self, obs):
        """
        alpha : A matrix represent forward probability of hidden state follow visible state.
                Each row representation probability of N hidden state at time t (with 0 <= t <= T-1)  
        """
        T = len(obs) # obs is vector (T, )
        alpha = np.zeros((T, self.N))

        # Initial first row of alpha with with initial probs and emission matrix.
        alpha[0, :] = self.prior.ravel() * self.emission[obs[0], :]
        alpha[0, :] /= np.sum(alpha[0, :])

        for t in range(1, T):
            alpha[t, :] = np.dot(alpha[t-1, :], (self.transition * self.emission[obs[t], :]))
            alpha[t, :] /= np.sum(alpha[t, :])
        
        return alpha

    def _backward(self, obs):
        T = len(obs)
        beta = np.zeros((T, self.N))
        beta[-1, :] = 1

        for t in range(T-2, -1, -1):
            beta[t, :] = np.dot(self.transition, (self.emission[obs[t+1], :] * beta[t+1, :]))
            beta[t, :] /= np.sum(beta[t, :])
        
        return beta

    def _step(self, obs):
        T = len(obs)
        
        alpha = self._forward(obs)
        beta = self._backward(obs)

        xi_sum = np.zeros((self.N, self.N))
        gamma = np.zeros((T, self.N))

        for t in range(T-1):
            partial_sum = self.transition * np.dot(
                alpha[t, :].reshape(-1, 1),
                (self.emission[obs[t+1], :] * beta[t+1, :]).reshape(1, -1)
            )

            xi_sum += partial_sum
        
        gamma = alpha * beta
        self.prior = gamma[0, :]
        for v in range(self.M):
            self.emission[v, :] = np.sum(gamma[v==obs, :], axis=0)

        self.transition = xi_sum / np.sum(xi_sum, axis=1)
        self.emission /= np.sum(gamma, axis=0)
       
    def train(self, obs, epoch=5):
        for _ in range(epoch):
            self._step(obs)

    
    def fit(self, obs, epoch=5):
        T = len(obs)
        for _ in range(epoch):
            alpha = self._forward(obs)
            beta = self._backward(obs)

            xi_sum = np.zeros((self.N, self.N))
            gamma = np.zeros((T, self.N))

            for t in range(T-1):
                partial_sum = self.transition * np.dot(
                    alpha[t, :].reshape(-1, 1),
                    (self.emission[obs[t+1], :] * beta[t+1, :]).reshape(1, -1)
                )

                xi_sum += self._normalize(partial_sum)
                partial_g = alpha[t, :] * beta[t, :]
                gamma[t, :] = self._normalize(partial_g)
            
            partial_g = alpha[-1, :] * beta[-1, :]
            gamma[-1, :] = self._normalize(partial_g)

            self.prior = gamma[0, :]
            self.transition = self._stochasticize(xi_sum)

            for v in range(self.M):
                self.emission[v, :] = np.sum(gamma[v==obs, :], axis=0)

            self.emission /= np.sum(gamma, axis=0)

            
# b = np.array(((1, 3, 5), (2, 4, 6)))
# b = b / np.sum(b, axis=1).reshape((-1, 1))
# emission = b.T
# transmission = np.array([[0.5, 0.5], [0.5, 0.5]])
# init = np.array([[0.5, 0.5]])
# # observations = ['2','3','3','2','3','2','3','2','2','3','1','3','3','1','1','1','2','1','1','1','3','1','2','1','1','1','2','3','3','2','3','2','2']
# # obs = [int(i)-1 for i in observations]
# # obs = np.array(obs)
# import pandas as pd
# data = pd.read_csv('data_python.csv')
# obs = data['Visible'].values
# hmm = HMM(transmission, emission, init)
# hmm.train(obs, 100)