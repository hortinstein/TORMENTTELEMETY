import dash
from dash import dcc, html, Input, Output
import requests
import json

app = dash.Dash(__name__)

runner_ids = [
    'd8eea9c2-d2f2-4a0b-b4e1-3508809fd951',
    '60188132-b459-4b15-bdd6-9f0259a28926',
    'f08743dd-1fcf-4001-8e27-d97e03152b6e',
]

app.layout = html.Div([
    html.H1('Runner Splits', className="text-2xl mb-4"),
    dcc.Interval(
        id='interval-component',
        interval=10 * 1000,  # in milliseconds
        n_intervals=0
    ),
    html.Table(
        id='splits-table',
        children=[
            html.Tbody(id='table-body', className="border-t border-b"),
        ],
        className="w-full border-collapse"
    ),
])

@app.callback(
    Output('table-body', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_splits_table(n_intervals):
    splits_table = []

    # Create the header row with increased spacing
    splits_table.append(html.Tr([
        html.Th('   Name   ', className="px-8 py-2 bg-gray-200"),
        html.Th('   Split Name   ', className="px-8 py-2 bg-gray-200"),
        html.Th('   Time of Day  ', className="px-8 py-2 bg-gray-200"),
        html.Th('  Pace  - ', className="px-8 py-2 bg-gray-200"),
        html.Th('   Elapsed Time   ', className="px-8 py-2 bg-gray-200")
    ]))
    
    for runner_id in runner_ids:
        api_url = f'https://api.enmotive.grepcv.com/prod/events/2023-uw-medicine-seattle-marathon-and-half-marathon/{runner_id}'
        
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = json.loads(response.json()["body"])
            print(data)
            if data.get('result', {}).get('splits'):
                runner_name = f"{data['firstname']} {data['lastname']}"
                splits_data = data['result']['splits']
                for split in splits_data:
                    splits_table.append(html.Tr([
                        html.Td(runner_name, className="px-8 py-2"),
                        html.Td(split['name'], className="px-8 py-2"),
                        html.Td(split['time_of_day'], className="px-8 py-2"),
                        html.Td(split['pace'], className="px-8 py-2"),
                        html.Td(split['time'], className="px-8 py-2"),
                    ]))
            else:
                print(f"No splits found for runner: {runner_id}")

        except Exception as e:
            print(f"Error fetching data for runner {runner_id}: {str(e)}")
    
    return splits_table

if __name__ == '__main__':
    app.run_server(debug=True)
