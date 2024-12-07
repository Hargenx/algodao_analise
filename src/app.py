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
    plot_correlation_heatmap,
)
from provenance import generate_provenance, save_provenance

# Configuração inicial da página
st.set_page_config(page_title="Análise de Algodão no Brasil", layout="wide")

# Título e introdução
st.title("Análise de Dados de Plantio e Colheita de Algodão no Brasil")
st.markdown(
    """
    Este painel interativo oferece insights sobre dados históricos de algodão e condições climáticas no Brasil. 
    Descubra os melhores períodos para plantio, regiões promissoras, tendências históricas e muito mais.
    """
)

# Carregar dados
st.sidebar.header("Carregar Dados")
try:
    cotton_data_path = st.sidebar.text_input(
        "Caminho para o dataset de algodão:", "../data/raw/AlgodoSerieHist.xlsx"
    )
    weather_data_path = st.sidebar.text_input(
        "Caminho para o dataset meteorológico:", "../data/raw/weather_sum_all.csv"
    )

    cotton_data = load_cotton_data(cotton_data_path)
    weather_data = load_weather_data(weather_data_path)

    st.sidebar.success("Dados carregados com sucesso!")
except Exception as e:
    st.sidebar.error(f"Erro ao carregar dados: {e}")
    st.stop()

# Sidebar para exibir dados brutos
if st.sidebar.checkbox("Exibir dados brutos de algodão"):
    st.subheader("Dados Brutos de Algodão")
    st.write(cotton_data.head(20))

if st.sidebar.checkbox("Exibir dados meteorológicos brutos"):
    st.subheader("Dados Brutos Meteorológicos")
    st.write(weather_data.head(20))

# Tabs principais
tabs = st.tabs(
    [
        "Tendências Sazonais",
        "Melhores Regiões",
        "Influência Climática",
        "Tendências Históricas",
        "Correlação de Variáveis",
        "Proveniência",
        "Conclusões",
    ]
)

# Aba: Tendências Sazonais
with tabs[0]:
    st.header("Tendências Sazonais")
    try:
        seasonal_trends = analyze_seasonal_trends(cotton_data, weather_data)
        st.subheader("Gráfico")
        plot_seasonal_trends(seasonal_trends)
        st.subheader("Dados de Tendências Sazonais")
        st.write(seasonal_trends)
    except Exception as e:
        st.error(f"Erro ao analisar tendências sazonais: {e}")

# Aba: Melhores Regiões
with tabs[1]:
    st.header("Melhores Regiões para Plantio")
    try:
        regional_potential = analyze_regional_potential(cotton_data, weather_data)
        st.subheader("Mapa")
        plot_regional_map(regional_potential)
        st.subheader("Detalhes por Região")
        st.write(regional_potential)
    except Exception as e:
        st.error(f"Erro ao analisar regiões: {e}")

# Aba: Influência Climática
with tabs[2]:
    st.header("Influência Climática")
    try:
        climatic_influences = analyze_climatic_influences(cotton_data, weather_data)
        st.subheader("Gráfico")
        plot_climatic_influence(climatic_influences)
        st.subheader("Detalhes da Influência Climática")
        st.write(climatic_influences)
    except Exception as e:
        st.error(f"Erro ao analisar influências climáticas: {e}")

# Aba: Tendências Históricas
with tabs[3]:
    st.header("Tendências Históricas")
    try:
        historical_trends = analyze_historical_trends(cotton_data)
        st.subheader("Gráfico de Tendências Históricas")
        plot_historical_trends(historical_trends)
        st.subheader("Dados Históricos")
        st.write(historical_trends)
    except Exception as e:
        st.error(f"Erro ao analisar tendências históricas: {e}")

# Aba: Correlação de Variáveis
with tabs[4]:
    st.header("Mapa de Correlação")
    try:
        st.subheader("Mapa de Calor")
        plot_correlation_heatmap(cotton_data, weather_data)
    except Exception as e:
        st.error(f"Erro ao gerar mapa de correlação: {e}")

# Aba: Proveniência
with tabs[5]:
    st.header("Proveniência do Projeto")
    try:
        prov_doc = generate_provenance()
        prov_json = prov_doc.serialize(indent=2)

        st.subheader("Proveniência JSON")
        st.json(prov_json)

        st.download_button(
            label="Baixar Proveniência (JSON)",
            data=prov_json,
            file_name="provenance.json",
            mime="application/json",
        )
        save_provenance(prov_doc, "outputs/provenance.json")
    except Exception as e:
        st.error(f"Erro ao gerar proveniência: {e}")

# Aba: Conclusões
with tabs[6]:
    st.header("Conclusões e Insights")
    st.markdown(
        """
        - **Melhores períodos para plantio:** Primavera e verão destacam-se devido às condições favoráveis.
        - **Regiões com maior potencial:** Nordeste e Centro-Oeste lideram devido à combinação de fatores climáticos e estruturais.
        - **Impactos climáticos mais significativos:** Temperatura média e precipitação apresentam as maiores correlações com o rendimento.
        """
    )
