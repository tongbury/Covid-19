## Cleaning data

# # file and country specific cleaning test
# confirmed_uk = confirmed_df[confirmed_df['Country/Region'] == 'United Kingdom']
# confirmed_uk_numbers = confirmed_uk.iloc[:,4:]
# confirmed_uk_numbers = confirmed_uk_numbers.T
# # Since there will be more than one region in UK (columns) , so we sum it to represent the whole UK cases
# confirmed_uk_numbers = confirmed_uk_numbers.sum(axis = 'columns')
# # Cleaning to daily cases will be more meaningful
# confirmed_uk_daily_numbers = confirmed_uk_numbers.diff()
# # Get the 7-day rolling average of the daily cases as well
# confirmed_uk_daily_rolling_average = confirmed_uk_daily_numbers.rolling(window = 7).mean()



# # Use a custom cleaning decorator to clean the data
# from functools import wraps

# def cleaning_decorator(function): # the function here is cleaning_data
    
#     @wraps(function) # so that when __doc__ is called, function description can be called
#     def wrapper(df_type = confirmed_df, country = 'Malaysia', window = 7):
#         df_country = df_type[df_type['Country/Region'] == country]  # df filter to particular country
#         df_country_numbers = df_country.iloc[:,4:]  # get the numbers data which only starts from the 5th column
#         df_country_numbers = df_country_numbers.T  # transpose them so that dates is in the index (first column), numbers in the second column (and third or more columns because of some countries further divided to regions)
#         df_country_numbers = df_country_numbers.sum(axis = 'columns')  # aggregate the columns numbers (useful for more than 1 column numbers)
#         df_country_daily_numbers = df_country_numbers.diff()  # get the daily numbers by subtracting today with yesterday
#         df_country_daily_rolling_average = df_country_daily_numbers.rolling(window = window).mean()  # get the x-day rolling average of numbers
#         df_country_daily_rolling_average = pd.DataFrame(df_country_daily_rolling_average, columns = ['Cases']) # make it as a dataframe, with it's column named as 'Cases'
#         from datetime import datetime
#         df_country_daily_rolling_average.index = pd.to_datetime(df_country_daily_rolling_average.index).strftime('%Y-%m-%d') # convert the index date to DateTime object with the required format
#         df_country_daily_rolling_average.index.name = 'Date'  # set the index name as 'Date'
#         print(function()) # print "cleaning completed"
#         return [df_country_daily_rolling_average, country, window]  # return the following set of results 
    
#     return wrapper

# @cleaning_decorator
# def cleaning_data(df_type = confirmed_df, country = 'Malaysia', window = 7):
#     ''' 
#     Function: Daily breakdown of cases in the country
    
#     Parameters:
    
#     df_type = confirmed/death/recovered_df
#     country = country name 
#     window = x-day rolling average
#     '''
#     return "cleaning completed"

# # print(cleaning_data.__doc__)
# cleaning_data(df_type = confirmed_df, country = 'United Kingdom', window = 3)[0]



# # Total cases worldwide
# def total_cases_worldwide(df_type):
#     total_cases_worldwide = df_type.iloc[:,-1].sum()  # sum all the last columns (which is the cumulative cases of each country) of the df
#     if df_type is confirmed_df:
#         print(f'Total Confirmed: {total_cases_worldwide: ,}')  # print the cases into thousand separators
#     elif df_type is recovered_df:
#         print(f'Total Recovered: {total_cases_worldwide: ,}')
#     elif df_type is death_df:
#         print(f'Total Death: {total_cases_worldwide: ,}')

# total_cases_worldwide(confirmed_df)

# # Total cases in a country
# def total_cases_country(df_type, country):
#     df_country = df_type[df_type['Country/Region'].isin(country)]
#     total_cases_country = df_country.iloc[:,-1].sum()
#     if df_type is confirmed_df:
#         print(f'Total Confirmed in {country}: {total_cases_country}')
#     elif df_type is recovered_df:
#         print(f'Total Recovered in {country}: {total_cases_country}')
#     elif df_type is death_df:
#         print(f'Total Death in {country}: {total_cases_country}')
#     return total_cases_country
# # total_cases_country(death_df, ['Malaysia'])

# total_cases_country(confirmed_df, all_countries()[1])




#    if window == 7:
#        figure.update_traces(mode ='lines+markers')
    #figure.update_layout(hovermode="x unified")
    # figure.update_xaxes(tickangle=45,
    #     ticktext=["End of Q1", "End of Q2", "End of Q3", "End of Q4"],
    #     tickvals=["2020-04-01", "2020-07-01", "2020-10-01",data[0].index.max()])
    
    
    
    
#    if selected_dropdown == all_metrics[0]:
#        return total_cases_all_countries(all_df[0]).to_dict('records')
#    elif selected_dropdown == all_metrics[1]:
#        return total_cases_all_countries(all_df[1]).to_dict('records')
#    elif selected_dropdown == all_metric[2]:
#        return total_cases_all_countries(all_df[2]).to_dict('records')
