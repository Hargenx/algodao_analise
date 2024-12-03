import pandas as pd
import matplotlib.pyplot as plt


def analyze_seasonal_trends(
    cotton_data: pd.DataFrame, weather_data: pd.DataFrame
) -> pd.DataFrame:
    """
    Analisa tendências sazonais combinando dados de algodão e climáticos.
    """
    try:
        # Identificar colunas numéricas
        numeric_cols = weather_data.select_dtypes(include=[float, int]).columns.tolist()

        # Agrupar os dados climáticos por ano e estação, calculando a média
        seasonal_weather = weather_data.groupby(["Ano", "Estacao"], as_index=False)[
            numeric_cols
        ].mean()

        # Combinar dados de algodão com as tendências sazonais climáticas
        combined_data = pd.merge(cotton_data, seasonal_weather, on="Ano", how="inner")

        print("Pré-visualização dos dados sazonais combinados:")
        print(combined_data.head())

        return combined_data
    except Exception as e:
        raise RuntimeError(f"Erro ao analisar tendências sazonais: {e}")


def analyze_regional_potential(cotton_data, weather_data):
    """
    Analisa as melhores regiões para o plantio de algodão.
    """
    try:
        # Inspecionar e garantir que todas as colunas numéricas sejam numéricas
        numeric_cols = ["Area_Plantada"]  # Atualize conforme necessário
        for col in numeric_cols:
            cotton_data[col] = pd.to_numeric(cotton_data[col], errors="coerce")

        # Remover linhas com valores NaN nas colunas numéricas
        cotton_data = cotton_data.dropna(subset=numeric_cols)

        # Garantir que os dados estejam prontos para agrupamento
        print("Pré-visualização dos dados antes do agrupamento:")
        print(cotton_data.head())

        # Agrupar por região e calcular a média da área plantada
        regional_data = (
            cotton_data.groupby("Região/UF")[numeric_cols]
            .mean()
            .sort_values(by="Area_Plantada", ascending=False)
        )

        # Resetar o índice para facilitar a visualização
        regional_data = regional_data.reset_index()

        print("Pré-visualização das melhores regiões para plantio:")
        print(regional_data.head())

        return regional_data
    except Exception as e:
        raise RuntimeError(f"Erro ao analisar potencial regional: {e}")


def analyze_climatic_influences(cotton_data, weather_data):
    # Garantir que 'Região/UF' exista em ambos os datasets
    if "Região/UF" not in weather_data.columns:
        # Exemplo de mapeamento; ajuste conforme necessário
        station_to_region = {
            "A001": "NORTE",
            "A002": "NORDESTE",
            # Outros mapeamentos
        }
        weather_data["Região/UF"] = weather_data["ESTACAO"].map(station_to_region)

    # Certificar-se de que a coluna 'Ano' existe e está correta
    if "Ano" not in weather_data.columns:
        weather_data["Ano"] = pd.to_datetime(weather_data["DATA (YYYY-MM-DD)"]).dt.year

    # Realizar a mesclagem
    combined_data = cotton_data.merge(
        weather_data, on=["Ano", "Região/UF"], how="inner"
    )

    # Filtrar apenas colunas numéricas
    numeric_data = combined_data.select_dtypes(include=["float64", "int64"])

    # Calcular correlações
    correlations = numeric_data.corr()["Area_Plantada"].sort_values(ascending=False)

    return correlations


def analyze_historical_trends(cotton_data):
    # Garantir que o nome da coluna esteja correto
    if "Area_Planted" not in cotton_data.columns:
        cotton_data.rename(columns={"Area_Plantada": "Area_Planted"}, inplace=True)

    # Agrupar por ano e somar a área plantada
    historical_trends = cotton_data.groupby("Ano")["Area_Planted"].sum().reset_index()

    # Criar visualização
    plt.figure(figsize=(10, 6))
    plt.plot(historical_trends["Ano"], historical_trends["Area_Planted"], marker="o")
    plt.title("Tendências Históricas de Plantio de Algodão")
    plt.xlabel("Ano")
    plt.ylabel("Área Plantada (em mil hectares)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    return historical_trends
