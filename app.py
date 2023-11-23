from dash import Dash, html

from view import main_view

app = Dash(__name__)

app.layout = html.Div(children=[
    main_view.layout
    ])
if __name__ == '__main__':
    app.run(debug=True)
    