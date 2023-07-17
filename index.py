import streamlit as st
import pandas as pd
import advertools as adv
import adviz
from urllib.parse import urlparse


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
      # El usuario introduce una URL
    #parsed_url = urlparse(sitemap_index_url)  # Analiza la URL
    #domain = parsed_url.netloc  # Extrae el nombre de dominio
    
    st_categorias = adviz.url_structure(sitemaps['loc'],domain='domain',items_per_level=20,height=700,title='Hola')
    st.plotly_chart(st_categorias, use_container_width=True)
    total_urls = sitemaps['sitemap_cat'].value_counts().sum()
    urls_por_sitemap = sitemaps['sitemap_cat'].value_counts()
    porcentajes = (urls_por_sitemap / total_urls) * 100
    df = pd.DataFrame({'urls_por_sitemap': urls_por_sitemap,'porcentaje': porcentajes,})
    #Se establecen columnas de streamlit
    col1, col2 = st.columns([1, 1])
    col1.dataframe(df)
    #Poner total_urls arriba
    col2.write(total_urls)
    

