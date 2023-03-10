# Option-Pricing-Using-MonteCarlo-Simulations
The tool also helps us in pricing a European Call option using Monte Carlo Simualtions

A geometric Brownian motion (GBM) (also known as exponential Brownian motion) is a continuous-time stochastic process in which the logarithm of the randomly varying quantity follows a Brownian motion (also called a Wiener process) with drift. It is an important example of stochastic processes satisfying a stochastic differential equation (SDE); in particular, it is used in mathematical finance to model stock prices in the Black–Scholes options pricing model.


The dashboard provides us the capabilities to select a stock (ticker) to retrieve its historical price data, which would then be displayed in the form of a simple line chart and the historical values for OHLC & Volume will be displayed in a data table in the adjacent tab.


To simulate the prices using GBM, inputs needed are - number of paths, number of days to forecast, time steps to discretize the continuous time. The tool also helps us in pricing a European Call option which requires two inputs - Risk Free Rate & Strike Price (K) of the option.


In order to determine the price of the European Call option, we use the terminal value of the stock price obtained after simulating the stock price using GBM for Number of days input. We apply the Call Option Payoff formula to calculate the payoff in each scenario and the average value of all simulations is discounted back to time 0 to obtain the price of the option. Needless to say, higher the number of simulations, better will be the accuracy of our prediction.
