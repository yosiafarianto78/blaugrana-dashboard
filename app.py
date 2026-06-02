import streamlit as st
import plotly.graph_objects as go 
import plotly.express as px
import pandas as pd
import numpy as np
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="FC Barcelona Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&family=Space+Mono:wght@400;700&display=swap');

/* Root variables */
:root {
    --barca-red:   #A50044;
    --barca-blue:  #004D98;
    --barca-gold:  #EDBB00;
    --madrid-white:#F5F5F0;
    --madrid-gold: #C8A84B;
    --madrid-navy: #00205B;
    --bg-deep:     #080C14;
    --bg-card:     #0D1421;
    --bg-surface:  #121A2B;
    --text-primary:#E8ECF4;
    --text-muted:  #6B7A9A;
    --accent-cyan: #00D4FF;
    --border:      rgba(255,255,255,0.07);
}

/* Full dark background */
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: var(--bg-deep) !important;
    font-family: 'DM Sans', sans-serif;
    color: var(--text-primary);
}
[data-testid="stHeader"] { background: transparent !important; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: var(--bg-card) !important;
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] * { color: var(--text-primary) !important; }

/* Nav radio buttons */
div[role="radiogroup"] label {
    display: block;
    padding: 10px 14px;
    border-radius: 8px;
    margin-bottom: 4px;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.85rem;
    letter-spacing: 0.02em;
    cursor: pointer;
    transition: background 0.2s;
    color: var(--text-muted) !important;
}
div[role="radiogroup"] label:hover { background: rgba(255,255,255,0.05); }
div[role="radiogroup"] [data-baseweb="radio"] input:checked ~ div {
    background: var(--barca-blue) !important;
}

/* Metric cards */
.metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px 24px;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--barca-red), var(--barca-blue));
}
.metric-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.12em;
    color: var(--text-muted);
    text-transform: uppercase;
    margin-bottom: 6px;
}
.metric-value {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.4rem;
    line-height: 1;
    color: var(--text-primary);
}
.metric-sub {
    font-size: 0.75rem;
    color: var(--text-muted);
    margin-top: 4px;
}

/* Section headers */
.section-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.8rem;
    letter-spacing: 0.06em;
    color: var(--text-primary);
    margin-bottom: 2px;
}
.section-sub {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    color: var(--text-muted);
    text-transform: uppercase;
    margin-bottom: 24px;
}

/* Business insight box */
.insight-box {
    background: linear-gradient(135deg, rgba(0,77,152,0.15), rgba(165,0,68,0.10));
    border: 1px solid rgba(0,212,255,0.2);
    border-left: 3px solid var(--accent-cyan);
    border-radius: 10px;
    padding: 16px 20px;
    margin-top: 20px;
}
.insight-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.12em;
    color: var(--accent-cyan);
    text-transform: uppercase;
    margin-bottom: 6px;
}
.insight-text {
    font-size: 0.82rem;
    line-height: 1.6;
    color: var(--text-muted);
}

/* Divider */
.dash-divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 28px 0;
}

/* Quadrant labels */
.quad-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* Page title header */
.page-header {
    background: linear-gradient(135deg, var(--bg-card), var(--bg-surface));
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.page-header::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, var(--barca-red), var(--barca-blue), var(--barca-gold));
}
.page-nav-tag {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.2em;
    color: var(--accent-cyan);
    text-transform: uppercase;
    margin-bottom: 6px;
}
.page-main-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.6rem;
    letter-spacing: 0.06em;
    line-height: 1;
    margin-bottom: 6px;
}
.page-desc {
    font-size: 0.82rem;
    color: var(--text-muted);
    max-width: 560px;
    line-height: 1.6;
}
            

.metric-card {
    transition: all 0.25s ease;
}

.metric-card:hover {
    transform: translateY(-4px);
    border-color: rgba(0,212,255,0.25);
    box-shadow: 0 10px 25px rgba(0,0,0,0.3);
}

.page-header {
    transition: all 0.25s ease;
}

