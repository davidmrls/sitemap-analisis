import streamlit as st
import pandas as pd
import advertools as adv
import adviz
import plotly.express as px
from urllib.parse import urlparse


st.title('Revisor de sitemaps')
#https://rentingfinders.com/sitemap_index.xml

sitemap_index_url = st.text_input('Introduce el sitemap')
st.text(sitemap_index_url)

if sitemap_index_url:
    sitemap_index = adv.sitemap_to_df(sitemap_index_url)
    sitemaps = (sitemap_index.assign(lastmod=lambda df: pd.to_datetime(df["lastmod"]),sitemap_cat=lambda df: df["sitemap"].str.split('/').str[3]).set_index("lastmod"))
    sitemaps['mcat'] = sitemaps['loc'].str.split('/').str[3]
    sitemaps['scat'] = sitemaps['loc'].str.split('/').str[4]
    st.write = st.header('Datos del sitemap')
    st.dataframe(sitemaps)
    #Sección para descargar CSV +  botón ----------
    @st.cache_data
    def convert_df(df):
    # IMPORTANT: Cach∫e the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')
    sitemap_csv = convert_df(sitemaps)
    st.download_button("Descargar CSV",sitemap_csv,(str(sitemap_index_url)+".csv"),"text/csv",key='download-csv')
    #-----------

      # El usuario introduce una URL
    #parsed_url = urlparse(sitemap_index_url)  # Analiza la URL
    #domain = parsed_url.netloc  # Extrae el nombre de dominio
    
    st_categorias = adviz.url_structure(sitemaps['loc'],domain='domain',items_per_level=20,height=700,title='Hola')
    st.plotly_chart(st_categorias, use_container_width=True)
    
    total_urls = sitemaps['sitemap_cat'].value_counts().sum()
    urls_por_sitemap = sitemaps['sitemap_cat'].value_counts()
    porcentajes = ((urls_por_sitemap / total_urls) * 100).round(2)

    df = pd.DataFrame({'Urls por sitemap': urls_por_sitemap,'Porcentaje (%)': porcentajes,})
    #Se establecen columnas de streamlit
    col1, col2 = st.columns([1, 1])
    col1.dataframe(df)
    #Poner total_urls arriba
    #col2.write(total_urls)
    col2.metric(label="Total de urls", value=total_urls)
    categorias_principales = sitemaps['mcat'].value_counts(normalize=True) * 100
    st.dataframe(categorias_principales)

    #Hasta aqui todo bien


    #Comprobamos el número de urls actualizadas en x tiempo
    urls_por_tiempo = sitemaps.resample('M')['loc'].count().to_frame()
    st.dataframe(urls_por_tiempo)
    pd.options.plotting.backend = "plotly"
    fig = urls_por_tiempo.plot(title="Urls por tiempo", template="plotly_dark",labels=dict(index="time", value="urls", variable="Sitemap"))
    st.plotly_chart(fig)


    #Creamos un dataframe con solo loc y datos de tiempo (Justo lo anterior)
    #fig = px.bar(urls_por_tiempo, x="loc", y="count", color="medal", title="Long-Form Input")
    #st.plotly_chart(fig)

