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
        html.H5("Source de nos données éCO2mix", className="mb-4"),
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
    cards_content = [
        {
            "title": "La Production Nucléaire",
            "text": (
                "Le nucléaire joue un rôle clé dans le mix énergétique français, "
                "représentant environ 65% de la production totale d'électricité. "
                "Cette dominance s'explique par la volonté historique de la France de garantir son indépendance énergétique et de limiter ses émissions de CO2."
            ),
            "image": "/assets/nucleaire.jpg",
            "image_credits": "Image credits: Getty Images, yangna",
        },
        {
            "title": "Les Énergies Renouvelables",
            "text": (
                "Les énergies renouvelables gagnent du terrain avec des projets d'éolien, de solaire, et d'hydroélectricité. "
                "Ces sources d'énergie sont essentielles pour la transition écologique et permettent à la France de se rapprocher de ses objectifs climatiques."
            ),
            "image": "/assets/renouvelable.jpg",  
            "image_credits": "Image credits: iStock, Petmal ",
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
                    height=180,
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

    cards_graphs_content = [
        {
            "title": "Pie Chart de la Production d'Électricité en Métropole et par Region",
            "text": (
                "Le Pie Chart illustre la répartition de la production d'électricité par filière en Métropole et par région. "
                "Le graphique est interactif, vous pouvez cliquer sur les différents secteurs pour les mettre en évidence et les comparer. "
                "Il est possible de cliquer sur une region de la carte interactive pour afficher la répartition de la production pour cette région. "
                "Par exemple, il permet de mettre en évidence que la région Grand-Est produit beaucoup d'électricité nucléaire, "
                "alors que la région Occitanie produit beaucoup d'électricité solaire."
            ),
        },
        {
            "title": "Stacked Area chart de la Production d'Électricité par région et par filière",
            "text": (
                "Le Stacked Area Chart illustre la production d'électricité par région et par filière. "
                "Le graphique est interactif, vous pouvez selectionner une filière dans le dropdown pour afficher la production par région pour cette filière. "
                "Il est possible de selectionner une ou plusieurs régions sur le graphique pour afficher les mettres en évidence et les comparer. "
                "Ce graphique permet de visualiser la production d'électricité par région et par filière en details pour une période donnée. "
            ),
        },
        {
            "title": "Troisieme graphique de la production d'électricité",
            "text": (
                "Description du troisieme graphique de la production d'électricité"
            ),
        }
    ]

    cards_graphs = [
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
                dmc.Text(card["title"], weight=500, size="lg", style={"color": "#FFF"}),
                dmc.Text(card["text"], style={"color": "#DDD"}),
            ],
        )
        for card in cards_graphs_content
    ]

    return dmc.Container([
        dmc.Divider(size="md", style={"marginBottom": "2rem"}),
        dmc.Text(
            "La France dispose d'un mix énergétique diversifié et est un leader mondial de la production d'électricité nucléaire. "
            "Les énergies renouvelables représentent une part croissante du mix, reflétant l'engagement du pays envers le développement durable."
        ),
        dmc.SimpleGrid(
            cols=2,
            spacing="lg",
            children=cards
        ),
        dmc.SimpleGrid(
            cols=3,
            spacing="lg",
            children=cards_graphs
        ),
    ], fluid=True, style={"maxWidth": 1200})


