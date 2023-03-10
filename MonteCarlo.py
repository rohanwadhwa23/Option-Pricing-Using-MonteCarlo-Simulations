import numpy as np
import pandas as pd

class MonteCarlo:

    def __init__(self):
        np.random.seed(123)

    def PathGenerator(self, NoOfPaths, TimeSteps, T, r, sigma, S0, K):
        z = np.random.normal(0.0,1.0,[NoOfPaths, TimeSteps])
        X = np.zeros([NoOfPaths, TimeSteps])
        S = np.zeros([NoOfPaths, TimeSteps])
        time = np.zeros(TimeSteps)
        X[:,0] = np.log(S0)
        dt = T/float(TimeSteps)
        for i in range(len(z[0])-1):
            if(NoOfPaths>1):
                z[:,i] = (z[:,i] - np.mean(z[:,i])) / np.std(z[:,i])
            X[:,i+1] = X[:,i] + (r - 0.5*sigma*sigma)*dt + sigma*np.power(dt,0.5)*z[:,i]
            time[i+1] = time[i] + dt

        S = np.exp(X)
        Payoff = np.round(np.mean(np.maximum(S[:,-1]-K,0))*np.exp(-r*T),2)

        Paths = {"time" : time, "X" : X, "S" : S, "Payoff" : Payoff}
        return Paths