.page-header:hover {
    border-color: rgba(0,212,255,0.2);
}
            
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div style="padding: 6px 0 20px;">
        <div style="font-family:'Bebas Neue',sans-serif;font-size:1.5rem;letter-spacing:0.08em;color:#E8ECF4;">
            ⚽ La Liga Analytics
        </div>
        <div style="margin-left:42px;font-family:'Space Mono',monospace;font-size:0.6rem;letter-spacing:0.15em;color:#6B7A9A;text-transform:uppercase;">
            FC Barcelona · 2025
        </div>
    </div>
    <hr style="border:none;border-top:1px solid rgba(255,255,255,0.07);margin-bottom:20px;">
    """, unsafe_allow_html=True)

    with st.sidebar:
        nav = option_menu(
            menu_title=None,
            options=[
                "Frontline Showdown",
                "Goal Conversion",
                "Performance Trend",
                "Talent Mapping"
            ],
            icons=[
                "trophy",
                "bullseye",
                "graph-up",
                "people"
            ],
            default_index=0,
            styles={
                "container": {
                    "background-color": "#0D1421",
                    "padding": "0!important"
                },
                "nav-link": {
                    "font-size": "14px",
                    "text-align": "left",
                    "margin": "3px",
                    "border-radius": "10px",
                },
                "nav-link-selected": {
                    "background-color": "#004D98",
                },
            }
        )

    st.markdown("""
    <hr style="border:none;border-top:1px solid rgba(255,255,255,0.07);margin:24px 0 16px;">
    <div style="font-family:'Space Mono',monospace;font-size:0.58rem;letter-spacing:0.1em;color:#3D4F70;text-transform:uppercase;line-height:1.8;">
        Data Source · FBref · 2024–2025
    </div>
    """, unsafe_allow_html=True)

# NAV 01 · FRONTLINE SHOWDOWN
if nav == "Frontline Showdown":
    st.markdown("""
    <div class="page-header">
        <div class="page-main-title">Frontline Showdown Barca vs Madrid</div>
        <div class="page-desc">
            Comparative productivity analysis of the attacking units from Barcelona and Real Madrid based on goals and assists contribution.
        </div>
    </div>
    """, unsafe_allow_html=True)

    df = pd.read_csv("data/frontline_showdown.csv")
    df["G+A"] = df["Goals"] + df["Assists"]
    
    # Colours
    COLOR_MAP = {
        "Barcelona": {"goals": "#004D98", "assists": "#A50044"},
        "Real Madrid":    {"goals": "#C8A84B", "assists": "#00205B"},
    }

    # KPI row 
    barca_df = df[df.Club == "Barcelona"]
    madrid_df = df[df.Club == "Real Madrid"]

    top_scorer = df.loc[df["Goals"].idxmax()]
    best_playmaker = df.loc[df["Assists"].idxmax()]
    c1, c2, c3, c4 = st.columns(4)
    kpis = [
                (
                    "Barça Total G+A",
                    int(barca_df["G+A"].sum()),
                    "Combined front-3 output"
                ),
                (
                    "Madrid Total G+A",
                    int(madrid_df["G+A"].sum()),
                    "Combined front-3 output"
                ),
                (
                    "Top Scorer",
                    f"{top_scorer['Player']} · {top_scorer['Goals']}G",
                    "Most goals – all players"
                ),
                (
                    "Best Playmaker",
                    f"{best_playmaker['Player']} · {best_playmaker['Assists']}A",
                    "Most assists – all players"
                ),
            ]
    for col, (label, val, sub) in zip([c1, c2, c3, c4], kpis):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{val}</div>
                <div class="metric-sub">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    # ── Chart 
    fig = go.Figure()

    for club, grp in df.groupby("Club"):
        gc = COLOR_MAP[club]["goals"]
        ac = COLOR_MAP[club]["assists"]
        fig.add_trace(go.Bar(
            y=grp["Player"], x=grp["Goals"],
            name=f"{club} – Goals",
            orientation="h",
            marker=dict(color=gc, line=dict(width=0)),
            text=grp["Goals"], textposition="inside",
            textfont=dict(family="Space Mono", size=11, color="white"),
        ))
        fig.add_trace(go.Bar(
            y=grp["Player"], x=grp["Assists"],
            name=f"{club} – Assists",
            orientation="h",
            marker=dict(color=ac, line=dict(width=0)),
            text=grp["Assists"], textposition="inside",
            textfont=dict(family="Space Mono", size=11, color="white"),
        ))

    fig.update_layout(
        barmode="stack",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color="#E8ECF4"),
        height=400,
        margin=dict(l=10, r=30, t=20, b=20),
        legend=dict(
            orientation="h", x=0, y=-0.12,
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=11),
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.05)",
            tickfont=dict(family="Space Mono", size=10),
            title="Goals + Assists",
            titlefont=dict(size=11),
        ),
        yaxis=dict(
            tickfont=dict(family="DM Sans", size=13),
            categoryorder="total ascending",
        ),
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})



# NAV 02 · GOAL CONVERSION RATE
elif nav == "Goal Conversion":
    st.markdown("""
    <div class="page-header">
        <div class="page-main-title">Goal Conversion Rate</div>
        <div class="page-desc">
            How efficiently did Barcelona turn shots into goals in 2025? Mapped to Marketing Conversion Rate — from impressions to purchases.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Data
    df = pd.read_csv("data/conversion_stats.csv")

    barca = df[df["Team"] == "Barcelona"].iloc[0]

    conversion = round(
        barca["GoalsScored"] / barca["TotalShots"] * 100,
        1
    )

    sot_rate = round(
        barca["ShotsOnTarget"] / barca["TotalShots"] * 100,
        1
    )

    xg_overperf = round(
        barca["GoalsScored"] - barca["xG"],
        1
    )
    # KPI row
    c1, c2, c3, c4 = st.columns(4)
    for col, (k, v, s) in zip([c1, c2, c3, c4], [
        ("Total Shots",      f"{barca['TotalShots']}",   "Attempts"),
        ("Shots on Target",  f"{barca['ShotsOnTarget']}","Accuracy rate"),
        ("Goals Scored",     f"{barca['GoalsScored']}",  "Actual conversions"),
        ("xG Over-perf.",    f"+{xg_overperf}",             "Goals above expected"),
    ]):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{k}</div>
                <div class="metric-value">{v}</div>
                <div class="metric-sub">{s}</div>
            </div>
            """, unsafe_allow_html=True)


    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    # Gauge + Activity Rings side by side 
    col_left, col_right = st.columns([1, 1])

    # Speedometer Gauge
    with col_left:
        st.markdown('<div class="section-title">Shot-to-Goal Rate</div><div class="section-sub">Conversion Efficiency</div>', unsafe_allow_html=True)
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=conversion,
            delta={"reference": 14.0, "suffix": "%", "font": {"size": 14}},
            number={"suffix": "%", "font": {"family": "Bebas Neue", "size": 52, "color": "#E8ECF4"}},
            gauge={
                "axis": {"range": [0, 30], "tickwidth": 1, "tickcolor": "#6B7A9A",
                         "tickfont": {"family": "Space Mono", "size": 9}},
                "bar": {"color": "#004D98", "thickness": 0.28},
                "bgcolor": "rgba(0,0,0,0)",
                "borderwidth": 0,
                "steps": [
                    {"range": [0,  10], "color": "rgba(165,0,68,0.15)"},
                    {"range": [10, 18], "color": "rgba(0,77,152,0.15)"},
                    {"range": [18, 30], "color": "rgba(237,187,0,0.15)"},
                ],
                "threshold": {
                    "line": {"color": "#EDBB00", "width": 3},
                    "thickness": 0.8,
                    "value": 14,
                },
            },
            title={"text": "Conversion %<br><span style='font-size:11px;color:#6B7A9A'>La Liga avg ≈ 14%</span>",
                   "font": {"family": "Space Mono", "size": 12, "color": "#6B7A9A"}},
        ))
        fig_gauge.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="DM Sans", color="#E8ECF4"),
            height=320,
            margin=dict(l=20, r=20, t=40, b=20),
        )
        st.plotly_chart(fig_gauge, use_container_width=True, config={"displayModeBar": False})

    # Activity Rings
    with col_right:
        st.markdown('<div class="section-title">Funnel Rings</div><div class="section-sub">Shot Funnel Analysis</div>', unsafe_allow_html=True)

        rings = [
            {"label": "Goal / Shot",   "val": conversion,  "max": 30,  "color": "#004D98", "r": 110},
            {"label": "SoT / Shot",    "val": sot_rate,    "max": 100, "color": "#A50044", "r":  75},
            {"label": "Goal / SoT",    "val": round(barca["GoalsScored"]/barca["ShotsOnTarget"]*100,1),
                                                            "max": 100, "color": "#EDBB00", "r":  40},
        ]

        fig_rings = go.Figure()
        for ring in rings:
            pct = ring["val"] / ring["max"]
            theta = np.linspace(0, 2 * np.pi * pct, 200)
            x = [ring["r"] * np.cos(t - np.pi/2) for t in theta]
            y = [ring["r"] * np.sin(t - np.pi/2) for t in theta]
            # Background ring
            t_full = np.linspace(0, 2 * np.pi, 200)
            xb = [ring["r"] * np.cos(t - np.pi/2) for t in t_full]
            yb = [ring["r"] * np.sin(t - np.pi/2) for t in t_full]
            fig_rings.add_trace(go.Scatter(
                x=xb, y=yb, mode="lines",
                line=dict(color=f"rgba{tuple(int(ring['color'].lstrip('#')[i:i+2],16) for i in (0,2,4)) + (0.12,)}", width=18),
                showlegend=False, hoverinfo="skip",
            ))
            fig_rings.add_trace(go.Scatter(
                x=x, y=y, mode="lines",
                line=dict(color=ring["color"], width=18),
                name=f"{ring['label']}: {ring['val']}%",
                hovertemplate=f"<b>{ring['label']}</b><br>{ring['val']}%<extra></extra>",
            ))
            # Label
            fig_rings.add_annotation(
                x=0, y=ring["r"],
                text=f"<b style='font-size:10px'>{ring['val']}%</b>",
                showarrow=False, font=dict(color=ring["color"], size=9, family="Space Mono"),
                xanchor="left", xshift=ring["r"]+8,
            )

        fig_rings.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=320,
            margin=dict(l=20, r=40, t=20, b=20),
            xaxis=dict(visible=False, range=[-145, 200]),
            yaxis=dict(visible=False, range=[-145, 145], scaleanchor="x"),
            legend=dict(orientation="v", x=0.65, y=0.5,
                        font=dict(family="Space Mono", size=9), bgcolor="rgba(0,0,0,0)"),
            showlegend=True,
        )
        st.plotly_chart(fig_rings, use_container_width=True, config={"displayModeBar": False})



# NAV 03 · PERFORMANCE TREND
elif nav == "Performance Trend":
    st.markdown("""
    <div class="page-header">
        <div class="page-main-title">Performance Trend 2025</div>
        <div class="page-desc">
            Monthly cumulative points + rolling win rate for Barcelona across 2024–2025.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Data 
    
    df_monthly = pd.read_csv("data/monthly_performance.csv")

    months = df_monthly["Month"].tolist()

    wins_pm = df_monthly["Wins"].tolist()
    draws_pm = df_monthly["Draws"].tolist()
    losses_pm = df_monthly["Losses"].tolist()

    goals_pm = df_monthly["Goals"].tolist()
    xg_pm = df_monthly["xG"].tolist()

    # Hitung points otomatis
    points_pm = (
        df_monthly["Wins"] * 3 +
        df_monthly["Draws"]
    ).tolist()
   
    cum_pts = np.cumsum(points_pm).tolist()

    win_rate = [
        round(w/(w+d+l)*100)
        for w,d,l in zip(
            wins_pm,
            draws_pm,
            losses_pm
        )
    ]
    # KPI
    c1, c2, c3, c4 = st.columns(4)
    peak_idx = np.argmax(points_pm)

    peak_month = months[peak_idx]
    peak_points = points_pm[peak_idx]
    for col, (k, v, s) in zip([c1,c2,c3,c4], [
        (
            "Total Points",
            sum(points_pm),
            "Full season 2024–25"),
        (
            "Avg Points/Mo",  
            f"{round(np.mean(points_pm),1)}", 
            "Consistency index"),
        (
            "Peak Month",
            f"{peak_month} · {peak_points} pts",
            "Best performing month"
        ),
        (   "Avg Win Rate",
            f"{round(np.mean(win_rate))}%",
            "Across all months"),
    ]):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{k}</div>
                <div class="metric-value">{v}</div>
                <div class="metric-sub">{s}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    # Smooth gradient area chart
    fig_trend = go.Figure()

    # Gradient fill area
    fig_trend.add_trace(go.Scatter(
        x=months, y=cum_pts,
        fill="tozeroy",
        fillcolor="rgba(0,77,152,0.18)",
        line=dict(color="#004D98", width=3, shape="spline", smoothing=1.3),
        name="Cumulative Points",
        mode="lines",
        hovertemplate="<b>%{x}</b><br>Cumulative pts: <b>%{y}</b><extra></extra>",
    ))

    # Monthly points bars (secondary)
    fig_trend.add_trace(go.Bar(
        x=months, y=points_pm,
        name="Monthly Points",
        marker=dict(
            color=points_pm,
            colorscale=[[0,"rgba(165,0,68,0.5)"],[0.5,"rgba(0,77,152,0.6)"],[1,"rgba(237,187,0,0.7)"]],
            line=dict(width=0),
        ),
        opacity=0.55,
        yaxis="y2",
        hovertemplate="<b>%{x}</b><br>Month pts: <b>%{y}</b><extra></extra>",
    ))

    # Win rate line
    fig_trend.add_trace(go.Scatter(
        x=months, y=win_rate,
        line=dict(color="#EDBB00", width=2, dash="dot", shape="spline", smoothing=1.3),
        name="Win Rate %",
        yaxis="y3",
        hovertemplate="<b>%{x}</b><br>Win rate: <b>%{y}%</b><extra></extra>",
    ))

    fig_trend.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=420,
        margin=dict(l=10, r=60, t=20, b=20),
        font=dict(family="DM Sans", color="#E8ECF4"),
        xaxis=dict(
            showgrid=False,
            tickfont=dict(family="Space Mono", size=10),
        ),
        yaxis=dict(
            title="Cumulative Points",
            showgrid=True, gridcolor="rgba(255,255,255,0.04)",
            tickfont=dict(family="Space Mono", size=9),
        ),
        yaxis2=dict(
            overlaying="y", side="right", range=[0, 20],
            showgrid=False, showticklabels=False,
        ),
        yaxis3=dict(
            overlaying="y", side="right", range=[0, 120],
            showgrid=False,
            tickfont=dict(family="Space Mono", size=9),
            ticksuffix="%",
            title="Win Rate",
            position=1.0,
        ),
        legend=dict(
            orientation="h", x=0, y=-0.12,
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=11),
        ),
        hovermode="x unified",
    )

    st.plotly_chart(fig_trend, use_container_width=True, config={"displayModeBar": False})

    # Monthly breakdown table
    st.markdown('<div class="section-title" style="font-size:1.1rem;">Monthly Breakdown</div>', unsafe_allow_html=True)
    breakdown_df = pd.DataFrame({
        "Month": months,
        "W": wins_pm, "D": draws_pm, "L": losses_pm,
        "Pts": points_pm,
        "Goals": goals_pm,
        "xG": xg_pm,
        "xG Δ": [round(g-x,1) for g,x in zip(goals_pm, xg_pm)],
        "Win Rate %": win_rate
    })
    st.dataframe(
        breakdown_df.style
            .background_gradient(subset=["Pts"], cmap="Blues")
            .format({"xG": "{:.1f}", "xG Δ": "{:+.1f}"}),
        use_container_width=True, hide_index=True,
    )


