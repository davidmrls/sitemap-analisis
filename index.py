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
    #sitemaps['loc'] = ['URL_Faltante' if x is None else x for x in sitemaps['loc']]
    sitemaps['loc'] = sitemaps['loc'].replace({None: 'URL_Faltante'})
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

    df = pd.DataFrame({'Urls Sitemap': urls_por_sitemap,'Porcentaje(%)': porcentajes,})
    # Calculamos el número de URLs con 'blog' en la columna 'mcat' usando sum()
    urls_blog = (sitemaps['mcat'] == 'blog').sum()

    # Si no hay ninguna URL con 'blog', establecemos la métrica a "Nada"
    if urls_blog == 0:
      urls_blog = "Nada"
    else:
        urls_blog = str(urls_blog)

    #Se establecen columnas de streamlit
    col1, col2 = st.columns([1, 1])
    col1.dataframe(df)
    #Poner total_urls arriba
    #col2.write(total_urls)
    col2.metric(label="Total de urls", value=total_urls)
    col2.metric(label="URLs de blog", value=urls_blog)

    st.subheader("Categorías Principales")
    categorias_principales = sitemaps['mcat'].value_counts(normalize=True).mul(100).round(2).reset_index()
    #categorias_principales = sitemaps['mcat'].value_counts(normalize=True) * 100
    categorias_principales.columns = ['Categorías', 'Porcentaje(%)']
    st.dataframe(categorias_principales)

    #-------NUEVO----------

    st.subheader("Análisis de Frecuencia de Actualización por Categoría")
    # Obtener la lista de categorías
    lista_categorias = categorias_principales['Categorías'].tolist()

    # Crear un selector para el valor mcat
    selected_mcat = st.selectbox('Selecciona una categoría para ver su frecuencia de actualización:', lista_categorias)

    # Filtrar las URLs basándonos en el valor seleccionado en 'selected_mcat'
    filtered_urls = sitemaps[sitemaps['mcat'] == selected_mcat]

    # Mostrar la frecuencia de actualización de las URLs filtradas
    urls_updated_frequency = filtered_urls.resample('M')['loc'].count()
    urls_updated_frequency.columns = ['Frecuencia de Actualización']

    col1.dataframe(urls_updated_frequency)

    # Configurar el backend de plotting para Plotly
    pd.options.plotting.backend = "plotly"

    # Crear un gráfico basado en el método .plot()
    fig1 = urls_updated_frequency.plot(title=f'Frecuencia de Actualización de {selected_mcat} durante el tiempo', template="plotly_dark", labels=dict(index="time", value="urls", variable=selected_mcat))

    # Mostrar el gráfico en streamlit
    col2.plotly_chart(fig1)

    #------HASTA AQUI NUEVO----------

    #Hasta aqui todo bien
    st.subheader("URLs por Tiempo")
    #Comprobamos el número de urls actualizadas en x tiempo
    urls_por_tiempo = sitemaps.resample('M')['loc'].count().to_frame()
    st.dataframe(urls_por_tiempo)
    pd.options.plotting.backend = "plotly"
    fig2 = urls_por_tiempo.plot(title="Urls por tiempo", template="plotly_dark",labels=dict(index="time", value="urls", variable="Sitemap"))
    st.plotly_chart(fig2)


    #Creamos un dataframe con solo loc y datos de tiempo (Justo lo anterior)
    #fig = px.bar(urls_por_tiempo, x="loc", y="count", color="medal", title="Long-Form Input")
    #st.plotly_chart(fig)

# Añade estilos CSS


#Se pueden añadir funcionalidades como filtrado del csv en el propio streamlit
