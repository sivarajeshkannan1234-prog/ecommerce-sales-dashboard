from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="E-Commerce Sales Analytics",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "ecommerce_customer_sales_6000.csv"

# Professional dashboard styling
st.markdown(
    """
    <style>
    :root {
        --navy: #14213d;
        --blue: #2563eb;
        --blue-light: #eff6ff;
        --page: #f4f7fb;
        --text: #182230;
        --muted: #64748b;
        --border: #e2e8f0;
        --white: #ffffff;
    }

    .stApp {
        background: var(--page);
        color: var(--text);
    }

    .block-container {
        max-width: 1600px;
        padding: 1.2rem 1.6rem 2.5rem;
    }

    h1, h2, h3, h4, p, label {
        color: var(--text);
    }

    .dashboard-header {
        background: linear-gradient(120deg, #14213d 0%, #1d4ed8 100%);
        padding: 1.35rem 1.5rem;
        border-radius: 18px;
        margin-bottom: 1.15rem;
        color: white;
        box-shadow: 0 8px 22px rgba(20, 33, 61, 0.13);
    }

    .dashboard-header h1 {
        color: white !important;
        text-align: center;
        font-size: clamp(1.45rem, 2.8vw, 2.25rem);
        margin: 0 0 .45rem 0;
        font-weight: 800;
    }

    .dashboard-header p {
        color: #eaf1ff !important;
        text-align: center;
        margin: 0;
        font-size: .95rem;
    }

    .section-heading {
        font-size: 1.12rem;
        font-weight: 750;
        color: #14213d;
        margin: .4rem 0 .7rem;
    }

    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 1rem 1rem .85rem;
        box-shadow: 0 3px 12px rgba(15, 23, 42, .045);
        min-height: 108px;
    }

    div[data-testid="stMetricLabel"] p {
        color: #526179 !important;
        font-weight: 650 !important;
        font-size: .83rem !important;
    }

    div[data-testid="stMetricValue"] div {
        color: #14213d !important;
        font-weight: 800 !important;
        font-size: clamp(1.2rem, 2vw, 1.85rem) !important;
    }

    section[data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid var(--border);
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #14213d !important;
    }

    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span {
        color: #253247;
    }

    div[data-baseweb="select"] > div {
        background: #ffffff !important;
        border-color: #cbd5e1 !important;
        border-radius: 8px !important;
    }

    div[data-baseweb="select"] input,
    div[data-baseweb="select"] span {
        color: #182230 !important;
        -webkit-text-fill-color: #182230 !important;
    }

    div[data-testid="stPlotlyChart"],
    div[data-testid="stDataFrame"] {
        background: #ffffff;
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: .35rem;
        box-shadow: 0 3px 12px rgba(15, 23, 42, .035);
    }

    .info-strip {
        color: #475569;
        font-size: .86rem;
        padding: .45rem .1rem .8rem;
    }

    .stButton button, .stDownloadButton button {
        border-radius: 9px;
        font-weight: 650;
    }

    hr {
        border-color: #e2e8f0;
    }

    @media (max-width: 768px) {
        .block-container {
            padding: .8rem .55rem 1.5rem;
        }
        .dashboard-header {
            padding: 1rem .7rem;
            border-radius: 12px;
        }
        .dashboard-header p {
            font-size: .82rem;
        }
        div[data-testid="stMetric"] {
            min-height: 92px;
            padding: .7rem .55rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# DATA LOADING AND PREPARATION
# ---------------------------------------------------------
@st.cache_data
def load_data(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)

    # Normalize column names to avoid accidental leading/trailing spaces.
    df.columns = [str(column).strip() for column in df.columns]

    if "Order_Date" in df.columns:
        df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")

    for column in ["Revenue", "Quantity", "Unit_Price", "Discount", "Customer_Age"]:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    if "Customer_Age" in df.columns:
        df["Age_Group"] = pd.cut(
            df["Customer_Age"],
            bins=[0, 25, 35, 45, 55, 65, float("inf")],
            labels=["18-25", "26-35", "36-45", "46-55", "56-65", "66+"],
            include_lowest=True,
        )

    if "Order_Date" in df.columns:
        df["YearMonth"] = df["Order_Date"].dt.to_period("M").astype("string")

    return df


def format_money(value: float) -> str:
    """Format rupee values compactly for KPI cards."""
    value = float(value or 0)
    if abs(value) >= 1_000_000:
        return f"₹{value / 1_000_000:.2f}M"
    if abs(value) >= 1_000:
        return f"₹{value / 1_000:.1f}K"
    return f"₹{value:,.0f}"


def chart_style(fig, height: int = 330):
    """Apply shared readable styling to Plotly charts."""
    fig.update_layout(
        height=height,
        autosize=True,
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        margin=dict(l=12, r=20, t=48, b=18),
        font=dict(family="Arial, sans-serif", size=12, color="#243247"),
        title_font=dict(size=15, color="#14213d"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
            font=dict(size=11, color="#475569"),
        ),
        hoverlabel=dict(
            bgcolor="#14213d",
            font=dict(color="#ffffff", size=12),
        ),
    )
    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        automargin=True,
        tickfont=dict(color="#475569", size=10),
        title_font=dict(color="#334155", size=11),
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor="#e9eef5",
        zeroline=False,
        automargin=True,
        tickfont=dict(color="#475569", size=10),
        title_font=dict(color="#334155", size=11),
    )
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"responsive": True, "displaylogo": False},
    )


def render_bar(data, x, y, horizontal=False, color="#2563eb", height=330):
    fig = px.bar(
        data,
        x=x if not horizontal else y,
        y=y if not horizontal else x,
        orientation="v" if not horizontal else "h",
        color_discrete_sequence=[color],
    )
    fig.update_traces(
        marker_line_width=0,
        hovertemplate="%{y}: %{x:,.2f}<extra></extra>" if horizontal
        else "%{x}: %{y:,.2f}<extra></extra>",
    )
    chart_style(fig, height=height)


# ---------------------------------------------------------
# PAGE HEADER
# ---------------------------------------------------------
st.markdown(
    """
    <div class="dashboard-header">
        <h1>🛍️ E-Commerce Customer Behavior &amp; Sales Analytics</h1>
        <p>Sales Performance&nbsp; | &nbsp;Customer Behavior&nbsp; | &nbsp;Product &amp; Regional Analysis</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if not DATA_FILE.exists():
    st.error(f"Dataset not found: {DATA_FILE}")
    st.info(
        "Check that ecommerce_customer_sales_6000.csv is inside the project's data folder."
    )
    st.stop()

try:
    raw_data = load_data(str(DATA_FILE))
except Exception as exc:
    st.error(f"Could not read the CSV file: {exc}")
    st.stop()

required_columns = [
    "Revenue", "Order_ID", "Customer_ID", "Product_Name", "Category",
    "State", "Customer_Gender", "Payment_Method",
]
missing_columns = [column for column in required_columns if column not in raw_data.columns]
if missing_columns:
    st.error("The dataset is missing these required columns: " + ", ".join(missing_columns))
    st.stop()

if raw_data.empty:
    st.warning("The dataset is empty.")
    st.stop()


# ---------------------------------------------------------
# FILTERS
# ---------------------------------------------------------
st.sidebar.markdown("## 🎛️ Dashboard Filters")
st.sidebar.caption("Choose values to update all KPIs and charts.")

filtered = raw_data.copy()
filter_config = [
    ("Category", "Product Category"),
    ("State", "State / Region"),
    ("Customer_Gender", "Customer Gender"),
    ("Payment_Method", "Payment Method"),
]

for column, label in filter_config:
    choices = sorted(filtered[column].dropna().unique().tolist(), key=lambda value: str(value))
    selected_values = st.sidebar.multiselect(
        label,
        options=choices,
        default=choices,
        key=f"filter_{column}",
        help=f"Select one or more {label.lower()} values.",
    )
    filtered = filtered[filtered[column].isin(selected_values)]

if st.sidebar.button("Reset all filters", use_container_width=True):
    for column, _ in filter_config:
        st.session_state[f"filter_{column}"] = sorted(
            raw_data[column].dropna().unique().tolist(),
            key=lambda value: str(value),
        )
    st.rerun()

if filtered.empty:
    st.warning("No records match the selected filters. Please change your filters.")
    st.stop()

st.markdown(
    f'<div class="info-strip">Showing <b>{len(filtered):,}</b> of '
    f'<b>{len(raw_data):,}</b> dataset rows after filtering.</div>',
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# KPI CARDS
# ---------------------------------------------------------
revenue = filtered["Revenue"].fillna(0).sum()
orders = filtered["Order_ID"].nunique()
customers = filtered["Customer_ID"].nunique()
products = filtered["Product_Name"].nunique()
average_order_value = revenue / orders if orders else 0

st.markdown('<div class="section-heading">📈 Sales Performance</div>', unsafe_allow_html=True)
kpi_columns = st.columns(5)
kpi_columns[0].metric("Total Revenue", format_money(revenue))
kpi_columns[1].metric("Total Orders", f"{orders:,}")
kpi_columns[2].metric("Total Customers", f"{customers:,}")
kpi_columns[3].metric("Total Products", f"{products:,}")
kpi_columns[4].metric("Average Order Value", format_money(average_order_value))


# ---------------------------------------------------------
# REVENUE BY GENDER AND DISCOUNT
# ---------------------------------------------------------
st.divider()
left, right = st.columns([1, 1.35], gap="medium")

with left:
    st.markdown('<div class="section-heading">Revenue by Gender</div>', unsafe_allow_html=True)
    gender_data = (
        filtered.groupby("Customer_Gender", dropna=False)["Revenue"]
        .sum().reset_index()
    )
    gender_data["Customer_Gender"] = gender_data["Customer_Gender"].fillna("Unknown")
    fig = px.pie(
        gender_data,
        names="Customer_Gender",
        values="Revenue",
        hole=0.62,
        color_discrete_sequence=["#2563eb", "#60a5fa", "#93c5fd", "#94a3b8"],
    )
    fig.update_traces(
        textposition="outside",
        textinfo="percent",
        marker=dict(line=dict(color="#ffffff", width=3)),
        hovertemplate="%{label}<br>Revenue: ₹%{value:,.2f}<br>Share: %{percent}<extra></extra>",
    )
    fig.add_annotation(
        text=format_money(revenue),
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=17, color="#14213d"),
    )
    chart_style(fig, 315)

with right:
    st.markdown('<div class="section-heading">Revenue by Discount</div>', unsafe_allow_html=True)
    if "Discount" in filtered.columns:
        discount_data = (
            filtered.dropna(subset=["Discount"])
            .groupby("Discount", as_index=False)["Revenue"]
            .sum().sort_values("Discount")
        )
        discount_data["Discount_Label"] = discount_data["Discount"].map(
            lambda value: f"{value:g}"
        )
        fig = px.bar(
            discount_data,
            x="Discount_Label",
            y="Revenue",
            text="Revenue",
            labels={"Discount_Label": "Discount", "Revenue": "Revenue (₹)"},
            color_discrete_sequence=["#2563eb"],
        )
        fig.update_traces(
            texttemplate="%{y:.3s}",
            textposition="outside",
            cliponaxis=False,
            hovertemplate="Discount: %{x}<br>Revenue: ₹%{y:,.2f}<extra></extra>",
        )
        chart_style(fig, 315)
    else:
        st.info("The dataset does not contain a Discount column.")


# ---------------------------------------------------------
# MONTHLY REVENUE TREND
# ---------------------------------------------------------
st.divider()
st.markdown('<div class="section-heading">Monthly Revenue Trend</div>', unsafe_allow_html=True)

if "Order_Date" in filtered.columns:
    monthly_data = filtered.dropna(subset=["Order_Date"]).copy()
    monthly_data["Month"] = monthly_data["Order_Date"].dt.to_period("M").astype(str)
    monthly_data = (
        monthly_data.groupby("Month", as_index=False)["Revenue"]
        .sum().sort_values("Month")
    )
    if not monthly_data.empty:
        fig = px.line(
            monthly_data,
            x="Month",
            y="Revenue",
            markers=True,
            labels={"Month": "Month", "Revenue": "Revenue (₹)"},
        )
        fig.update_traces(
            line=dict(color="#2563eb", width=3),
            marker=dict(size=7, color="#2563eb", line=dict(color="#ffffff", width=1.5)),
            hovertemplate="%{x}<br>Revenue: ₹%{y:,.2f}<extra></extra>",
        )
        chart_style(fig, 350)


# ---------------------------------------------------------
# CATEGORY AND TOP PRODUCTS
# ---------------------------------------------------------
st.divider()
left, right = st.columns(2, gap="medium")

with left:
    st.markdown('<div class="section-heading">Revenue by Category</div>', unsafe_allow_html=True)
    category_data = (
        filtered.groupby("Category", as_index=False)["Revenue"]
        .sum().sort_values("Revenue", ascending=True)
    )
    fig = px.bar(
        category_data,
        x="Revenue",
        y="Category",
        orientation="h",
        text="Revenue",
        labels={"Revenue": "Revenue (₹)", "Category": ""},
        color_discrete_sequence=["#2563eb"],
    )
    fig.update_traces(
        texttemplate="%{x:.3s}",
        textposition="outside",
        cliponaxis=False,
        hovertemplate="%{y}<br>Revenue: ₹%{x:,.2f}<extra></extra>",
    )
    chart_style(fig, 360)

with right:
    st.markdown('<div class="section-heading">Top 10 Products by Revenue</div>', unsafe_allow_html=True)
    product_data = (
        filtered.groupby("Product_Name", as_index=False)["Revenue"]
        .sum().nlargest(10, "Revenue").sort_values("Revenue", ascending=True)
    )
    fig = px.bar(
        product_data,
        x="Revenue",
        y="Product_Name",
        orientation="h",
        text="Revenue",
        labels={"Revenue": "Revenue (₹)", "Product_Name": ""},
        color_discrete_sequence=["#0f766e"],
    )
    fig.update_traces(
        texttemplate="%{x:.3s}",
        textposition="outside",
        cliponaxis=False,
        hovertemplate="%{y}<br>Revenue: ₹%{x:,.2f}<extra></extra>",
    )
    chart_style(fig, 360)


# ---------------------------------------------------------
# PAYMENT METHOD AND AGE GROUP
# ---------------------------------------------------------
st.divider()
left, right = st.columns(2, gap="medium")

with left:
    st.markdown('<div class="section-heading">Orders by Payment Method</div>', unsafe_allow_html=True)
    payment_data = (
        filtered.groupby("Payment_Method")["Order_ID"]
        .nunique().sort_values(ascending=True)
        .reset_index(name="Orders")
    )
    fig = px.bar(
        payment_data,
        x="Orders",
        y="Payment_Method",
        orientation="h",
        text="Orders",
        labels={"Orders": "Number of Orders", "Payment_Method": ""},
        color_discrete_sequence=["#2563eb"],
    )
    fig.update_traces(
        textposition="outside",
        cliponaxis=False,
        hovertemplate="%{y}<br>Orders: %{x:,}<extra></extra>",
    )
    chart_style(fig, 350)

with right:
    st.markdown('<div class="section-heading">Revenue by Age Group</div>', unsafe_allow_html=True)
    if "Age_Group" in filtered.columns:
        age_data = filtered.dropna(subset=["Age_Group"]).copy()
        age_data = (
            age_data.groupby("Age_Group", observed=False, as_index=False)["Revenue"]
            .sum()
        )
        age_data = age_data[age_data["Revenue"].notna()]
        fig = px.bar(
            age_data,
            x="Age_Group",
            y="Revenue",
            text="Revenue",
            labels={"Age_Group": "Age Group", "Revenue": "Revenue (₹)"},
            color_discrete_sequence=["#7c3aed"],
        )
        fig.update_traces(
            texttemplate="%{y:.3s}",
            textposition="outside",
            cliponaxis=False,
            hovertemplate="Age: %{x}<br>Revenue: ₹%{y:,.2f}<extra></extra>",
        )
        chart_style(fig, 350)


# ---------------------------------------------------------
# REVENUE BY STATE
# ---------------------------------------------------------
st.divider()
st.markdown('<div class="section-heading">Revenue by State</div>', unsafe_allow_html=True)
state_data = (
    filtered.groupby("State", as_index=False)["Revenue"]
    .sum().nlargest(10, "Revenue").sort_values("Revenue", ascending=True)
)
fig = px.bar(
    state_data,
    x="Revenue",
    y="State",
    orientation="h",
    text="Revenue",
    labels={"Revenue": "Revenue (₹)", "State": ""},
    color_discrete_sequence=["#2563eb"],
)
fig.update_traces(
    texttemplate="%{x:.3s}",
    textposition="outside",
    cliponaxis=False,
    hovertemplate="%{y}<br>Revenue: ₹%{x:,.2f}<extra></extra>",
)
chart_style(fig, 360)


# ---------------------------------------------------------
# FILTERED DATA TABLE AND DOWNLOAD
# ---------------------------------------------------------
st.divider()
st.markdown('<div class="section-heading">Sales Data Details</div>', unsafe_allow_html=True)

with st.expander("Preview filtered records"):
    st.dataframe(
        filtered.head(1000),
        use_container_width=True,
        hide_index=True,
    )

st.download_button(
    label="⬇️ Download Filtered Sales Data (CSV)",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="filtered_ecommerce_sales.csv",
    mime="text/csv",
    use_container_width=True,
)

st.caption(
    "E-Commerce Sales Analytics • Built with Python, Pandas, Plotly and Streamlit"
)
