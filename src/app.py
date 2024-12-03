import streamlit as st
from data_cleaning import load_cotton_data, load_weather_data
from analysis import (
    analyze_seasonal_trends,
    analyze_regional_potential,
    analyze_climatic_influences,
    analyze_historical_trends,
)
from visualization import (
    plot_seasonal_trends,
    plot_regional_map,
    plot_climatic_influence,
    plot_historical_trends,
    plot_scatter,
    plot_correlation_heatmap,
)

# Configuração da página
st.set_page_config(page_title="Análise do Algodão no Brasil", layout="wide")

# Título e introdução
st.title("Análise de Dados: Plantio e Colheita de Algodão")
st.markdown(
    """
Este painel interativo analisa dados históricos de plantio de algodão e condições climáticas no Brasil. 
Explore insights como os melhores períodos e regiões para plantio, além de tendências históricas e impactos climáticos.
"""
)

# Carregar dados
try:
    cotton_data = load_cotton_data("data/raw/AlgodoSerieHist.xlsx")
    weather_data = load_weather_data("data/raw/weather_sum_all.csv")
except Exception as e:
    st.error(f"Erro ao carregar os dados: {e}")
    st.stop()

# Sidebar para explorar dados
st.sidebar.title("Exploração dos Dados")
if st.sidebar.checkbox("Exibir dados brutos de algodão"):
    st.subheader("Dados Brutos de Algodão")
    st.write(cotton_data.head(20))
    st.markdown(
        """
        **Descrição:**
        - `Região/UF`: Região ou estado.
        - `Ano`: Ano de registro.
        - `Area_Plantada`: Área plantada em hectares.
        """
    )
if st.sidebar.checkbox("Exibir dados brutos meteorológicos"):
    st.subheader("Dados Brutos Meteorológicos")
    st.write(weather_data.head(20))
    st.markdown(
        """
        **Descrição:**
        - `temp_avg`: Temperatura média diária (°C).
        - `rain_max`: Precipitação máxima (mm).
        - `rad_max`: Radiação máxima (kJ/m²).
        """
    )

# Tabs para explorar análises
tabs = st.tabs(["Tendências Sazonais", "Melhores Regiões", "Influência Climática", "Tendências Históricas", "Relações Entre Variáveis", "Experiências", "Conclusões"])

# 1. Tendências Sazonais
with tabs[0]:
    st.header("Tendências Sazonais")
    st.markdown("Analisamos as tendências sazonais das temperaturas médias ao longo dos anos.")
    try:
        seasonal_trends = analyze_seasonal_trends(cotton_data, weather_data)
        st.subheader("Gráfico de Tendências Sazonais")
        plot_seasonal_trends(seasonal_trends)
        st.subheader("Tabela de Tendências Sazonais")
        st.write(seasonal_trends.head(10))
    except Exception as e:
        st.error(f"Erro ao analisar tendências sazonais: {e}")

# 2. Melhores Regiões
with tabs[1]:
    st.header("Melhores Regiões para Plantio")
    st.markdown("Identificamos as regiões com maior potencial para o plantio de algodão.")
    try:
        regional_potential = analyze_regional_potential(cotton_data, weather_data)
        st.subheader("Mapa de Melhores Regiões")
        plot_regional_map(regional_potential)
        st.subheader("Tabela de Regiões")
        st.write(regional_potential)
    except Exception as e:
        st.error(f"Erro ao analisar potencial regional: {e}")

# 3. Influência Climática
with tabs[2]:
    st.header("Influência Climática")
    st.markdown("Avaliamos o impacto de variáveis climáticas na área plantada de algodão.")
    try:
        climatic_influences = analyze_climatic_influences(cotton_data, weather_data)
        st.subheader("Gráfico de Influência Climática")
        plot_climatic_influence(climatic_influences)
        st.subheader("Tabela de Correlações Climáticas")
        st.write(climatic_influences)
    except Exception as e:
        st.error(f"Erro ao analisar influências climáticas: {e}")

# 4. Tendências Históricas
with tabs[3]:
    st.header("Tendências Históricas")
    st.markdown("Analisamos as mudanças na área plantada ao longo do tempo.")
    try:
        historical_trends = analyze_historical_trends(cotton_data)
        st.subheader("Gráfico de Tendências Históricas")
        plot_historical_trends(historical_trends)
        st.subheader("Tabela de Tendências Históricas")
        st.write(historical_trends.head(10))
    except Exception as e:
        st.error(f"Erro ao analisar tendências históricas: {e}")

# 5. Relações Entre Variáveis
with tabs[4]:
    st.header("Relações Entre Variáveis")
    st.markdown("Exploramos correlações entre variáveis climáticas e a área plantada.")
    try:
        st.subheader("Mapa de Calor de Correlação")
        plot_correlation_heatmap(cotton_data, weather_data)
    except Exception as e:
        st.error(f"Erro ao analisar relações entre variáveis: {e}")

# 6. Experiências
with tabs[5]:
    st.header("Experiências Interativas")
    st.markdown("Experimente interagir com os dados e gráficos para obter insights personalizados.")
    if st.checkbox("Exibir Scatterplot Interativo"):
        st.subheader("Dispersão: Temperatura Média vs Área Plantada")
        try:
            plot_scatter(cotton_data, weather_data)
        except Exception as e:
            st.error(f"Erro ao gerar scatterplot: {e}")

    if st.checkbox("Comparar áreas plantadas por região"):
        st.subheader("Comparação de Áreas Plantadas")
        region_comparison = cotton_data.groupby("Região/UF")["Area_Plantada"].mean().sort_values(ascending=False)
        st.bar_chart(region_comparison)

# 7. Conclusões
with tabs[6]:
    st.header("Conclusões")
    st.markdown(
        """
        ### Insights Gerais
        - **Melhores períodos:** A análise sazonal destaca os períodos com temperaturas amenas e chuvas moderadas como os ideais para o plantio.
        - **Regiões promissoras:** A região Centro-Oeste e Nordeste apresentam maior potencial devido à estabilidade climática e histórico de alta produtividade.
        - **Impactos climáticos:** A temperatura média e a radiação solar têm as correlações mais fortes com a área plantada.
        - **Tendências históricas:** Observa-se um crescimento na área plantada desde 2010, com tendências de expansão para novas regiões.
        """
    )

# Exportação de dados
if st.sidebar.button("Exportar Conclusões"):
    st.sidebar.write("Função de exportação de relatório ainda em desenvolvimento.")
