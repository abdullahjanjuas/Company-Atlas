import io
import pandas as pd
import streamlit as st
import altair as alt

# ---------- Page setup ----------
st.set_page_config(page_title="Company Atlas", layout="wide")

# ---------- Sidebar ----------
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/company.png", width=80)  # Company icon
    st.markdown("## Company Atlas")
    st.caption("📊 Explore and download company clusters")
    st.markdown("---")
    st.info("Tip: Start by uploading your dataset →")


# ----------------- Dark Theme Styling -----------------
st.markdown(
    """
    <style>
    /* Whole app background */
    .stApp {
        background-color: #121212;
        color: #e0e0e0;
    }

    /* Main content container */
    .block-container {
        background-color: #1e1e1e !important; 
        border-radius: 8px;
        padding: 1rem;
    }

/* Title */
h1 {
    color: #90caf9;
    text-align: center;
    margin-top: 30px !important;     /* space above */
    margin-bottom: 40px !important;  /* space below */
}
h2, h3 {
    color: #bbdefb;
}


    /* Buttons */
    div.stButton > button {
        background-color: #1e88e5;
        color: white;
        border-radius: 8px;
        padding: 0.6em 1em;
        font-weight: 600;
        transition: 0.3s;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.4);
    }
    div.stButton > button:hover {
        background-color: #1565c0;
        transform: scale(1.02);
        box-shadow: 0px 6px 18px rgba(0,0,0,0.6);
    }

    /* DataFrame background */
    .stDataFrame {
        background-color: #2c2c2c;
        border-radius: 6px;
    }

    /* Expander header */
    .streamlit-expanderHeader {
        background-color: #333333 !important;
        color: #90caf9 !important;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Title ----------
st.markdown("<h1>🌐 Company Atlas</h1>", unsafe_allow_html=True)

# ---------- Instructions (toggleable) ----------
with st.expander("How this works"):
    st.markdown(
        """
1. Upload the dataset CSV provided along with this script.
2. Click a **coarse cluster** (e.g., `Technology Services` or `General`).
3. Click a **fine cluster** (e.g., `Services and Products`, `Business Solutions`, `Healthcare Technology`, `Digital Services Marketing`, or `General`).
4. View the matching rows and **download** them as CSV.

**Required columns:** `fine_label`, `coarse_label`.  
Other columns (e.g., `uuid`, `name`, `description`, etc.) are shown as-is.
"""
    )

# ---------- Session state ----------
if "stage" not in st.session_state:
    st.session_state.stage = "coarse"
if "selected_coarse" not in st.session_state:
    st.session_state.selected_coarse = None
if "selected_fine" not in st.session_state:
    st.session_state.selected_fine = None

# ---------- Data loader ----------
@st.cache_data(show_spinner=False)
def load_data(file) -> pd.DataFrame:
    df = pd.read_csv(file)
    df.columns = [c.strip() for c in df.columns]
    required = {"coarse_label", "fine_label"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required column(s): {', '.join(missing)}")
    return df

# ---------- Display Label Mapper ----------
def display_label(label):
    """Show 'General' instead of 'Unclustered' on frontend"""
    return "General" if label == "Unclustered" else label

# ---------- File input ----------
left, right = st.columns([3, 2])
with left:
    uploaded = st.file_uploader("Upload your dataset CSV", type=["csv"])
with right:
    sample_cols = st.toggle("Show first 10 rows after loading", value=False)

df = None
if uploaded is not None:
    df = load_data(uploaded)
else:
    st.info("Upload your CSV to begin. (Columns must include `coarse_label` and `fine_label`.)")

# ---------- Main Logic ----------
if df is not None:
    if sample_cols:
        st.dataframe(df.head(10), use_container_width=True)

    df_display = df.copy()
    df_display["coarse_label"] = df_display["coarse_label"].replace("Unclustered", "General")

    # ---------- Metrics ----------
    total_rows = len(df)
    coarse_counts = df.groupby("coarse_label").size().sort_values(ascending=False)
    st.metric("Total Companies", total_rows)

    # ---------- Cluster Overview Chart ----------
    st.subheader("Cluster Overview")
    coarse_chart = (
        alt.Chart(df_display)
        .mark_bar()
        .encode(
            x="coarse_label:N",
            y="count():Q",
            color="coarse_label:N"
        )
    )
    st.altair_chart(coarse_chart, use_container_width=True)

    # ---------- Stage: COARSE ----------
    if st.session_state.stage == "coarse":
        st.subheader("Step 1 — Pick a Coarse Cluster")
        coarse_list = coarse_counts.index.tolist()
        cols_per_row = 3 if len(coarse_list) > 2 else len(coarse_list) or 1
        rows = (len(coarse_list) + cols_per_row - 1) // cols_per_row

        idx = 0
        for r in range(rows):
            row_cols = st.columns(cols_per_row)
            for c in range(cols_per_row):
                if idx >= len(coarse_list):
                    break
                coarse = coarse_list[idx]
                count = coarse_counts.loc[coarse]
                with row_cols[c]:
                    display_name = display_label(coarse)
                    if st.button(f"{display_name} ({count})", use_container_width=True):
                        st.session_state.selected_coarse = coarse
                        st.session_state.stage = "fine"
                idx += 1

        st.caption(f"Total rows: {total_rows}")
        st.markdown("---")

    # ---------- Stage: FINE ----------
    if st.session_state.stage == "fine":
        coarse = st.session_state.selected_coarse
        st.subheader(f"Step 2 — Fine Clusters in: **{display_label(coarse)}**")
        st.button("← Back to Coarse Clusters", on_click=lambda: st.session_state.update(stage="coarse"))

        df_coarse = df[df["coarse_label"] == coarse]
        fine_counts = df_coarse.groupby("fine_label").size().sort_values(ascending=False)

        if fine_counts.empty:
            st.warning("No fine clusters found under this coarse cluster.")
        else:
            fine_list = fine_counts.index.tolist()
            cols_per_row = 3 if len(fine_list) > 2 else len(fine_list) or 1
            rows = (len(fine_list) + cols_per_row - 1) // cols_per_row

            idx = 0
            for r in range(rows):
                row_cols = st.columns(cols_per_row)
                for c in range(cols_per_row):
                    if idx >= len(fine_list):
                        break
                    fine = fine_list[idx]
                    count = fine_counts.loc[fine]
                    with row_cols[c]:
                        display_name = display_label(fine)
                        if st.button(f"{display_name} ({count})", use_container_width=True, key=f"fine_{fine}_{idx}"):
                            st.session_state.selected_fine = fine
                            st.session_state.stage = "results"
                    idx += 1

            st.caption(f"Rows in '{display_label(coarse)}': {len(df_coarse)}")
            st.markdown("---")

    # ---------- Stage: RESULTS ----------
    if st.session_state.stage == "results":
        coarse = st.session_state.selected_coarse
        fine = st.session_state.selected_fine
        st.subheader(f"Results — {display_label(coarse)} ➜ {display_label(fine)}")
        st.markdown("---")

        nav_cols = st.columns([1, 1, 6])
        with nav_cols[0]:
            st.button("← Back to Fine", on_click=lambda: st.session_state.update(stage="fine"))
        with nav_cols[1]:
            st.button("⟲ Reset", on_click=lambda: st.session_state.update(stage="coarse", selected_coarse=None, selected_fine=None))

        filtered = df[(df["coarse_label"] == coarse) & (df["fine_label"] == fine)]
        st.write(f"Matching rows: **{len(filtered)}**")
        st.dataframe(filtered, use_container_width=True)

        csv_bytes = filtered.to_csv(index=False).encode("utf-8")
        st.download_button(
            label=f"Download CSV for {display_label(fine)}",
            data=csv_bytes,
            file_name=f"{coarse}__{fine}.csv",
            mime="text/csv",
            use_container_width=True
        )
