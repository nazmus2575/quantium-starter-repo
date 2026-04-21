import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html

# ── Load & prepare data ───────────────────────────────────────────────────────
df = pd.read_csv("data/daily_sales_data.csv", parse_dates=["date"])
df = df.sort_values("date")

# Aggregate total sales per day across all regions (for the "All Regions" view)
daily = df.groupby("date", as_index=False)["sales"].sum()

PRICE_INCREASE_DATE = "2021-01-15"
PRICE_INCREASE_TS = pd.Timestamp(PRICE_INCREASE_DATE).timestamp() * 1000  # ms epoch for Plotly
regions = ["all"] + sorted(df["region"].unique().tolist())

# ── Build traces ──────────────────────────────────────────────────────────────
def build_figure(region="all"):
    if region == "all":
        data = daily.copy()
    else:
        data = df[df["region"] == region].groupby("date", as_index=False)["sales"].sum()

    before = data[data["date"] < PRICE_INCREASE_DATE]
    after  = data[data["date"] >= PRICE_INCREASE_DATE]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=before["date"], y=before["sales"],
        mode="lines",
        name="Before price increase",
        line=dict(color="#F97B4B", width=2),
        hovertemplate="<b>%{x|%d %b %Y}</b><br>Sales: $%{y:,.0f}<extra></extra>"
    ))

    fig.add_trace(go.Scatter(
        x=after["date"], y=after["sales"],
        mode="lines",
        name="After price increase",
        line=dict(color="#5BC4BF", width=2),
        hovertemplate="<b>%{x|%d %b %Y}</b><br>Sales: $%{y:,.0f}<extra></extra>"
    ))

    # Vertical line marking the price increase
    fig.add_vline(
        x=PRICE_INCREASE_TS,
        line_width=1.5,
        line_dash="dash",
        line_color="#AAAAAA",
        annotation_text="Price increase  ",
        annotation_position="top left",
        annotation_font=dict(size=12, color="#AAAAAA")
    )

    fig.update_layout(
        paper_bgcolor="#0F1117",
        plot_bgcolor="#0F1117",
        font=dict(family="'DM Sans', sans-serif", color="#E0E0E0"),
        xaxis=dict(
            title="Date",
            gridcolor="#1E2130",
            showline=False,
            tickfont=dict(size=11),
        ),
        yaxis=dict(
            title="Daily Sales (AUD)",
            gridcolor="#1E2130",
            showline=False,
            tickprefix="$",
            tickfont=dict(size=11),
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom", y=1.02,
            xanchor="left", x=0,
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=12),
        ),
        margin=dict(t=30, l=60, r=30, b=60),
        hovermode="x unified",
        transition_duration=400,
    )
    return fig


# ── Layout ────────────────────────────────────────────────────────────────────
app = Dash(__name__)
app.title = "Soul Foods · Pink Morsel Sales"

REGION_OPTIONS = [
    {"label": "All Regions", "value": "all"},
    {"label": "North",       "value": "north"},
    {"label": "South",       "value": "south"},
    {"label": "East",        "value": "east"},
    {"label": "West",        "value": "west"},
]

app.layout = html.Div(
    style={
        "backgroundColor": "#0F1117",
        "minHeight": "100vh",
        "fontFamily": "'DM Sans', sans-serif",
        "padding": "40px 48px",
    },
    children=[
        # Google Font
        html.Link(
            rel="stylesheet",
            href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;700&family=DM+Serif+Display&display=swap"
        ),

        # Header
        html.Div([
            html.P(
                "Soul Foods Analytics",
                style={"color": "#F97B4B", "fontSize": "13px", "letterSpacing": "3px",
                       "textTransform": "uppercase", "marginBottom": "6px", "fontWeight": "500"}
            ),
            html.H1(
                "Pink Morsel Sales",
                style={"fontFamily": "'DM Serif Display', serif", "fontSize": "40px",
                       "color": "#FFFFFF", "margin": "0 0 8px 0", "fontWeight": "400"}
            ),
            html.P(
                "Daily revenue before and after the January 15 2021 price increase.",
                style={"color": "#888", "fontSize": "15px", "margin": "0 0 32px 0"}
            ),
        ]),

        # Region filter
        html.Div([
            html.Label("Filter by region", style={"color": "#888", "fontSize": "12px",
                                                   "letterSpacing": "1px", "textTransform": "uppercase",
                                                   "marginBottom": "8px", "display": "block"}),
            dcc.RadioItems(
                id="region-selector",
                options=REGION_OPTIONS,
                value="all",
                inline=True,
                inputStyle={"marginRight": "6px"},
                labelStyle={
                    "marginRight": "20px",
                    "color": "#C0C0C0",
                    "fontSize": "14px",
                    "cursor": "pointer",
                },
            ),
        ], style={"marginBottom": "24px"}),

        # Chart
        dcc.Graph(
            id="sales-chart",
            figure=build_figure(),
            config={"displayModeBar": False},
            style={"height": "520px", "borderRadius": "12px",
                   "border": "1px solid #1E2130", "overflow": "hidden"}
        ),

        # Footer note
        html.P(
            "Each data point represents total Pink Morsel sales for that day. "
            "Dashed line marks the price increase on 15 Jan 2021.",
            style={"color": "#555", "fontSize": "12px", "marginTop": "16px"}
        ),
    ]
)


# ── Callback ──────────────────────────────────────────────────────────────────
from dash import Input, Output

@app.callback(
    Output("sales-chart", "figure"),
    Input("region-selector", "value")
)
def update_chart(region):
    return build_figure(region)


if __name__ == "__main__":
    app.run(debug=True)

