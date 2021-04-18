from dash import Dash
from dash.dependencies import Input, Output
from dash_core_components import Dropdown, Graph
from dash_html_components import H1, Div, P

from src.database import LastPackage, Package, PackageHistory

dash_app = Dash(__name__)

dash_app.layout = Div(
    children=[
        Div(
            className='header',
            children=[
                P(children='📈', className='header-emoji'),
                H1(children='COCOMO-PYTHON', className='header-title'),
                P(
                    children='''
                    A simple analysis of packages in pypi.
                    ''',
                    className='header-description',
                ),
                P(
                    children='https://github.com/dunossauro/cocomo-python',
                    className='header-description',
                ),
            ],
        ),
        Div(
            className='menu',
            children=[
                Div(
                    className='dropdown',
                    children=[
                        Div(children='Select Group', className='menu-title'),
                        Dropdown(
                            id='group',
                            className='dropdown',
                        ),
                    ],
                ),
                Div(
                    className='dropdown',
                    children=[
                        Div(
                            children='Select packages', className='menu-title'
                        ),
                        Dropdown(
                            id='package',
                            className='dropdown',
                            multi=True,
                        ),
                    ],
                ),
            ],
        ),
        Div(
            className='wrapper',
            children=[
                Graph(
                    id='graph_lines_value',
                    config={'displayModeBar': False},
                )
            ],
        ),
        Div(
            className='graph-header',
            children=[
                Div(
                    className='menu2',
                    children=[
                        Div(
                            className='dropdown',
                            children=[
                                Div(
                                    children='Select package', className='menu-title'
                                ),
                                Dropdown(
                                    id='xpto',
                                    className='dropdown',
                                    multi=True,
                                ),
                            ],
                        ),
                    ],
                ),
                Div(
                    className='wrapper',
                    children=[
                        Graph(
                            id='graph_lines_value2',
                            config={'displayModeBar': False},
                        )
                    ],
                ),
            ],
        ),
    ]
)


@dash_app.callback(
    Output('group', 'options'),
    Input('group', 'search_value'),
)
def update_groups(search_value):
    return [
        {'label': p.group.capitalize(), 'value': p.group}
        for p in LastPackage.select().group_by(LastPackage.group).execute()
    ]


@dash_app.callback(
    Output('package', 'options'),
    Input('group', 'value'),
)
def update_packages(search_value):
    return [
        {'label': p.name.name.capitalize(), 'value': p.name.name}
        for p in LastPackage.select().where(LastPackage.group == search_value)
    ]


@dash_app.callback(
    Output(component_id='graph_lines_value', component_property='figure'),
    Input(component_id='group', component_property='value'),
    Input(component_id='package', component_property='value'),
)
def lines_price(group, package):
    if not package:
        query = LastPackage.select().where(LastPackage.group == group)
    else:
        query = (
            LastPackage.select().join(Package).where(Package.name.in_(package))
        )
    return {
        'data': [
            {
                'y': [d.name.name for d in query],
                'x': [d.total_lines for d in query],
                'name': 'Code Lines',
                'type': 'bar',
                'orientation': 'h',
            },
            {
                'y': [d.name.name for d in query],
                'x': [d.total_cost for d in query],
                'name': 'Cocomo',
                'type': 'bar',
                'orientation': 'h',
            },
        ],
        'layout': {
            'title': {
                'text': 'SLOC-package x Cocomo-Value (100.000)',
                'x': 0.05,
                'xanchor': 'left',
            }
        },
    }


dash_app.run_server(debug=True)
