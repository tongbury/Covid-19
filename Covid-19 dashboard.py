import pandas as pd

# Extract raw github csv from JHU
confirmed_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
death_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
recovered_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'

# read all the csv
confirmed_df = pd.read_csv(confirmed_url)
death_df = pd.read_csv(death_url)
recovered_df = pd.read_csv(recovered_url)

# assign name to the df (useful later)
confirmed_df.name = 'confirmed_df'
death_df.name = 'death_df'
recovered_df.name = 'recovered_df'

all_df = [confirmed_df, death_df, recovered_df]

# get all the countries available in all 3 files
def all_countries():
    # find the unique countries in all 3 dfs
    total_countries_available = pd.concat([confirmed_df['Country/Region'], death_df['Country/Region'], recovered_df['Country/Region']]).unique()
    column_name = pd.concat([confirmed_df['Country/Region'], death_df['Country/Region'], recovered_df['Country/Region']]).name
    return column_name, total_countries_available
# all_countries()

# file and country specific cleaning test
def cleaning_data2(df_type = confirmed_df, country = ['Malaysia'], window = 7 ):
    df_countries = df_type[df_type['Country/Region'].isin(country)]    
    df_countries_numbers = df_countries.groupby(by = 'Country/Region')[df_countries.iloc[:,4:].columns].sum()
    df_countries_numbers = df_countries_numbers.T
    # Cleaning to daily cases will be more meaningful
    df_countries_daily_numbers = df_countries_numbers.diff()
    # Get the 7-day rolling average of the daily cases as well
    df_countries_daily_rolling_average = df_countries_daily_numbers.rolling(window = window).mean()
    df_countries_daily_rolling_average = df_countries_daily_rolling_average.rename_axis(index = 'Date', columns = None)
    df_countries_daily_rolling_average.index = pd.to_datetime(df_countries_daily_rolling_average.index).strftime('%Y-%m-%d') # convert the index date to DateTime object with the required format
    return df_countries_daily_rolling_average

# cleaning_data2(confirmed_df, ['United Kingdom', 'Malaysia', 'US', 'Singapore'])

# format the table numbers to make them easier to read
#def format_numbers(num):
#    num = float(f'{num:.3g}')
#    # print(num)
#    magnitude = 0
#    while abs(num) >= 1000:
#        magnitude += 1
#        num /= 1000.0
#    # print(num)
#    # print('{}'.format('{:f}'.format(num).rstrip('0').rstrip('.')))
#    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

#format_numbers(190000000)
    
# Get all countries cumulative cases
def total_cases_all_countries(df_type):
    total_cases_country = df_type.iloc[:,-1]  # get the last column (which is the cumulative cases of each country) of the df. Output: Series
    total_cases_all_countries = df_type[['Country/Region', total_cases_country.name]]  # get only the 'Country/Region' column and last column from the df
    total_cases_all_countries = total_cases_all_countries.groupby(by = 'Country/Region').sum().reset_index()  # as there can be multiple same countries in the rows, group them together and sum their cases
    total_cases_all_countries.rename(columns = {total_cases_all_countries.columns[-1]: 'Cases'}, inplace=True)  # rename the column to 'Cases' and replace the old column name
#    total_cases_all_countries['Cases'] = total_cases_all_countries['Cases'].apply(lambda x: format_numbers(x))
    return total_cases_all_countries

#total_cases_all_countries(confirmed_df)
    
# Use plotly to plot the cleaned data

# for graphing
import plotly.express as px
# to place where the plot renders
import plotly.io as pio

# view plots in browser tab
pio.renderers.default = 'browser' # for pdf -> install orca first; for browser view -> easiest

def generate_plot(df_type, country, window):
    data = cleaning_data2(df_type = df_type, country = country, window = window)  # get the daily breakdown of cases of the country
    figure = px.line(data, y = country,  # plot for multiple countries line graphs
                     title = f"{window}-day moving average daily new {df_type.name.split('_', 1)[0]} cases",
                     template = "simple_white",
                     width = 900,
                     height = 500)
    figure.update_xaxes(title_text = "Timeline", dtick = "M1", showgrid = False)  # step of x-ticks is 1 month
    figure.update_yaxes(title_text = "Cases", showgrid = True, gridcolor = 'Black')
    figure.update_layout(title = {'x': 0.5}, hovermode = "x", legend_title = "Country", legend_title_font = {'size': 16})  # hover in the line with x appearing below for better visuals
    figure.update_traces(hovertemplate = '%{y}') # Variables are inserted using %{variable}; in this case is 'country'
    return figure

