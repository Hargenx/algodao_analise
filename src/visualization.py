import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import geopandas as gpd
import streamlit as st
import plotly.express as px


@st.cache_data
def prepare_combined_data(cotton_data, weather_data):
    """
    Prepara os dados combinados para análise (merge de algodão e clima).
    """
    # Renomear colunas
    cotton_data.rename(columns={"Area_Plantada": "Area_Planted"}, inplace=True)

    # Filtrar dados por anos em comum
    common_years = set(cotton_data["Ano"]).intersection(weather_data["Ano"])
    cotton_filtered = cotton_data[cotton_data["Ano"].isin(common_years)]
    weather_filtered = weather_data[weather_data["Ano"].isin(common_years)]

    # Fazer o merge dos dados
    combined_data = pd.merge(cotton_filtered, weather_filtered, on="Ano")
    return combined_data


def plot_seasonal_trends(seasonal_data: pd.DataFrame):
    """
    Plota tendências sazonais.
    """
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=seasonal_data, x="Ano", y="temp_avg", hue="Estacao")
    plt.title("Tendências Sazonais de Temperatura Média")
    plt.xlabel("Ano")
    plt.ylabel("Temperatura Média (°C)")
    st.pyplot(plt)


def plot_regional_map(regional_data: pd.DataFrame):
    """
    Plota o mapa das melhores regiões para plantio de algodão, focado no Brasil.
    """
    try:
        # Caminho do arquivo shapefile do Natural Earth
        shapefile_path = "../data/geo/ne_10m_admin_0_countries.shp"

        # Carregar dados geográficos
        world = gpd.read_file(shapefile_path)

        # Adicionar as coordenadas às regiões
        regional_data = add_coordinates_to_regions(regional_data)

        # Verificar se as colunas necessárias existem
        if "lon" not in regional_data.columns or "lat" not in regional_data.columns:
            raise ValueError("Faltando colunas 'lon' ou 'lat' no DataFrame.")

        # Converter para GeoDataFrame
        gdf = gpd.GeoDataFrame(
            regional_data,
            geometry=gpd.points_from_xy(regional_data["lon"], regional_data["lat"]),
            crs="EPSG:4326",
        )

        # Criar o mapa
        fig, ax = plt.subplots(figsize=(12, 8))

        # Filtrar o shapefile para mostrar apenas o Brasil
        brazil = world[world["NAME"] == "Brazil"]

        # Plotar os limites do Brasil
        brazil.boundary.plot(ax=ax, linewidth=1, color="black")

        # Plotar os pontos no Brasil
        gdf.plot(
            ax=ax,
            color="red",
            markersize=regional_data["Area_Plantada"] / 100,  # Ajuste do tamanho
            alpha=0.7,
        )

        # Adicionar rótulos
        for x, y, label in zip(gdf.geometry.x, gdf.geometry.y, gdf["Região/UF"]):
            ax.text(x, y, label, fontsize=8, ha="right")

        # Ajustar os limites do mapa para focar no Brasil
        ax.set_xlim([-75, -32])  # Longitudes do Brasil
        ax.set_ylim([-35, 5])   # Latitudes do Brasil

        plt.title("Melhores Regiões para o Plantio de Algodão (Foco no Brasil)", fontsize=16)
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.grid(True)
        st.pyplot(fig)  # Usar Streamlit para exibir o gráfico

    except Exception as e:
        st.error(f"Erro ao plotar o mapa regional: {e}")




def add_coordinates_to_regions(regional_data):
    """
    Adiciona coordenadas de longitude e latitude às regiões no DataFrame.
    """
    # Exemplo de mapeamento de regiões para coordenadas
    coordinates = {
        "NORDESTE": {"lon": -38.0, "lat": -7.0},
        "CENTRO-SUL": {"lon": -47.0, "lat": -21.0},
        "CENTRO-OESTE": {"lon": -56.0, "lat": -16.0},
        "MT": {"lon": -55.0, "lat": -12.0},
        "CE": {"lon": -39.0, "lat": -5.0},
        "BA": {"lon": -41.0, "lat": -12.0},
        "SUDESTE": {"lon": -44.0, "lat": -22.0},
        "PR": {"lon": -51.0, "lat": -24.0},
        "SUL": {"lon": -49.0, "lat": -27.0},
        "PB": {"lon": -36.5, "lat": -7.2},
        "SP": {"lon": -46.6, "lat": -23.5},
        "RN": {"lon": -36.5, "lat": -5.8},
        "PI": {"lon": -42.8, "lat": -6.6},
        "MG": {"lon": -44.0, "lat": -18.0},
        "GO": {"lon": -49.0, "lat": -15.9},
        "PE": {"lon": -37.0, "lat": -8.0},
        "MS": {"lon": -54.0, "lat": -20.4},
        "AL": {"lon": -36.8, "lat": -9.6},
        "MA": {"lon": -44.2, "lat": -5.4},
        "NORTE": {"lon": -60.0, "lat": -3.0},
        "SE": {"lon": -37.0, "lat": -10.6},
        "RO": {"lon": -62.0, "lat": -11.2},
        "PA": {"lon": -52.0, "lat": -1.4},
        "TO": {"lon": -48.0, "lat": -10.2},
        "DF": {"lon": -47.9, "lat": -15.8},
        "RR": {"lon": -61.4, "lat": 2.8},
        "RJ": {"lon": -43.2, "lat": -22.9},
        "RS": {"lon": -51.2, "lat": -30.0},
        "SC": {"lon": -49.0, "lat": -27.6},
        "ES": {"lon": -40.3, "lat": -19.2},
        "AP": {"lon": -51.0, "lat": 0.0},
        "AM": {"lon": -62.0, "lat": -3.0},
        "AC": {"lon": -70.0, "lat": -9.5},
    }

    # Adicionar colunas de longitude e latitude
    regional_data["lon"] = regional_data["Região/UF"].map(
        lambda x: coordinates.get(x, {}).get("lon")
    )
    regional_data["lat"] = regional_data["Região/UF"].map(
        lambda x: coordinates.get(x, {}).get("lat")
    )

    # Verificar se há valores ausentes
    missing = regional_data[
        regional_data["lon"].isnull() | regional_data["lat"].isnull()
    ]
    if not missing.empty:
        print(f"Coordenadas ausentes para: {missing['Região/UF'].tolist()}")
        raise ValueError("Adicione coordenadas para todas as regiões.")

    return regional_data


