import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

class Graph:
    
    def __init__(self):
        self.fig = go.Figure()
        self.monte_fig = go.Figure()
        
    def plot_empty(self):
        self.fig.update_layout(
            title = {
                'text': 'Historical Stock Prices',
                'y': 0.95,
                'x': 0.5,
                'font': {'size': 22}
            },
            paper_bgcolor = '#ededed',
            plot_bgcolor = '#ededed',
            autosize = True,
            #height = 400,
            xaxis = {
                'title': 'Closing Date',
                'showline': True, 
                'linewidth': 1,
                'linecolor': 'black',
                'gridcolor': '#ededed',
                'rangemode': 'tozero'
            },
            yaxis = {
                'title': 'Price ($)',
                'showline': True, 
                'linewidth': 1,
                'linecolor': 'black',
                'gridcolor': '#ededed',
                'rangemode': 'tozero'
            }
        )

        self.fig.update_layout(
            xaxis=dict(
                rangeselector = dict(
                    buttons = list([
                        dict(count=1,
                             label="1m",
                             step="month",
                             ),
                        dict(count=6,
                             label="6m",
                             step="month",
                             ),
                        dict(count=1,
                             label="1y",
                             step="year",
                             ),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type="date"
            )
        )
        return self.fig
    
    def add_stock(self, df_ticker, name):
        self.fig.data = []
        self.fig.add_trace(go.Scatter(y = df_ticker.iloc[:,0].to_list(), x = df_ticker.index.to_list(), name = name))
        self.fig.update_layout(
            title = {'text': 'Historical Stock Prices'},
            showlegend = True)
        
        return self.fig
    
    def add_simulation(self, Path):
        self.monte_fig = px.line(pd.DataFrame(Path["S"].T), 
            labels = {"index":"# Days", "value": "Simulated Price", "variable": "Simulations"})
        self.monte_fig.update_layout(
            title = {
                'text': 'Monte Carlo Simulations', 
                'x':0.5, 
                'font' : {'size':22}},
            paper_bgcolor = '#ededed',
            plot_bgcolor = '#ededed',
            #grid='Black',    
            autosize = True,
            showlegend = False)

        self.monte_fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey', linecolor='black')
        self.monte_fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey', linecolor='black')
        
        return self.monte_fig