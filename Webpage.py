from dash import html, dcc
import dash
from dash import Input, Output
import dash_bootstrap_components as dbc
from jupyter_dash import JupyterDash
from datetime import datetime as dt
import numpy as np
from dash.dash_table import DataTable, FormatTemplate, Format
import plotly.express as px

import Graph
import MonteCarlo

graph = Graph.Graph()

def get_dashtable(df, selectable = None, row_ids = None, filtering = 'none', sorting = 'none', scroll = None, 
                   editable = [], page_action = 'native', export = False, ddown = {}):
    
    row_style = [
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': '#eaf1f8'
        },
            
        ]
    
    cond_style = [
        {
            'if': {'column_id': c},
            'textAlign': 'right',
            'width': '5em',
        } for c in ['Date']
    ] + [
        {
            'if': {'column_id': c},
            'color': 'blue',
        } for c in ['Close']
    ]
    
    editable_list = []
    
    cond_format = {
        'commas'    : ['Volume'],
        'decimals'  : ['Open', 'High', 'Low'],
        'money'     : ['Close']
    }

    commas   = cond_format['commas']
    decimals = cond_format['decimals']
    money    = cond_format['money']
    formats = {
        **{m: FormatTemplate.money(3) for m in money}, 
        **{c: Format.Format(group=',') for c in commas},
        **{c: Format.Format(precision = 4, scheme = Format.Scheme.fixed) for c in decimals}
    }

    cols = [
        {'id': c, 'name': c, 'editable': True if c in editable + list(ddown.keys()) else False, 'type': 'numeric', 'format': formats[c], 
             'presentation': 'dropdown' if c in ddown.keys() else 'input'} if c in formats.keys() else
        {'id': c, 'name': c, 'editable': True if c in editable + list(ddown.keys()) else False, 
             'presentation': 'dropdown' if c in ddown.keys() else 'input'} for c in df.columns
    ]
        
    contents = DataTable(
        data=df.to_dict('records'),
        #NOTE: in order to access the id, I need a row with the id -> ID or Id will not work
        columns = cols,
        
        #style_table = {
        #    'border': 'none',
        #    'border-collapse': 'collapse',
        #    'overflowX': scroll,
        #    },

        style_table = {
            'border': 'none',
            'border-collapse': 'collapse',
            'height': 500,
            'overflowX': 'scroll',
            'overflowY': 'scroll'
            },

        fixed_rows={'headers': True, 'data': 0},
        page_size = 1000,

        style_cell={
            'border': 'none',
            'fontSize': '12px', 
            'boxShadow': '0 0',
            'height': 'auto',
            'width': 'auto',
            'whiteSpace': 'normal',
            'textAlign': 'center'
            },
        
        style_cell_conditional = cond_style,
        style_data_conditional = row_style,
        style_as_list_view = True,
        style_header={
            'border': 'none',
            'backgroundColor': 'white',
            'fontWeight': 'bold',
            'borderBottom': '1px solid black',
            'font-size' : '14px'
        },
        style_data={'whiteSpace': 'pre-line', 'height': 'auto'},
        
        # #EXTRA OPTIONS
#         filter_action   = 'none',
#         sort_action     = 'none',
#         page_action     = 'native',
#         export_format   = "xlsx" if export == True else 'none',
#         filter_options  = {'case': 'insensitive'},
#         dropdown        = ddown,

    )
    return(contents)    