def plot_correlation_heatmap(cotton_data, weather_data):
    """
    Plota um mapa de calor da correlação entre as variáveis numéricas dos dados combinados.
    """
    import seaborn as sns
    import matplotlib.pyplot as plt

    try:
        # Combinar os dados
        combined_data = cotton_data.merge(
            weather_data, on=["Ano", "Região/UF"], how="inner"
        )

        # Selecionar apenas colunas numéricas
        numeric_data = combined_data.select_dtypes(include=["float64", "int64"])

        # Calcular a matriz de correlação
        corr_matrix = numeric_data.corr()

        # Plotar o mapa de calor
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar=True)
        plt.title("Mapa de Calor de Correlação")
        st.pyplot(plt)  # Usar st.pyplot para integrar com o Streamlit
    except Exception as e:
        st.error(f"Erro ao gerar mapa de calor: {e}")


def plot_climatic_influence(correlations: pd.Series):
    """
    Plota as variáveis climáticas mais influentes.
    """
    plt.figure(figsize=(8, 5))
    sns.barplot(x=correlations.values, y=correlations.index)
    plt.title("Influência de Variáveis Climáticas na Área Plantada")
    plt.xlabel("Correlação")
    st.pyplot(plt)


def plot_historical_trends(historical_trends: pd.DataFrame):
    """
    Plota as tendências históricas na área plantada.
    """
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=historical_trends, x="Ano", y="Area_Planted")
    plt.title("Tendências Históricas da Área Plantada")
    plt.xlabel("Ano")
    plt.ylabel("Área Plantada (ha)")
    st.pyplot(plt)


def plot_scatter(cotton_data: pd.DataFrame, weather_data: pd.DataFrame):
    """
    Plota scatterplot das variáveis: temperatura média vs área plantada.
    """
    # Renomear colunas, se necessário
    cotton_data.rename(columns={"Area_Plantada": "Area_Planted"}, inplace=True)

    # Verificar colunas nos datasets
    required_cols = {"Ano", "Area_Planted"}
    if not required_cols.issubset(cotton_data.columns):
        raise ValueError(
            f"Faltando colunas no dataset de algodão: {required_cols - set(cotton_data.columns)}"
        )

    weather_cols = {"Ano", "temp_avg", "rain_max"}
    if not weather_cols.issubset(weather_data.columns):
        raise ValueError(
            f"Faltando colunas no dataset meteorológico: {weather_cols - set(weather_data.columns)}"
        )

    # Filtrar dados por anos em comum
    common_years = set(cotton_data["Ano"]).intersection(weather_data["Ano"])
    cotton_filtered = cotton_data[cotton_data["Ano"].isin(common_years)]
    weather_filtered = weather_data[weather_data["Ano"].isin(common_years)]

    # Fazer o merge dos dados
    combined_data = pd.merge(cotton_filtered, weather_filtered, on="Ano")

    # Amostrar dados para melhorar desempenho (exemplo: 20%)
    if len(combined_data) > 10000:
        combined_data = combined_data.sample(frac=0.2, random_state=42)

    # Gerar scatterplot
    plt.figure(figsize=(8, 5))
    plt.scatter(combined_data["temp_avg"], combined_data["Area_Planted"], alpha=0.7)
    plt.title("Dispersão: Temperatura Média vs Área Plantada")
    plt.xlabel("Temperatura Média (°C)")
    plt.ylabel("Área Plantada (ha)")
    plt.grid(True)
    st.pyplot(plt)


def plot_interactive_scatter(data):
    """
    Gera um gráfico interativo usando Plotly.
    """
    fig = px.scatter(
        data,
        x="temp_avg",
        y="Area_Plantada",
        title="Dispersão: Temperatura Média vs Área Plantada",
        labels={"temp_avg": "Temperatura Média", "Area_Plantada": "Área Plantada"},
    )
    fig.update_traces(marker=dict(size=5, opacity=0.7))

    fig.show()
