# EXAMEN PYTHON --LY Néné Gallé -- Enseignant: Abdou Razak Sané
# Dash-Bord interactif d'un supermarché 

# Importation des bibliothèques
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc


# Chargement des données
df = pd.read_csv("supermarket_sales.csv")

# Conversion de la date
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Suppression des dates manquantes
df = df.dropna(subset=["Date"]).copy()

# Création de la variable semaine
df["Week"] = df["Date"].dt.to_period("W").apply(lambda x: x.start_time)

# Modalités pour les filtres
genders = sorted(df["Gender"].dropna().unique())
cities = sorted(df["City"].dropna().unique())

# =========================
# Couleurs générales
# =========================
BLANC = "#FFFFFF"
BORDURE = "rgba(255,255,255,0.75)"
FOND_DROPDOWN = "rgba(255,255,255,0.25)"

# Couleurs du graphique d'évolution (comme avant)
CITY_COLORS_LINE = {
    "Yangon": "#2E6BD1",
    "Mandalay": "#F28C28",
    "Naypyitaw": "#2FBF71"
}

# Couleurs du diagramme en barres
GENDER_COLORS_BAR = {
    "Male": "#2E6BD1",     # bleu
    "Female": "#F48FB1"    # rose
}

# Couleurs du diagramme circulaire
# Reprise de l'ancien style, en évitant les couleurs déjà utilisées
PIE_COLORS = [
    "#F4C542",  # jaune doré
    "#7A57C2",  # violet
    "#EF5350",  # rouge doux
    "#66BB6A",  # vert clair
    "#8D6E63",  # brun doux
    "#26A69A",  # turquoise
    "#D81B60"   # rose foncé
]


# Application Dash

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server


# Styles

style_page = {
    "minHeight": "100vh",
    "backgroundImage": "url('/assets/background.jpg')",
    "backgroundSize": "cover",
    "backgroundPosition": "center",
    "padding": "10px 20px"
}

style_box = {
    "backgroundColor": "transparent",
    "border": f"12px solid {BORDURE}",
    "borderRadius": "25px",
    "padding": "15px",
    "marginBottom": "20px"
}
#  Style spécifique pour les KPI, avec un peu plus de padding et une bordure plus épaisse pour les faire ressortir davantage
style_kpi = {
    "backgroundColor": "transparent",
    "border": f"12px solid {BORDURE}",
    "borderRadius": "25px",
    "padding": "20px"
}

style_oval_title = {
    "display": "inline-block",
    "padding": "10px 28px",
    "border": f"8px solid {BORDURE}",
    "borderRadius": "20px",
    "color": BLANC,
    "fontWeight": "bold",
    "fontSize": "22px",
    "marginBottom": "14px",
    "backgroundColor": "rgba(255,255,255,0.10)"
}

style_oval_filter = {
    "display": "inline-block",
    "padding": "8px 22px",
    "border": f"8px solid {BORDURE}",
    "borderRadius": "20px",
    "color": BLANC,
    "fontWeight": "bold",
    "fontSize": "20px",
    "marginBottom": "10px",
    "backgroundColor": FOND_DROPDOWN
}

dropdown_style = {
    "color": "#1f1f1f",
    "backgroundColor": FOND_DROPDOWN,
    "border": f"8px solid {BORDURE}",
    "borderRadius": "20px"
}

style_gender_note = {
    "color": BLANC,
    "fontSize": "18px",
    "fontWeight": "600",
    "textAlign": "center",
    "marginTop": "-5px",
    "marginBottom": "10px"
}


# Mise en page

