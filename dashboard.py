from dash import Dash
from dash.dependencies import Input, Output
from dash_core_components import Dropdown, Graph
from dash_html_components import H1, Div, P
from peewee import fn

from src.database import LastPackage, Package, PackageHistory

dash_app = Dash(__name__)
server = dash_app.server

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
            className='wrapper',
            children=[
                Graph(
                    id='graph_license',
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
                                    children='Select package',
                                    className='menu-title',
                                ),
                                Dropdown(
                                    id='package_history',
                                    className='dropdown',
                                ),
                            ],
                        ),
                    ],
                ),
                Div(
                    className='wrapper',
                    children=[
                        Graph(
                            id='graph_package_history',
                            config={'displayModeBar': False},
                        )
                    ],
                ),
                Div(
                    className='wrapper',
                    children=[
                        Graph(
                            id='python_history',
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
    Output('graph_lines_value', 'figure'),
    Input('group', 'value'),
    Input('package', 'value'),
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
                'text': 'SLOC-package x Cocomo-Value (110.140)',
                'x': 0.05,
                'xanchor': 'left',
            }
        },
    }


@dash_app.callback(
    Output('package_history', 'options'),
    Input('package_history', 'value'),
)
def history(package_history):
    return [
        {'label': p.name, 'value': p.name}
        for p in Package.select().order_by(Package.name)
    ]


@dash_app.callback(
    Output('graph_package_history', 'figure'),
    Input('package_history', 'value'),
)
def package_history(package):
    query = (
        PackageHistory.select()
        .join(Package)
        .where(Package.name == package)
        .order_by(PackageHistory.date)
    )

    wheel_query = query.where(PackageHistory.package_type == 'wheel')
    tar_query = query.where(PackageHistory.package_type == 'tar')
    return {
        'data': [
            {
                'y': [d.total_lines for d in wheel_query],
                'x': [d.date for d in wheel_query],
                'name': 'Wheel',
            },
            {
                'y': [d.total_cost for d in wheel_query],
                'x': [d.date for d in wheel_query],
                'name': 'Cocomo wheel',
            },
            {
                'y': [d.total_lines for d in tar_query],
                'x': [d.date for d in tar_query],
                'name': 'Tar',
            },
            {
                'y': [d.total_cost for d in tar_query],
                'x': [d.date for d in tar_query],
                'name': 'Cocomo tar',
            },
        ],
        'layout': {
            'title': {
                'text': 'Package history',
                'x': 0.05,
                'xanchor': 'left',
            }
        },
    }


@dash_app.callback(
    Output('graph_license', 'figure'),
    Input('group', 'value'),
)
def license(value):
    query = (
        Package.select(
            Package.license, fn.COUNT(Package.id).alias("license_count")
        )
        .join(LastPackage)
        .where(LastPackage.group == value)
        .group_by(Package.license)
    )
    return {
        'data': [
            {
                'x': [x.license_count for x in query],
                'y': [x.license for x in query],
                'type': 'bar',
                'orientation': 'h',
            },
        ],
        'layout': {
            'title': {
                'text': 'License type',
                'x': 0.05,
                'xanchor': 'left',
            }
        },
    }


@dash_app.callback(
    Output('python_history', 'figure'),
    Input('package_history', 'value'),
)
def python(value):
    query = (
        PackageHistory.select().join(Package).where(Package.name == 'python')
    )
    return {
        'data': [
            {
                'x': [x.version for x in query],
                'y': [x.total_cost for x in query],
                'type': 'bar',
            },
        ],
        'layout': {
            'title': {
                'text': 'Python version',
                'x': 0.05,
                'xanchor': 'left',
            }
        },
    }


# dash_app.run_server(debug=True)