# generate_plot(confirmed_df, ['United Kingdom', 'Malaysia', 'US', 'Singapore'], 7)
# plot_bgcolor = '#F2DFCE'

## DASH

import dash
from dash.dependencies import Input, Output, State
#from dash.exceptions import PreventUpdate
import dash_table
import dash_core_components as dcc
import dash_html_components as html
# create the DASH app with current notebook codes (__name__)
import dash_bootstrap_components as dbc
# MUST add the dbc themes for dbc components to work!
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

# chrome tab title
app.title = 'Covid-19 dashboard'

def generate_header():
    # use html H1 (top heading)
    header = html.H1(children = 'Covid-19 Explorer', style = {'text-align': 'center'})
    return header

all_metrics = ['Confirmed cases', 'Death cases', 'Recovered cases']

def metric_options_generator():
    options = []
    [options.append({'label': metric, 'value': metric}) for metric in all_metrics]
# Alternatively: (for loop method)
#     for metric in all_metrics:
#         option = {'label': metric, 'value': metric}
#         options.append(option)
    return options

# metric_options_generator()

def metric_dropdown():
    dropdown = dcc.Dropdown(id = 'metric_dropdown1', 
                            options = metric_options_generator(), 
                            value = 'Confirmed cases',
                            style = {'width': '80%'}
                           # style = {'margin-left': 'auto', 'margin-right': 'auto'}
                           )
    return dropdown
# 'width': '40%'
# style = {'width': '50%'})
from dash_table.Format import Format, Scheme

def table_selection():
    table_selection = dash_table.DataTable(
                    id = 'datatable1',
                    columns = [
                        {"name": 'Country/Region', "id": 'Country/Region', "deletable": False, "selectable": True},
                        # format data ONLY at dash table function to allow the sorting functionality to happen
                        dict(name = 'Cases', id ='Cases', deletable = False, selectable = True, type = 'numeric',
                         format = Format(precision = 3, scheme = Scheme.decimal_si_prefix))
                    ],
                    data = total_cases_all_countries(confirmed_df).to_dict('records'), # the contents of the table (list of dictionaries)
                    editable = False, # do not allow edit data
                    filter_action = "native", # allow filter of data by user, else "none" to deactivate the function
                    sort_action = "native", # enables data to be sorted, else "none" to deactivate the function
                    sort_mode = "multi",
                    column_selectable = False, # can able to tick "multi" or "single" columns; false -> not selectable 
                    row_selectable = "multi",  # can able to tick "multi" or "single" rows
                    row_deletable = False,  # "False" to not allow deletion of date 
                    selected_columns = [],
                    selected_rows = [1],   # list of row numbers to be selected as default
                    page_action = "none",  # all the data is passed to the table altogether in a single page; none -> not passed in a single page
                    style_cell = {'whiteSpace': 'normal'},
                    style_table = {'height': '500px','overflowY': 'auto'},  # allow scrolling vertically
                    fill_width = False,
                    # fixed_rows={'headers': True},
                    style_cell_conditional=[
                            {'if': {'column_id': 'Country/Region'},
                             'textAlign': 'left'
                             }],
                    style_data = {'border': 'none'},
                    style_header = {'color': '#34ebd5', 'border': 'none','whiteSpace': 'normal'}
                    )

    return table_selection
# 'backgroundColor': '#F2DFCE'
# 'overflowY': 'auto
#'width' : '350px'

def graph():
    graph = dcc.Graph(id = 'graph1', style = {'height': '500px'})# style = {'width': 500, 'height': 480}) #figure = generate_plot(confirmed_df, ['Malaysia', 'United Kingdom'], 1)
    return graph