app.layout = html.Div(
    style=style_page,
    children=[

        html.Div(
            html.Img(
                src="/assets/logo.png",
                style={
                    "height": "400px",
                    "display": "block",
                    "margin": "0 auto",
                    "marginBottom": "30px"
                }
            )
        ),

        dbc.Row(
            className="mb-4",
            children=[
                dbc.Col(
                    [
                        html.Div("Sexe", style=style_oval_filter),
                        dcc.Dropdown(
                            id="gender_filter",
                            options=[{"label": "Tous", "value": "All"}] +
                                    [{"label": x, "value": x} for x in genders],
                            value="All",
                            clearable=False,
                            style=dropdown_style
                        )
                    ],
                    md=6
                ),
                dbc.Col(
                    [
                        html.Div("Ville", style=style_oval_filter),
                        dcc.Dropdown(
                            id="city_filter",
                            options=[{"label": "Toutes", "value": "All"}] +
                                    [{"label": x, "value": x} for x in cities],
                            value="All",
                            clearable=False,
                            style=dropdown_style
                        )
                    ],
                    md=6
                )
            ]
        ),

        dbc.Row(
            className="mb-4",
            children=[
                dbc.Col(
                    html.Div(
                        [
                            html.Div("Montant Total des Achats", style=style_oval_title),
                            html.H2(
                                id="kpi_total",
                                style={
                                    "color": BLANC,
                                    "fontSize": "40px",
                                    "fontWeight": "bold"
                                }
                            )
                        ],
                        style=style_kpi
                    ),
                    md=6
                ),
                dbc.Col(
                    html.Div(
                        [
                            html.Div("Nombre Total d'Achats", style=style_oval_title),
                            html.H2(
                                id="kpi_count",
                                style={
                                    "color": BLANC,
                                    "fontSize": "40px",
                                    "fontWeight": "bold"
                                }
                            )
                        ],
                        style=style_kpi
                    ),
                    md=6
                )
            ]
        ),

        html.Div(
            [
                html.Div("Évolution des ventes", style=style_oval_title),
                dcc.Graph(id="line_chart")
            ],
            style=style_box
        ),

        dbc.Row(
            children=[
                dbc.Col(
                    html.Div(
                        [
                            html.Div("Achats par sexe et ville", style=style_oval_title),
                            dcc.Graph(id="bar_chart")
                        ],
                        style=style_box
                    ),
                    md=6
                ),
                dbc.Col(
                    html.Div(
                        [
                            html.Div("Catégories de produits", style=style_oval_title),
                            dcc.Graph(id="pie_chart"),
                            html.Div(id="pie_gender_note", style=style_gender_note)
                        ],
                        style=style_box
                    ),
                    md=6
                )
            ]
        )
    ]
)

# Callback

@app.callback(
    Output("kpi_total", "children"),
    Output("kpi_count", "children"),
    Output("line_chart", "figure"),
    Output("bar_chart", "figure"),
    Output("pie_chart", "figure"),
    Output("pie_gender_note", "children"),
    Input("gender_filter", "value"),
    Input("city_filter", "value")
)
def update_dashboard(gender, city):
    dff = df.copy()

    # Filtre sexe
    if gender != "All":
        dff = dff[dff["Gender"] == gender]

    # Filtre ville
    if city != "All":
        dff = dff[dff["City"] == city]

    # KPI
    total = dff["Total"].sum()
    count = dff["Invoice ID"].nunique()

    # Texte sous le diagramme circulaire
    if gender == "All":
        pie_gender_note = "Tous sexes confondus"
    else:
        pie_gender_note = gender

 
    # 1. Courbe d'évolution hebdomadaire
   
    if city == "All":
        line_data = dff.groupby(["Week", "City"], as_index=False)["Total"].sum()

        fig_line = px.line(
            line_data,
            x="Week",
            y="Total",
            color="City",
            markers=True,
            color_discrete_map=CITY_COLORS_LINE
        )
    else:
        line_data = dff.groupby("Week", as_index=False)["Total"].sum()

        selected_line_color = CITY_COLORS_LINE.get(city, "#2E6BD1")

        fig_line = px.line(
            line_data,
            x="Week",
            y="Total",
            markers=True
        )
        fig_line.update_traces(line=dict(color=selected_line_color))

    fig_line.update_traces(line=dict(width=4))

    fig_line.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white", size=14),
        legend=dict(font=dict(color="white")),
        xaxis_title="Semaine",
        yaxis_title="Montant total des achats"
    )

    fig_line.update_xaxes(showgrid=False, color="white")
    fig_line.update_yaxes(
        showgrid=True,
        gridcolor="rgba(255,255,255,0.25)",
        color="white"
    )

    
    # 2. Diagramme en barres
  
    bar_data = dff.groupby(["City", "Gender"], as_index=False)["Invoice ID"].nunique()

    fig_bar = px.bar(
        bar_data,
        x="City",
        y="Invoice ID",
        color="Gender",
        barmode="group",
        color_discrete_map=GENDER_COLORS_BAR,
        text="Invoice ID"
    )

    fig_bar.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white", size=14),
        legend=dict(font=dict(color="white")),
        xaxis_title="Ville",
        yaxis_title="Nombre total d'achats"
    )

    fig_bar.update_xaxes(showgrid=False, color="white")
    fig_bar.update_yaxes(
        showgrid=True,
        gridcolor="rgba(255,255,255,0.25)",
        color="white"
    )

    
    # 3. Diagramme circulaire
  
    pie_data = dff.groupby("Product line", as_index=False)["Invoice ID"].nunique()

    fig_pie = px.pie(
        pie_data,
        names="Product line",
        values="Invoice ID",
        color_discrete_sequence=PIE_COLORS
    )

    fig_pie.update_traces(
        textinfo="percent+label",
        textfont=dict(color="white", size=12)
    )

    fig_pie.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white", size=14),
        legend=dict(font=dict(color="white"))
    )

    return (
        f"{total:,.2f} $",
        f"{count}",
        fig_line,
        fig_bar,
        fig_pie,
        pie_gender_note
    )

