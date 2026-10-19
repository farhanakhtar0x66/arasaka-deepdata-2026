"""DeepData 3.0 starter EDA dashboard. Run: streamlit run app.py"""
from pathlib import Path
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title='DeepData • Dataset Explorer', page_icon='📊', layout='wide')
st.title('📊 DeepData • Dataset Explorer')
st.caption('Practice dashboard. Inspect an uploaded CSV, identify quality issues, and tell a story with defensible charts.')

sample = Path(__file__).resolve().parent / 'data' / 'mock_water_network.csv'
file = st.file_uploader('Upload CSV', type=['csv'])
try:
    df = pd.read_csv(file) if file is not None else pd.read_csv(sample)
except Exception as exc:
    st.error(f'Could not read CSV: {exc}')
    st.stop()
if df.empty:
    st.warning('This CSV is empty.')
    st.stop()
st.caption(f'Data source: {file.name if file is not None else "Included synthetic water network practice data"}')

nrows, ncols, nmissing, ndupes = len(df), len(df.columns), int(df.isna().sum().sum()), int(df.duplicated().sum())
q1, q2, q3, q4 = st.columns(4)
q1.metric('Rows', f'{nrows:,}')
q2.metric('Columns', ncols)
q3.metric('Missing cells', f'{nmissing:,}')
q4.metric('Exact duplicates', f'{ndupes:,}')

with st.sidebar:
    st.header('Filters')
    potential = ['(none)'] + list(df.columns)
    target = st.selectbox('Optional target', potential,
                          index=potential.index('failed_next_30d') if 'failed_next_30d' in df else 0)
    cats = [c for c in df.select_dtypes(include=['object', 'category', 'bool']).columns
            if df[c].nunique(dropna=True) <= 25]
    chosen = st.selectbox('Filter by category', ['(none)'] + cats)
    if chosen != '(none)':
        choices = sorted(df[chosen].dropna().astype(str).unique().tolist())
        selected = st.multiselect('Show values', choices, default=choices)
        df_view = df[df[chosen].astype(str).isin(selected)]
    else:
        df_view = df

st.subheader('Data preview')
st.dataframe(df_view.head(100), use_container_width=True, hide_index=True)
with st.expander('Column quality & missingness', expanded=True):
    health = pd.DataFrame({
        'column': df.columns,
        'type': df.dtypes.astype(str).values,
        'missing_count': df.isna().sum().values,
        'missing_%': (df.isna().mean().values * 100).round(2),
        'unique_values': df.nunique(dropna=True).values,
    }).sort_values('missing_%', ascending=False)
    st.dataframe(health, use_container_width=True, hide_index=True)
    st.bar_chart(health.set_index('column')['missing_%'], x_label='Column', y_label='% missing')

if target != '(none)':
    st.subheader('Target distribution')
    target_series = df_view[target]
    if pd.api.types.is_numeric_dtype(target_series) and target_series.nunique(dropna=True) > 30:
        values = target_series.dropna().to_numpy()
        if len(values):
            counts, edges = np.histogram(values, bins=20)
            centers = [f'{(edges[i]+edges[i + 1]) / 2:.1f}' for i in range(len(counts))]
            st.bar_chart(pd.Series(counts, index=centers), x_label=target, y_label='Frequency')
        else:
            st.info('No nonmissing target values in this filter.')
    else:
        freq = target_series.fillna('(missing)').astype(str).value_counts()
        st.bar_chart(freq, x_label='Target class/value', y_label='Row count')

left, right = st.columns(2)
with left:
    st.subheader('Numeric distribution')
    numeric = list(df_view.select_dtypes(include=np.number).columns)
    if numeric:
        num = st.selectbox('Numeric column', numeric)
        values = df_view[num].dropna()
        if len(values):
            counts, edges = np.histogram(values.to_numpy(), bins=20)
            bin_labels = [f'{(edges[i]+edges[i+1])/2:.1f}' for i in range(len(counts))]
            st.bar_chart(pd.Series(counts, index=bin_labels), x_label=num, y_label='Frequency')
        else:
            st.info('No nonmissing values for this column.')
    else:
        st.info('No numeric columns.')
with right:
    st.subheader('Category comparison')
    cat_cols = [c for c in df_view.columns if df_view[c].nunique(dropna=True) <= 30]
    if cat_cols:
        cat = st.selectbox('Category column', cat_cols)
        st.bar_chart(df_view[cat].fillna('(missing)').astype(str).value_counts(),
                     x_label=cat, y_label='Count')
    else:
        st.info('No low-cardinality columns.')

st.subheader('Write your evidence-backed insight')
st.text_area('What did you observe? Why does it matter? What should someone do?',
             placeholder='For example: Group X has higher observed failure rate than Group Y; investigate with a controlled comparison.')
st.warning('Correlations are not proof of causation. Check leakage, missingness, sampling, and whether features existed at prediction time.')
st.download_button('Download filtered CSV', df_view.to_csv(index=False),
                   file_name='deepdata_filtered.csv', mime='text/csv')