app.layout = dbc.Container(children = [
        html.Div(children = generate_header()),
        dbc.Row(children = html.Label(children = 'Metrics'), justify = "center"),
        dbc.Row(children = [
                dbc.Col([html.Button('Select all rows', id = 'select-all-button'),
                html.Button('Deselect all rows', id = 'deselect-all-button')], width = 3),
                dbc.Col(metric_dropdown(), width={'size': 6, "offset": 1})
                ]),
        dbc.Row(children = [
                dbc.Col(table_selection(), width = dict(size = 3, offset = -1)),
                dbc.Col([graph(),dbc.Row(children = [
                                                     dbc.Col(html.Label('Select Moving Average Window')),
                                                     dbc.Col(dcc.Slider(id = 'slider1',
                                                                 min = 1,
                                                                 max = 14,
                                                                 step = None,
                                                                 marks = {1: '1',
                                                                          3: '3',
                                                                          5: '5',
                                                                          7: '7',
                                                                          10: '10',
                                                                          14: '14'
                                                                          },
                                                                 value = 7))
                                                     ]
                                         )
                         ], width = 6
                        )
                             ] # no_gutters=True
                )
        ], fluid = True, style={'backgroundColor': '#F2DFCE'}
        )
        

# Present the loggings into a log file for callback (tracking purpose)
import logging   
import importlib
#reload the logging module (for spyder)
importlib.reload(logging)

logging.basicConfig(
    # set the file name
    filename="log_messages.txt",
    # set the level to the minimum warning level (debug)
    level=logging.DEBUG,
    # display the time, level and message for every log
    format="%(asctime)s:%(levelname)s:%(message)s",
    # rewrite the log file entirely when restarting the app
    filemode="w"
    )

# App callbacks   

@app.callback(
        Output('datatable1', 'data'),
        Input('metric_dropdown1', 'value')
)
def update_table(selected_dropdown):
    for i,j in zip(all_metrics, all_df):
        if selected_dropdown == i:
            logging.debug("Updating table...")
            return total_cases_all_countries(j).to_dict('records')

@app.callback(
    Output('datatable1', 'style_data_conditional'),
    Input('datatable1', 'selected_rows')
)
def update_styles(selected_rows):
    logging.debug("Updating styles....")
    return [{'if': { 'row_index': i },
            'background_color': '#7586bd'
            } for i in selected_rows]

# update graph through ticking in the table and slider changing
@app.callback(
    Output('graph1', 'figure'),
    [Input('datatable1', 'derived_virtual_data'),
     Input('datatable1', 'derived_virtual_selected_rows'),
     Input('slider1', 'value')]
)
def update_graph1(rows, derived_virtual_selected_rows, slider_value):
    # make the table data in pandas df
    dff = pd.DataFrame(rows)
    for i in all_df:
        true_list = []
        for j in dff.columns:
            # check whether all elements are True in the jth column of dff
            true_list.append(dff[j].isin(total_cases_all_countries(i)[j]).all())
            
        # if all elements in true_list are True, then generate the plot of the selected countries
        if all(true_list):
            logging.debug("Updating graph...")
            figure = generate_plot(i, dff['Country/Region'][derived_virtual_selected_rows].tolist(), slider_value)
        else:
            logging.debug("Graph not updated...")
            pass
    return figure

@app.callback(
    [Output('datatable1', 'selected_rows')],
    [
     # when input is presented, output will pop out immediately
        Input('select-all-button', 'n_clicks'),
        Input('deselect-all-button', 'n_clicks')
    ],
    [
     # 'State' allows to pass changes without changing output immediately (not like 'Input')
        State('datatable1', 'data'),
        State('datatable1', 'derived_virtual_data'),  # contains content of data (filtered and unfiltered version) list of dictionaries
        State('datatable1', 'derived_virtual_selected_rows')
    ]
)
def select_all(select_n_clicks, deselect_n_clicks, original_rows, filtered_rows, selected_rows):
    ctx = dash.callback_context.triggered[0]
    ctx_caller = ctx['prop_id']  # is either the below 2 (select-all/deselect-all)
    if filtered_rows is not None:
        if ctx_caller == 'select-all-button.n_clicks':
            logging.debug("Selecting all rows..")
            selected_ids = [row for row in filtered_rows] # list of dictionaries
#            print(original_rows)
#            print(selected_ids)
            return [[i for i, row in enumerate(original_rows) if row in selected_ids]]  # get the row id and select all the unfiltered/filtered ones
        if ctx_caller == 'deselect-all-button.n_clicks':
            logging.debug("Deselecting all rows..")
            return [[]]

# NOTE!! If decided to stop running, need to rerun the DASH app again from the start!!
if __name__ == '__main__':
    app.run_server()
