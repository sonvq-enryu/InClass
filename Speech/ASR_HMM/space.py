import numpy as np
import scipy.stats as stats

class HMM:
    def __init__(self, num_states):
        self.N = num_states
        self.prior = None
        self.transition = None
        self.emission = None

    def _forward(self, obs):
        alpha = np.zeros((T, self.N))
        alpha[0, :] = self.prior.ravel() * self.emission[obs[0], :]
        alpha[0, :] = alpha[0, :] / np.sum(alpha[0, :])
        T = len(obs)
        
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

    def _normalize(self, x):
        return x / np.sum(x)
    
    def _stochasticize(self, x):
        return x / np.sum(x, axis=1)
        
    def _em_init(self, obs):
        pass

    def _em_step(self, obs):
        T = len(obs)
        xi_sum = np.zeros((self.N, self.N))
        gamma = np.zeros((self.N, T))

        alpha = self._forward(obs)
        beta = self._backward(obs)
        
        for t in range(T-1):
            partial_sum = self.transition * np.dot(
                alpha[t, :].reshape(-1, 1),
                (self.emission[obs[t+1], :] * beta[t+1, :]).reshape(1, -1)
            )

            xi_sum += self._normalize(partial_sum)
            partial_g = alpha[t, :] * beta[t, :]
            gamma[t, :] = self._normalize(partial_g)
        
        partial_g = alpha[:, -1] * beta[:, -1]
        gamma[:, -1] = self._normalize(partial_g)

        self.prior = gamma[:, 0]
        self.transition = self._stochasticize(xi_sum)