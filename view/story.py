from dash import html
# AJOUTER D'AUTRES IMPORTS SI BESOIN

## On appellera ces fonctions dans les pages pour afficher le texte
## Ne pas hesiter a utiliser des balises html pour mettre en forme le texte et du bootstrap components pour le style ou autre 
## (faires des petites cases de texte pour chaque problematique etc...) (bootstrap components: https://dash-bootstrap-components.opensource.faculty.ai/docs/components/card/)
## Ne pas hesiter a faire plus de fonctions si besoin
## Pourquoi pas ajouter quelques images pour illustrer les propos, pour rendre le site plus vivant

def story_accueil():
    return html.Div([
        html.P("Ce dashboard a été réalisé dans le cadre du projet de M1 CMI ISI de Louis Delignac, Théo Lavandier et Hamad Tria."),
        html.P("Il a pour but de présenter et de visualiser les données de production, d'échange et de consommation d'électricité en France."),
        html.P("Pour revenir à cette page, cliquez sur le bouton 'Accueil' dans la barre de navigation.")
        ## Ajouter des informations sur les données utilisées (sources, dates, liens etc...)
        ## Ajouter des informations sur les graphiques de la page d'accueil
    ])

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
        ## Peut etre rajouter une image de carte qui montre la France et les pays frontaliers pour illustrer les échanges (pour ceux aui sont nuls en geo lol) et ca decore le site aussi
    ])