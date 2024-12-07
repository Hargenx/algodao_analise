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
from provenance import generate_provenance, save_provenance

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
    cotton_data = load_cotton_data("../data/raw/AlgodoSerieHist.xlsx")
    weather_data = load_weather_data("../data/raw/weather_sum_all.csv")
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
tabs = st.tabs(
    [
        "Tendências Sazonais",
        "Melhores Regiões",
        "Influência Climática",
        "Tendências Históricas",
        "Relações Entre Variáveis",
        "Experiências",
        "Proveniência",
        "Conclusões",
    ]
)

# 1. Tendências Sazonais
with tabs[0]:
    st.header("Tendências Sazonais")
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
    try:
        st.subheader("Mapa de Calor de Correlação")
        plot_correlation_heatmap(cotton_data, weather_data)
    except Exception as e:
        st.error(f"Erro ao analisar relações entre variáveis: {e}")

# 6. Experiências
with tabs[5]:
    st.header("Experiências Interativas")
    if st.checkbox("Exibir Scatterplot Interativo"):
        try:
            plot_scatter(cotton_data, weather_data)
        except Exception as e:
            st.error(f"Erro ao gerar scatterplot: {e}")

    if st.checkbox("Comparar áreas plantadas por região"):
        region_comparison = (
            cotton_data.groupby("Região/UF")["Area_Plantada"]
            .mean()
            .sort_values(ascending=False)
        )
        st.bar_chart(region_comparison)

# 7. Proveniência
# Geração de Proveniência
prov_doc = generate_provenance()

# Aba de Proveniência
with tabs[6]:  # Aba "Proveniência"
    st.header("Proveniência do Projeto")
    prov_json = prov_doc.serialize(indent=2)
    st.subheader("Tabela de Proveniência")
    st.json(prov_json)

    # Botão para Download
    st.download_button(
        label="Baixar Proveniência JSON",
        data=prov_json,
        file_name="provenance.json",
        mime="application/json",
    )

    # Salvar Proveniência
    save_provenance(prov_doc, "outputs/provenance.json")


# 8. Conclusões
with tabs[7]:
    st.header("Conclusões")
    st.markdown(
        """
        ### Insights Gerais
        - **Melhores períodos:** Primavera e verão se destacam como os melhores períodos para plantio.
        - **Regiões promissoras:** Nordeste e Centro-Oeste apresentam maior potencial.
        - **Impactos climáticos:** A radiação solar e a temperatura média são os fatores mais influentes.
        """
    )