# NAV 04 · PLAYER CONTRIBUTION vs AGE
elif nav == "Talent Mapping":
    st.markdown("""
    <div class="page-header">
        <div class="page-main-title">Player Contribution vs Age</div>
        <div class="page-desc">
            Squad mapped by Age × Minutes Played. Bubble size = Goal Contributions.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Data ──────────────────────────────────────────────────────────────────
    squad = pd.read_csv("data/squad_matrix.csv")

    age_mid     = squad["Age"].median()
    minutes_mid = squad["Minutes"].median()

    COLORS = {"FWD": "#A50044", "MID": "#004D98", "DEF": "#EDBB00", "GK": "#6B7A9A"}

    # KPI row
    c1, c2, c3, c4 = st.columns(4)
    for col, (k,v,s) in zip([c1,c2,c3,c4], [
        ("Squad Size",      len(squad), "Players tracked"),
        ("Avg Age",         f"{squad['Age'].mean():.1f}", "Squad average"),
        ("Future Stars",    int((squad.Age < age_mid).sum()), "Players below median age"),
        ("Total G+A",       int(squad["GA"].sum()), "Combined contributions"),
    ]):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{k}</div>
                <div class="metric-value">{v}</div>
                <div class="metric-sub">{s}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    # ── 4-Quadrant Bubble Scatter ──────────────────────────────────────────────
    fig_bubble = go.Figure()

    # Quadrant shading
    quad_fills = [
        (0,   age_mid,  minutes_mid, 4000, "rgba(237,187,0,0.05)",  "Young Talent"),
        (age_mid, 45,   minutes_mid, 4000, "rgba(0,77,152,0.05)",   "Core Pillars"),
        (0,   age_mid,  0, minutes_mid,    "rgba(165,0,68,0.04)",   "Prospects"),
        (age_mid, 45,   0, minutes_mid,    "rgba(107,122,154,0.04)","Veterans"),
    ]
    for x0, x1, y0, y1, fill, _ in quad_fills:
        fig_bubble.add_shape(type="rect", x0=x0, x1=x1, y0=y0, y1=y1,
                             fillcolor=fill, line=dict(width=0), layer="below")

    # Quadrant dividers
    fig_bubble.add_shape(type="line", x0=age_mid, x1=age_mid, y0=0, y1=4000,
                         line=dict(color="rgba(255,255,255,0.1)", width=1, dash="dot"))
    fig_bubble.add_shape(type="line", x0=14, x1=40, y0=minutes_mid, y1=minutes_mid,
                         line=dict(color="rgba(255,255,255,0.1)", width=1, dash="dot"))

    # Quadrant labels
    for x, y, txt in [
        (age_mid-4, minutes_mid+350, "⭐ RISING STAR"),
        (age_mid+1, minutes_mid+350, "🏆 STRONG PILLAR"),
        (age_mid-4, minutes_mid-400, "🌱 PROSPECTS"),
        (age_mid+1, minutes_mid-400, "📉 VETERANS"),
    ]:
        fig_bubble.add_annotation(
            x=x, y=y, text=txt, showarrow=False,
            font=dict(family="Space Mono", size=8, color="rgba(255,255,255,0.3)"),
            xanchor="center",
        )

    for pos in ["FWD","MID","DEF","GK"]:
        sub = squad[squad.Position == pos]
        fig_bubble.add_trace(go.Scatter(
            x=sub["Age"], y=sub["Minutes"],
            mode="markers+text",
            name=pos,
            text=sub["Player"],
            textposition="top center",
            textfont=dict(family="DM Sans", size=9, color="rgba(232,236,244,0.75)"),
            marker=dict(
                size=sub["GA"].apply(lambda v: max(8, v * 1.4)),
                color=COLORS[pos],
                opacity=0.85,
                line=dict(color="rgba(255,255,255,0.2)", width=1),
            ),
            hovertemplate=(
                "<b>%{text}</b><br>"
                "Age: %{x}<br>"
                "Minutes: %{y}<br>"
                "GA: %{customdata}<extra></extra>"
            ),
            customdata=sub["GA"],
        ))

    fig_bubble.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=520,
        margin=dict(l=10, r=20, t=20, b=20),
        font=dict(family="DM Sans", color="#E8ECF4"),
        xaxis=dict(
            title="Age", range=[15, 38],
            showgrid=True, gridcolor="rgba(255,255,255,0.04)",
            tickfont=dict(family="Space Mono", size=10),
        ),
        yaxis=dict(
            title="Minutes Played",
            showgrid=True, gridcolor="rgba(255,255,255,0.04)",
            tickfont=dict(family="Space Mono", size=10),
        ),
        legend=dict(
            orientation="h", x=0, y=-0.1,
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=11),
        ),
        hovermode="closest",
    )

    st.plotly_chart(fig_bubble, use_container_width=True, config={"displayModeBar": False})

    # Player table
    st.markdown('<div class="section-title" style="font-size:1.1rem;">Full Squad Matrix</div>', unsafe_allow_html=True)
    display_df = squad[["Player","Position","Age","Minutes","GA"]].sort_values("GA", ascending=False)

    st.dataframe(
        display_df.style.background_gradient(subset=["GA","Minutes"], cmap="Blues"),
        use_container_width=True, hide_index=True,
    )


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<hr style="border:none;border-top:1px solid rgba(255,255,255,0.07);margin-top:40px;">
<div style="text-align:center;font-family:'Space Mono',monospace;font-size:0.58rem;
            letter-spacing:0.12em;color:#3D4F70;text-transform:uppercase;padding:16px 0;">
    La Liga Analytics Dashboard
    Built with Streamlit · Plotly · Python
    Data Visualization & Sports Analytics
</div>
""", unsafe_allow_html=True)