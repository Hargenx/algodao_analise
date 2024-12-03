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

# 1. Análise de Tendências Sazonais
st.header("1. Melhores Períodos para Plantio")
try:
    seasonal_trends = analyze_seasonal_trends(cotton_data, weather_data)
    plot_seasonal_trends(seasonal_trends)
except Exception as e:
    st.error(f"Erro ao analisar tendências sazonais: {e}")

# 2. Potencial Regional
st.header("2. Melhores Regiões para Plantio")
try:
    regional_potential = analyze_regional_potential(cotton_data, weather_data)
    plot_regional_map(regional_potential)
except Exception as e:
    st.error(f"Erro ao analisar potencial regional: {e}")

# 3. Influência Climática
st.header("3. Condições Climáticas que Influenciam o Plantio")
try:
    climatic_influences = analyze_climatic_influences(cotton_data, weather_data)
    plot_climatic_influence(climatic_influences)
except Exception as e:
    st.error(f"Erro ao analisar influências climáticas: {e}")

# 4. Tendências Históricas
st.header("4. Tendências Históricas de Plantio")
try:
    historical_trends = analyze_historical_trends(cotton_data)
    plot_historical_trends(historical_trends)
except Exception as e:
    st.error(f"Erro ao analisar tendências históricas: {e}")

# 5. Relações Entre Variáveis
st.header("5. Relação entre Variáveis")
try:
    #plot_scatter(cotton_data, weather_data)
    plot_correlation_heatmap(cotton_data, weather_data)
except Exception as e:
    st.error(f"Erro ao analisar relações entre variáveis: {e}")

# Conclusões
st.markdown("### Conclusões")
try:
    # Gerar conclusões dinâmicas (ajuste conforme necessário)
    st.markdown(
        """
        - **Melhores períodos:** A análise sazonal destaca os períodos com temperaturas amenas e chuvas moderadas como os ideais para o plantio.
        - **Regiões promissoras:** A região Centro-Oeste e Nordeste apresentam maior potencial devido à estabilidade climática e histórico de alta produtividade.
        - **Impactos climáticos:** A temperatura média e a radiação solar têm as correlações mais fortes com a área plantada.
        - **Tendências históricas:** Observa-se um crescimento na área plantada desde 2010, com tendências de expansão para novas regiões.
        """
    )
except Exception as e:
    st.error(f"Erro ao gerar as conclusões: {e}")