def story_echanges():
    return dmc.Container([
        dmc.Divider(size="md", style={"marginBottom": "2rem"}),
        dmc.Text(
            "La France est au cœur du réseau électrique européen grâce à ses échanges "
            "transfrontaliers. Cela lui permet d'exporter et d'importer de l'électricité, "
            "optimisant ainsi l'utilisation de ses ressources et répondant mieux à la demande énergétique."
        ),
        dbc.Row([
            dmc.Card(
                children=[
                    dmc.Text("Les Pays frontaliers", weight=500, size="lg", style={"color": "#FFF"}),
                    dmc.Text(
                        "La France partage des frontières avec six pays voisins, chacun ayant un profil de production "
                        "d'électricité unique. Les échanges d'électricité avec ces pays sont essentiels pour maintenir "
                        "l'équilibre entre l'offre et la demande."
                        "Voici la liste des pays interconnectés avec la France",
                        style={"color": "#DDD"}
                    ),
                    dmc.List(
                        [
                            dmc.ListItem("Allemagne"),
                            dmc.ListItem("Belgique"),
                            dmc.ListItem("Espagne"),
                            dmc.ListItem("Italie"),
                            dmc.ListItem("Angleterre"),
                            dmc.ListItem("Suisse"),
                        ],
                        style={
                            "marginBottom": "20px",
                            "color": "#DDD"  
                        }
                    ),
                    dmc.Text(
                        "Dans nos données, les échanges d'électricité sont exprimés en MW, "
                        "ce qui correspond à la puissance électrique instantanée. "
                        "Un MW est équivalent à un million de watts, soit la puissance d'environ 1000 voitures.",
                        style={"color": "#DDD"}
                    ),
                
                ],
                shadow="sm",
                p="lg",
                style={
                    "backgroundColor": "#1A1B1E",
                    "color": "white",
                    "marginBottom": 30,
                    "borderRadius": "8px",
                },
            ),
        ]),
        dbc.Row([
            dmc.SimpleGrid(
            cols=3,
            spacing="lg",
            breakpoints=[
                {"maxWidth": 980, "cols": 2, "spacing": "md"},
                {"maxWidth": 755, "cols": 1, "spacing": "sm"},
            ],
            children=[
                dmc.Card(
                children=[
                    dmc.Text("Donut Chart", weight=500, size="lg", style={"color": "#FFF"}),
                    dmc.Text(
                        "Le Donut Chart illustre la proportion des échanges avec chaque pays voisin, "
                        "offrant une perspective claire sur le partage des flux d'électricité. "
                        "Le graphique est interactif, vous pouvez cliquer sur les différents pays pour "
                        "les mettre en évidence et les comparer. "
                        "Par exemple, il permet de mettre en évidence que l'Allemagne/Belgique est le "
                        "plus gros importateur d'électricité de la France. "
                        "Egalement, il permet de mettre en évidence que l'Italie importe très peu d'électricité en France."
                    ),
                ],
                shadow="sm",
                p="lg",
                style={
                    "backgroundColor": "#1A1B1E",
                    "color": "white",
                    "marginBottom": 30,
                    "borderRadius": "8px",
                },
            ),
            dmc.Card(
                children=[
                    dmc.Text("Boxplot", weight=500, size="lg", style={"color": "#FFF"}),
                    dmc.Text(
                        "Le Boxplot présente la variabilité et la distribution des échanges sur une "
                        "période étendue, révélant les tendances et les points aberrants dans les données pour chaque pays. "
                        "Le graphique est interactif, vous pouvez cliquer sur les différents pays pour les mettre en évidence et les comparer. "
                        "Par exemple, il permet de mettre en évidence que les échanges avec l'Allemagne/Belgique sont très variables, "
                        "alors que les échanges avec l'Italie sont plus constants. (Les échanges avec l'Italie sont également plus faibles en termes de d'imports.)"

                    ),
                ],
                shadow="sm",
                p="lg",
                style={
                    "backgroundColor": "#1A1B1E",
                    "color": "white",
                    "marginBottom": 30,
                    "borderRadius": "8px",
                },
            ),
            dmc.Card(
                children=[
                    dmc.Text("Bar Chart", weight=500, size="lg", style={"color": "#FFF"}),
                    dmc.Text(
                        "Le Bar Chart illustre la quantité d'électricité échangée avec chaque pays voisin sur une période donnée. "
                        "Le graphique est interactif, vous pouvez cliquer sur les différents "
                        "pays pour les mettre en évidence et les comparer."
                        "Vous pouvez également utiliser le curseur pour afficher les échanges pour une heure donnée."
                        "Ce graphique est utile pour identifier les périodes de forte demande et les périodes de faible demande."
                        "Il est également précis car il affiche les échanges pour chaque heure de la journée."
                    ),
                ],
                shadow="sm",
                p="lg",
                style={
                    "backgroundColor": "#1A1B1E",
                    "color": "white",
                    "marginBottom": 30,
                    "borderRadius": "8px",
                },
            ),
            ]
        ),
        ]),
        dmc.Card(
            children=[
                dmc.Text("Carte de la France et ses pays frontaliers", weight=500, size="lg", style={"color": "#FFF"}),
                dmc.Text(
                    "Pour ceux moins familiers avec la géographie européenne, une carte de la France et de ses pays voisins est disponible. "
                ),
                dmc.Image(
                    src="/assets/europe.png",
                    height=740,
                    fit="cover",
                    style={"borderTopLeftRadius": "8px", "borderTopRightRadius": "8px"}
                ),
                html.Div(
                    dcc.Markdown('Image credits: Google Maps'),
                    className="image-credits",
                    style={
                        "fontSize": "0.7rem",  
                        "color": "grey",       
                        "textAlign": "center", 
                        "marginTop": "0.5rem", 
                    }
                ),
                
            ],
            shadow="sm",
            p="lg",
            style={
                "backgroundColor": "#1A1B1E",
                "color": "white",
                "marginBottom": 30,
                "borderRadius": "8px",
            },
        ),
    ], fluid=True, style={"maxWidth": 1200})

