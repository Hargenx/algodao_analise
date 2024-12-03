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
cotton_data = load_cotton_data("data/raw/AlgodoSerieHist.xlsx")
weather_data = load_weather_data("data/raw/weather_sum_all.csv")

# 1. Análise de Tendências Sazonais
st.header("1. Melhores Períodos para Plantio")
seasonal_trends = analyze_seasonal_trends(cotton_data, weather_data)
plot_seasonal_trends(seasonal_trends)

# Exibir os gráficos e resultados
st.title("Análise de Dados: Plantio e Colheita de Algodão")
st.write(
    "Este painel analisa os melhores períodos e regiões para o plantio de algodão."
)

# Gráfico 1: Tendências Sazonais
st.subheader("Tendências Sazonais")
st.line_chart(seasonal_trends.set_index("Ano")[["Area_Plantada", "temp_avg"]])

# 2. Potencial Regional
st.header("2. Melhores Regiões para Plantio")
regional_potential = analyze_regional_potential(cotton_data, weather_data)
plot_regional_map(regional_potential)

# 3. Influência Climática
st.header("3. Condições Climáticas que Influenciam o Plantio")
climatic_influences = analyze_climatic_influences(cotton_data, weather_data)
plot_climatic_influence(climatic_influences)

# 4. Tendências Históricas
st.header("4. Tendências Históricas de Plantio")
historical_trends = analyze_historical_trends(cotton_data)
plot_historical_trends(historical_trends)

# 5. Relações Entre Variáveis
st.header("5. Relação entre Variáveis")
plot_scatter(cotton_data, weather_data)
plot_correlation_heatmap(cotton_data, weather_data)

# Conclusões
st.markdown(
    """
### Conclusões
- **Melhores períodos:** A análise sazonal destaca o período X-Y como ideal para o plantio devido às condições climáticas favoráveis.
- **Regiões promissoras:** A região Z apresenta maior potencial devido à estabilidade climática e histórico de alta produtividade.
- **Impactos climáticos:** A radiação solar e a temperatura média têm as correlações mais fortes com a área plantada.
- **Tendências históricas:** Há um crescimento/declínio consistente de X% na área plantada ao longo dos últimos anos.
"""
)
