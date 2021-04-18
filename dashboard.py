from dash import Dash
from dash_core_components import Graph, Dropdown
from dash_html_components import Div, P, H1
from dash.dependencies import Input, Output

from src.database import LastPackage, Package

dash_app = Dash(__name__)

dash_app.layout = Div(
    children=[
        Div(
            children=[
                Dropdown(
                    id='group',
                    options=[
                        {'label': i, 'value': i}
                        for i in set(x.group for x in LastPackage.select())
                    ],
                ),
                Graph(
                    id='xpto',
                ),
            ]
        ),
        Div(
            children=[
                Dropdown(
                    id='package',
                    options=[
                        {'label': i, 'value': i}
                        for i in set(x.name for x in Package.select())
                    ],
                ),
                Graph(
                    id='xpto2',
                ),
            ]
        ),
    ]
)


@dash_app.callback(
    Output(component_id='xpto', component_property='figure'),
    Input(component_id='group', component_property='value'),
)
def generate_graphs(group):
    x = []
    y1 = []
    y2 = []
    for p in LastPackage.select().where(LastPackage.group == group):
        y1.append(p.total_lines)
        y2.append(p.total_cost)
        x.append(p.name)

    return {
        'data': [
            {
                'y': x,
                'x': y1,
                'type': 'bar',
                'name': 'Linhas de código',
                'orientation': 'h',
            },
            {
                'y': x,
                'x': y2,
                'type': 'bar',
                'name': 'Custo estimado',
                'orientation': 'h',
            },
        ],
    }


@dash_app.callback(
    Output(component_id='xpto2', component_property='figure'),
    Input(component_id='package', component_property='value'),
)
def lib(package):
    x1 = []
    x2 = []
    x3 = []

    y1 = []
    y2 = []
    y3 = []

    for p in (
        Package.select()
        .where(
            Package.name == package,
            Package.downloaded == True,
        )
        .order_by(Package.date)
    ):
        x1.append(p.date)
        y1.append(p.total_cost)

    for p in (
        Package.select()
        .where(
            Package.name == package,
            Package.downloaded == True,
            Package.packge_type == 'wheel',
        )
        .order_by(Package.date)
    ):
        x2.append(p.date)
        y2.append(p.total_lines)

    for p in (
        Package.select()
        .where(
            Package.name == package,
            Package.downloaded == True,
            Package.packge_type == 'tar',
        )
        .order_by(Package.date)
    ):
        x3.append(p.date)
        y3.append(p.total_lines)

    return {
        'data': [
            {'x': x2, 'y': y2, 'name': 'wheel'},
            {
                'x': x1,
                'y': y1,
                'name': 'Custo estimado',
            },
            {
                'x': x3,
                'y': y3,
                'name': 'tar',
            },
        ]
    }


dash_app.run_server()