class Webpage:
    
    def __init__(self):
        #self.app = JupyterDash(__name__) 
        self.app = dash.Dash(external_stylesheets=[dbc.themes.LUMEN])
        
    def server_run(self, port):
        self.app.run_server(
            debug=False,
            port=port,
            #mode = 'inline'
        )
        
    def layout(self, ticker_list, ticker_data):
        #self.ticker_options = [{'label': ticker, 'value': num} for num, ticker in enumerate(ticker_list['Ticker'])]
        #self.ticker_options = [{'label': row['Name'], 'value': row['Ticker']} for index, row in ticker_list.iterrows()]
        self.ticker_options = [{'label': name, 'value': ticker} for ticker, name in zip(ticker_list['Ticker'], ticker_list['Name'])]
        self.app.layout = html.Div(
        [
            html.H1("Simulation of Stock Prices using Geometric Brownian Motion", 
                style={'backgroundColor':"Green", 'color':'white', 'textAlign': 'center'}),
            html.Br(),
            html.P("Developed by Rohan Wadhwa (rw2912) & Abhishek Kulkarni (ask9103)", style={'font-size':'105%','textAlign': 'center'}),
            html.Br(),

            html.P("A geometric Brownian motion (GBM) (also known as exponential Brownian motion) is a \
                continuous-time stochastic process in which the logarithm of the randomly varying quantity follows a Brownian motion \
                (also called a Wiener process) with drift. It is an important example of stochastic processes satisfying a stochastic \
                differential equation (SDE); in particular, it is used in mathematical finance to model stock prices in the \
                Black–Scholes options pricing model.",
                style = {'font-size':'120%', 'textAlign': 'justify'}
            ),

            html.Br(),

            html.P("The dashboard provides us the capabilities to select a stock (ticker) to retrieve its historical price\
                data, which would then be displayed in the form of a simple line chart and the historical values for OHLC & Volume\
                will be displayed in a data table in the adjacent tab.",
                style = {'font-size':'120%', 'textAlign': 'justify'}
            ),

            html.Br(),

            html.P("To simulate the prices using GBM, inputs needed are - number of paths, number of days to forecast,\
                time steps to discretize the continuous time. The tool also helps us in pricing a European Call option \
                which requires two inputs - Risk Free Rate & Strike Price (K) of the option.",
                style = {'font-size':'120%', 'textAlign': 'justify'}
            ),

            html.Br(),

            html.P("In order to determine the price of the European Call option, we use the terminal value of the stock price\
                obtained after simulating the stock price using GBM for Number of days input. We apply the Call Option Payoff\
                formula to calculate the payoff in each scenario and the average value of all simulations is discounted back\
                to time 0 to obtain the price of the option. Needless to say, higher the number of simulations, better will be\
                the accuracy of our prediction.",
                style = {'font-size':'120%', 'textAlign': 'justify'}
            ),

            html.Br(),

            html.P("Data Source: Yahoo Finance",
                style = {'color':'grey', 'font-size':'80%', 'textAlign': 'justify'}
            ),

            html.Br(),

            html.H3("Stock Selection", style={'textAlign': 'center'}),
            html.Hr(),

            html.Br(),

            html.Div([
                dcc.Dropdown(
                    options = self.ticker_options,
                    placeholder = 'Select stock...',
                    disabled = False,
                    searchable = True,
                    multi = False,
                    id = 'select_ticker'
                )
            ], style = {'width':"50%", 'marginLeft': 'auto', 'marginRight': 'auto'}
            ),
            
            html.Br(),
            html.Br(),

            html.H3("Inputs for Monte Carlo Simulations", style={'textAlign': 'center'}),
            html.Hr(),
            
            dbc.Row([
                dbc.Col(width=True),
                
                dbc.Col([
                    dbc.Label('Enter Number of Paths'),
                    html.Br(),
                    dcc.Input(
                        type = 'number',
                        placeholder = 100,
                        min = 1, 
                        max = 1000,
                        id = 'select_paths'
                    )
                ]),

                dbc.Col(width=True),

                dbc.Col([
                    dbc.Label('Enter Number of Days'),
                    html.Br(),
                    dcc.Input(
                        type = 'number',
                        placeholder = 50,
                        min = 1, 
                        max = 100,
                        id = 'select_ts'
                    )
                ]),

                dbc.Col(width=True),

                dbc.Col([
                    dbc.Label('Enter Time Periods per Day'),
                    html.Br(),
                    dcc.Input(
                        type = 'number',
                        placeholder = 10,
                        min = 1, 
                        max = 100,
                        id = 'select_tp'
                    )
                ]),

                dbc.Col(width=True),

                dbc.Col([
                   dbc.Label('Enter Interest Rate'),
                    html.Br(),
                    dcc.Input(
                        type='number',
                        placeholder = 0.01,
                        min = 0.01, 
                        max = 0.1,
                        id = 'select_ir'
                    ) 
                ]),
                
                dbc.Col(width=True),
                
                dbc.Col([
                    dbc.Label('Enter the strike price:'),
                    html.Br(),
                    dcc.Input(
                        type='number',
                        placeholder = 130,
                        min = 0, 
                        max = 100000,
                        id = 'select_strike'
                    )
                ]),
                
                dbc.Col(width=True),
                            
            ], align = "center"),

            html.Br(),
            html.Br(),

            dbc.Tabs(
                [
                    dbc.Tab(dcc.Graph(figure=graph.plot_empty(), id = 'fig'), label="Graph"),
                    dbc.Tab(html.Div(id='table'), label="Data"),
                    dbc.Tab(dcc.Graph(figure=px.line(), id = 'monte_fig'), label="Monte-Carlo Simulations")
                ]
            ),

            html.Br(),
            html.Br(),

            html.H3("Summary", style={'textAlign': 'center'}),
            html.Hr(),
            html.Br(),

            dbc.Table([
                html.Thead(html.Tr([html.Th("Option Type"), html.Th("Option Price")]), style={'color':'white','background':"Grey"}),
                html.Tr([html.Td("European Call"), html.Td(html.Div(id='payoff'))])],
                style = {'width':"50%", "textAlign": "center", 'marginLeft': 'auto', 'marginRight': 'auto'},
                bordered = True
            ),

            html.Br(),
            html.Br(),
            
        ], style = {'border-style': 'solid', 'padding': '5em'}
        )
        
        @self.app.callback(
            [Output(component_id='fig', component_property='figure'),
            Output(component_id='monte_fig', component_property='figure'),
            Output(component_id='table', component_property='children'),
            Output(component_id='payoff', component_property='children')],
            [Input(component_id='select_ticker', component_property='value'),
            Input(component_id='select_paths', component_property='value'),
            Input(component_id='select_ts', component_property='value'),
            Input(component_id='select_tp', component_property='value'),
            Input(component_id='select_ir', component_property='value'),
            Input(component_id='select_strike', component_property='value')]
        )
        def update_graph(ticker, paths, ts, tp, ir, strike):
            df_ticker = ticker_data['Close'][[ticker]].dropna()
            NoOfPaths = paths
            Timesteps = ts
            T = tp
            r = ir
            K = strike
            sigma = np.std(np.log1p(df_ticker.pct_change()))#np.std(df_ticker)/100
            S0 = df_ticker.iloc[-1].at[ticker]
            Path = MonteCarlo.MonteCarlo().PathGenerator(NoOfPaths, Timesteps, T, r, sigma[0], S0, K)
            
            monte_fig = graph.add_simulation(Path)
            
            fig = graph.add_stock(df_ticker, ticker)
            payoff = "${}".format(Path["Payoff"])
            print(payoff)
            
            df_ticker_full = ticker_data.filter([x for x in ticker_data.columns if x[1]==ticker])
            df_ticker_full = df_ticker_full.droplevel(1, axis = 1)
            df_ticker_full = df_ticker_full.reset_index()
            df_ticker_full['Date'] = df_ticker_full['Date'].map(dt.date)
            df_ticker_full['Close'] = df_ticker_full['Close'].astype(float)
            table = get_dashtable(df_ticker_full)
            return(fig, monte_fig, table, payoff)


