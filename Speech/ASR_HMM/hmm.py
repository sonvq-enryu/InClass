import numpy as np

class HMM(object):
    def __init__(self, transition_matrix, emission_matrix, prior_matrix):

    self.transition_matrix = transition_matrix
    self.emmistion_matrix = emission_matrix
    self.prior_matrix = prior_matrix

    def forward(self, obversation):

