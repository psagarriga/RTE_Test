
import requests
url = "https://digital.iservices.rte-france.com/token/oauth/"

data = { 'Authorization' : 'Basic ZjI3YjM5MTUtMTYzYi00OTFlLTllN2UtYWNlM2FiM2QxMjFiOjk3ZWExOGFkLTkyMDQtNGE1NC1iNmNmLTM4NTkwNmVlOTk4Nw==' ,
        'Content-Type': 'application/x-www-form-urlencoded',
       }

response = requests.post(url, headers=data)

status_code = response.status_code

print('status code =',status_code)

info_rte_token = response.json()

print('info_rte_token =', info_rte_token)

token = info_rte_token['access_token']

print('token =', token)


# ############# DEFINE DATES ##################

from datetime import datetime, timedelta

# Calculate the end date as today's date
ending_date = datetime.now()

# Calculate the start date as 10 days before the end date
starting_date = ending_date - timedelta(days=10)

# Format the dates in the required format
start_date_str = starting_date.strftime("%Y-%m-%dT%H:%M:%S%z")+"%2B02:00"
end_date_str = ending_date.strftime("%Y-%m-%dT%H:%M:%S%z")+"%2B02:00"

print (starting_date, ending_date)
print (start_date_str, end_date_str)

start_date_str = start_date_str.replace("%2B", "+")
end_date_str = end_date_str.replace("%2B", "+")
print(start_date_str)
print(end_date_str)




url = f"https://digital.iservices.rte-france.com/open_api/actual_generation/v1/actual_generations_per_production_type?start_date={start_date_str}&end_date={end_date_str}"

data = { 'Authorization' : 'Bearer '+ token,
        'Content-Type': 'application/soap+xml',
        'charset' : 'UTF-8',
       }

response = requests.get(url, headers=data)
status_code = response.status_code
print('status code =',status_code)

print ('Response')
print (response)
print (data)

data = response.json()

print (data)



# ############# PLOT ##################


# Processing the data ***********************************************

import matplotlib.pyplot as plt
import pandas as pd
import json

# Extracting values
production_types = []
dates = []
values = []

for production in data['actual_generations_per_production_type']:
    production_type = production['production_type']
    for value in production['values']:
        start_date = pd.to_datetime(value['start_date'])
        val = value['value']
        production_types.append(production_type)
        dates.append(start_date)
        values.append(val)

# Creating DataFrame ***********************************************
df = pd.DataFrame({
    'ProductionType': production_types,
    'Date': dates,
    'Value': values
})


# Pivot for easier plotting ***********************************************
df_pivot = df.pivot(index='Date', columns='ProductionType', values='Value')


'''
# Plotting **************HERE NOT PLOTTED AS SAVED HTML *********************************
plt.figure(figsize=(15, 10))
plt.plot(df_pivot.index, df_pivot, marker='', linestyle='-')
plt.title('Energy Production by Type Over Time')
plt.xlabel('Date and Time')
plt.ylabel('Energy Production (MW)')
plt.legend(df_pivot.columns, loc='upper right')
plt.xticks(rotation=45)
plt.grid(True)  # This line adds the grid to the chart
plt.tight_layout()
plt.show()
'''

# ############# SAVE PLOT ##################

import pandas as pd
import plotly.express as px

# Assuming 'df_pivot' is your DataFrame from the previous steps
df_pivot.reset_index(inplace=True)
df_melted = df_pivot.melt(id_vars='Date', var_name='ProductionType', value_name='Value')

# Creating an interactive plot with Plotly
fig = px.line(df_melted, x='Date', y='Value', color='ProductionType',
              title='Energy Production by Type Over Time')

# Adding layout adjustments similar to your matplotlib plot
fig.update_layout(
    xaxis_title='Date and Time',
    yaxis_title='Energy Production (MW)',
    legend_title='Production Type',
    xaxis_tickangle=-45,
    template='plotly_white'
)

# Export the figure as an HTML file
fig.write_html('energy_production_by_type.html')






