from dash import Dash, html, dcc, page_container

app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True)

app.layout = html.Div(
    style={'backgroundColor': '#475ba3'},
    children=[
        dcc.Location(id="url"),
        page_container
    ]
)

if __name__ == '__main__':
    app.run(debug=True)