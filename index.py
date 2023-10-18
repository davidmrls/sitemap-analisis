import streamlit as st
import pandas as pd
import advertools as adv
import adviz
import plotly.express as px
from urllib.parse import urlparse

st.title('Revisor de sitemaps')

url_sitemap = st.text_input('Introduce el sitemap')
st.text(url_sitemap)

#Análisis del sitemap o índice de sitemaps con Advertools

if url_sitemap:
    info_sitemap = adv.sitemap_to_df(url_sitemap)
    sitemaps = (info_sitemap.assign(lastmod=lambda df: pd.to_datetime(df["lastmod"]),sitemap_cat=lambda df: df["sitemap"].str.split('/').str[3]).set_index("lastmod"))

    #Limpia el sitemap de respuestas sin datos y extrae jerarquías principales
    sitemaps['loc'] = sitemaps['loc'].replace({None: 'URL_Faltante'})
    sitemaps['cat1'] = sitemaps['loc'].str.split('/').str[3]
    sitemaps['cat2'] = sitemaps['loc'].str.split('/').str[4]
    st.header('Datos del sitemap')

    st.dataframe(sitemaps)

    sitemap_utf = sitemaps.to_csv().encode('utf-8')
    st.download_button("Descargar CSV",sitemap_utf,(str(url_sitemap)+".csv"),"text/csv",key='descarga-csv')

    #Extrae nombre de dominio para visualización
    root_dom = urlparse(url_sitemap)
    dominio = root_dom.netloc
    adviz_title = "Análisis: " + url_sitemap
    
    #Usamos Adviz para mostrar estructura del site
    st_categorias = adviz.url_structure(sitemaps['loc'],domain=str(dominio),items_per_level=20,height=700,title=str(adviz_title))
    st.plotly_chart(st_categorias, use_container_width=True)
    
    total_urls = sitemaps['sitemap_cat'].value_counts().sum()
    urls_por_sitemap = sitemaps['sitemap_cat'].value_counts()
    porcentajes = ((urls_por_sitemap / total_urls) * 100).round(2)

    # Comprobamos urls con /blog en la url
    urls_blog = (sitemaps['cat1'] == 'blog').sum()
    
    if urls_blog == 0:
      urls_blog = "Nada"
    else:
        urls_blog = str(urls_blog)

    col1, col2 = st.columns([1, 1])
    col1.metric(label="Total de urls", value=total_urls)
    col2.metric(label="URLs de blog", value=urls_blog)

    #Frecuencia de actualización
    st.subheader("Frecuencia de actualización urls")
    urls_por_tiempo = sitemaps.resample('M')['loc'].count()
    expander = st.expander("Tabla frecuencia de actualización urls")
    expander.dataframe(urls_por_tiempo)

    pd.options.plotting.backend = "plotly"
    graf_urls = urls_por_tiempo.plot(template="plotly_dark",labels=dict(index="time", value="urls", variable="Sitemap"))
    st.plotly_chart(graf_urls)

    col3, col4 = st.columns([1,1])

    col3.subheader('Urls por sitemap')
    datos_urlsitemap = pd.DataFrame({'Urls Sitemap': urls_por_sitemap,'Porcentaje(%)': porcentajes,})
    col3.dataframe(datos_urlsitemap)

    col4.subheader("Categorías Principales")
    categorias_principales = sitemaps['cat1'].value_counts(normalize=True).mul(100).round(2).reset_index()

    categorias_principales.columns = ['Categorías', 'Porcentaje(%)']
    col4.dataframe(categorias_principales)

    st.subheader("Análisis de frecuencia de actualización por categoría")
    lista_categorias = categorias_principales['Categorías'].tolist()
    selec_categoria = st.selectbox('Selecciona una categoría para ver su frecuencia de actualización:', lista_categorias)

    #Filtro por jerarquía
    filtro_url = sitemaps[sitemaps['cat1'] == selec_categoria]
    
    #Frecuenia de actualización
    frec_estructura = filtro_url.resample('M')['loc'].count()
    frec_estructura.columns = ['Frecuencia de actualización']
    pd.options.plotting.backend = "plotly"
    graf_urls_cat = frec_estructura.plot(title=f'Frecuencia de actualización de {selec_categoria}', template="plotly_dark", labels=dict(index="time", value="urls", variable=selec_categoria))
    st.plotly_chart(graf_urls_cat)