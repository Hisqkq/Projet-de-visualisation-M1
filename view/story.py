import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import html, dcc

# AJOUTER D'AUTRES IMPORTS SI BESOIN

## On appellera ces fonctions dans les pages pour afficher le texte
## Ne pas hesiter a utiliser des balises html pour mettre en forme le texte et du bootstrap components pour le style ou autre 
## (faires des petites cases de texte pour chaque problematique etc...) (bootstrap components: https://dash-bootstrap-components.opensource.faculty.ai/docs/components/card/)
## (ou https://www.dash-mantine-components.com/components/card)
## Ne pas hesiter a faire plus de fonctions si besoin
## Pourquoi pas ajouter quelques images pour illustrer les propos, pour rendre le site plus vivant

def story_accueil():
    cards_content = [
        {
            "title": "Échanges d'électricité",
            "text": "Découvrez les échanges d'électricité avec les pays voisins. La France est un grand exportateur d'électricité, mais importe également de l'électricité. Le graphique en boite à moustaches montre la répartition des échanges par pays pour la date d'aujourd'hui. Pour plus de détails, cliquez sur le graphique pour accéder à la page dédiée aux échanges d'électricité.",
            "image": "/assets/echanges.jpg",
            "image_credits": "Image credits: Yan Zabolotnyi 123RF"
        },
        {
            "title": "Production d'électricité",
            "text": "Explorez la répartition de la production d'électricité par filière en France. Le graphique en secteurs visualise la contribution de chaque filière pour la date d'aujourd'hui. La France France possède un parc nucléaire important, mais les énergies renouvelables sont en plein essor. Pour plus de détails sur les production nationales et régionales, cliquez sur le graphique pour accéder à la page dédiée à la production d'électricité.",
            "image": "/assets/production.jpg",
            "image_credits": "Image credits: Getty Images/iStockphoto par gopixa"
        },
        {
            "title": "Consommation d'électricité",
            "text": "Analysez les modèles de consommation et identifiez les périodes de pic. Le graphique linéaire montre la consommation du jours avec les différentes prédictions. Pour plus de détails sur la consommation nationale et régionale, cliquez sur le graphique pour accéder à la page dédiée à la consommation d'électricité",
            "image": "/assets/consommation.jpeg",
            "image_credits": "Image credits: lovelyday12 - stock.adobe.com"
        },
    ]

    cards = [
        dmc.Card(
            shadow="sm",
            p="lg",
            style={
                "backgroundColor": "#1A1B1E", 
                "color": "white",  
                "marginBottom": 30,  
                "borderRadius": "8px",  
            },
            children=[
                dmc.Image(
                    src=card["image"],
                    height=250,
                    fit="cover",
                    style={"borderTopLeftRadius": "8px", "borderTopRightRadius": "8px"} 
                ),
                html.Div(
                    dcc.Markdown(card["image_credits"]),
                    className="image-credits",
                    style={
                        "fontSize": "0.7rem",  
                        "color": "grey",       
                        "textAlign": "center", 
                        "marginTop": "0.5rem", 
                    }
                ),
                dmc.Text(card["title"], weight=500, size="lg", style={"color": "#FFF"}),  
                dmc.Text(card["text"], style={"color": "#DDD"}), 
            ],
        )
        for card in cards_content
    ]

    cards_data_content = [
        {
            "title": "Données nationales",
            "text": "Consultez les données nationales sur la production, la consommation et les échanges d'électricité. Les données sont disponibles en temps réel et consolidées. Pour plus de détails, cliquez sur l'un des boutons ci-dessous.",
            "image": "/assets/donnees_nationales.jpg",
            "image_credits": "Image credits: Europe at night viewed from space, NASA",
            "links": [
                {"text": "Données consolidées", "href": "https://odre.opendatasoft.com/explore/dataset/eco2mix-national-cons-def/information/?disjunctive.nature"},
                {"text": "Données en temps réel", "href": "https://odre.opendatasoft.com/explore/dataset/eco2mix-national-tr/information/?flg=fr-fr&disjunctive.nature"}
        ]
        },
        {
            "title": "Données régionales",
            "text": "Explorez les données régionales sur la production et la consommation d'électricité. Les données sont disponibles en temps réel et consolidées. Pour plus de détails, cliquez sur l'un des boutons ci-dessous.",
            "image": "/assets/donnees_regionales.jpg",
            "image_credits": "Image credits: photo by Éric Soulé de Lafont",
            "links": [
                {"text": "Données consolidées", "href": "https://odre.opendatasoft.com/explore/dataset/eco2mix-regional-cons-def/information/?disjunctive.libelle_region&disjunctive.nature "},
                {"text": "Données en temps réel", "href": "https://odre.opendatasoft.com/explore/dataset/eco2mix-regional-tr/information/?disjunctive.libelle_region&disjunctive.nature"}
        ]
        },
    ]

    cards_data = [
        dmc.Card(
            shadow="sm",
            p="lg",
            style={
                "backgroundColor": "#1A1B1E",
                "color": "white",
                "marginBottom": 30,
                "borderRadius": "8px",
            },
            children=[
                dmc.Image(
                    src=card["image"],
                    height=250,
                    fit="cover",
                    style={"borderTopLeftRadius": "8px", "borderTopRightRadius": "8px"}
                ),
                html.Div(
                    dcc.Markdown(card["image_credits"]),
                    className="image-credits",
                    style={
                        "fontSize": "0.7rem",  
                        "color": "grey",       
                        "textAlign": "center", 
                        "marginTop": "0.5rem", 
                    }
                ),
                dmc.Text(card["title"], weight=500, size="lg", style={"color": "#FFF"}),
                dmc.Text(card["text"], style={"color": "#DDD"}),
                html.Div(
                    [
                        dcc.Link(
                            dmc.Button(link["text"], color="primary", style={"marginRight": "10px"}),
                            href=link["href"],
                            target="_blank"
                        )
                        for link in card["links"]
                    ],
                    className="card-buttons"
                ),
            ],
        )
        for card in cards_data_content
    ]


    return html.Div([
        html.H6("Veuillez cliquer sur l'un des trois graphique ci-dessus pour explorer une problématique.", className="text-center mb-4"),
        dmc.Divider(size="md", style={"marginBottom": "2rem"}),
        html.H5("Les trois grands sujets de l'electricité en France", className="mb-4"),
        dmc.SimpleGrid(
            cols=3,
            spacing="lg",
            breakpoints=[
                {"maxWidth": 980, "cols": 2, "spacing": "md"},
                {"maxWidth": 755, "cols": 1, "spacing": "sm"},
            ],
            children=cards
        ),
        dmc.Divider(size="md", style={"marginBottom": "2rem"}),
        html.H5("Nos données éCO2mix", className="mb-4"),
        dmc.SimpleGrid(
            cols=2,
            spacing="lg",
            breakpoints=[
                {"maxWidth": 980, "cols": 2, "spacing": "md"},
                {"maxWidth": 755, "cols": 1, "spacing": "sm"},
            ],
            children=cards_data
        ),
        dmc.Divider(size="md", style={"marginBottom": "2rem"}),
        html.H5("À propos de ce dashboard", className="mb-4"),
        html.P("Pour revenir à cette page, cliquez sur le bouton 'Accueil' dans la barre de navigation."),
        html.P("Pour des données à jour, utilisez le bouton 'Mettre à jour les données'. Cela peut prendre plusieurs minutes, soyez patient."),
        dmc.Divider(size="md", style={"marginBottom": "2rem"}),
        dmc.Blockquote(
            "Un sourire coûte moins cher que l'électricité, mais donne autant de lumière.",
            cite="- Abbé Pierre",
            style={"marginBottom": "2rem", "color": "#DDD", "textAlign": "center"}
        ),
        html.Footer(html.P("Les données utilisées pour ce dashboard proviennent de sources officielles et sont mises à jour en continu.", className="text-center mt-4")),
    ], className="story-content")



def story_consommation():
    return html.Div([
        html.P("Cette page présente la consommation d'électricité en France."),
        ## Parler de la consommatin d'électricité en France
        ## Parler des graphiques de la page (carte, courbe de prédiction, courbe de consommation par région)
        ## Peut etre faire une "card" avec bootstrap components pour parler de la prédiction de la consommation
    ])

def story_production():
    return html.Div([
        html.P("Cette page présente la production d'électricité en France."),
        ## Parler de la production d'électricité en France
        ## Parler des graphiques de la page (carte interactive pour selectionner les regions, camembert, courbe de production par région et par type d'énergie)
        ## Peux etre faire une "card" avec bootstrap components pour parler du nucleaires, une card pour parler des energies renouvelables etc...
    ])

def story_echanges():

    return html.Div([
        html.P("Cette page présente les échanges d'électricité en France."),
        ## Parler des échanges d'électricité en France
        ## Parler des graphiques de la page (Bar chart, donut chart, boxplot)
        ## Peut etre rajouter une image de carte qui montre la France et les pays frontaliers pour illustrer les échanges (pour ceux qui sont nuls en geo lol) et ca decore le site aussi
    ])