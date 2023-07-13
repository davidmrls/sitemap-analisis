import streamlit as st
import pandas as pd
import advertools as adv


st.title('Revisor de sitemaps')
#https://rentingfinders.com/sitemap_index.xml

sitemap_index_url = st.text_input('Introduce el sitemap')
st.text(sitemap_index_url)

if sitemap_index_url:
    sitemap_index = adv.sitemap_to_df(sitemap_index_url)
    sitemaps = (sitemap_index.assign(lastmod=lambda df: pd.to_datetime(df["lastmod"]),sitemap_cat=lambda df: df["sitemap"].str.split('/').str[3]).set_index("lastmod"))
    #sitemaps['mcat'] = sitemaps['loc'].str.split('/').str[3]
    #sitemaps['scat'] = sitemaps['loc'].str.split('/').str[4]
    st.write = st.header('Datos del sitemap')
    st.dataframe(sitemaps)
    @st.cache_data
    def convert_df(df):
    # IMPORTANT: Cach∫e the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')
    sitemap_csv = convert_df(sitemaps)
    st.download_button("Descargar CSV",sitemap_csv,(str(sitemap_index_url)+".csv"),"text/csv",key='download-csv')

