
import pandas as pd
import logging


def load_cotton_data(filepath: str) -> pd.DataFrame:
    """
    Carrega e processa os dados de algodão do arquivo Excel.
    """
    try:
        # Carregar o arquivo Excel
        data = pd.read_excel(filepath, engine="openpyxl", skiprows=4, header=None)

        # Exibir a estrutura inicial do dataframe para diagnóstico
        print("Estrutura inicial do dataset de algodão:")
        print(data.head())

        # Detectar automaticamente o número de colunas com dados
        col_count = len(data.columns)

        # Criar os nomes das colunas dinamicamente
        col_names = ["Região/UF"] + [
            str(year) for year in range(1976, 1976 + col_count - 1)
        ]
        data.columns = col_names[:col_count]  # Ajustar o número de colunas

        # Excluir totais gerais ou linhas de rodapé não relevantes
        data = data[~data["Região/UF"].str.contains("BRASIL|NORTE/NORDESTE", na=False)]

        # Transformar a tabela em formato longo (melt) para análise
        data_long = data.melt(
            id_vars=["Região/UF"], var_name="Ano", value_name="Area_Plantada"
        )

        # Remover valores nulos ou não numéricos
        data_long = data_long.dropna(subset=["Area_Plantada"])
        data_long["Area_Plantada"] = pd.to_numeric(
            data_long["Area_Plantada"], errors="coerce"
        )

        # Garantir que "Ano" seja tratado como um inteiro
        data_long["Ano"] = data_long["Ano"].astype(int)

        logging.info(
            f"Dados de algodão carregados: {data_long.shape[0]} linhas processadas."
        )
        print("Pré-visualização dos dados carregados:")
        print(data_long.head())

        return data_long
    except Exception as e:
        raise RuntimeError(f"Erro ao carregar dados de algodão: {e}")


def load_weather_data(filepath: str) -> pd.DataFrame:
    """
    Carrega e processa os dados climáticos.
    """
    try:
        # Carregar os dados
        data = pd.read_csv(filepath)

        # Converter a coluna DATA para datetime
        data["DATA"] = pd.to_datetime(data["DATA (YYYY-MM-DD)"], errors="coerce")
        data["Ano"] = data["DATA"].dt.year
        data["Mes"] = data["DATA"].dt.month

        # Definir estações do ano com base nos meses
        season_bins = [0, 2, 5, 8, 11, 12]  # Divisão em meses
        season_labels = ["Verão", "Outono", "Inverno", "Primavera", "Verão"]
        data["Estacao"] = pd.cut(
            data["Mes"],
            bins=season_bins,
            labels=season_labels,
            ordered=False,
            right=True,
        )

        # Verificar duplicatas ou problemas
        if data["Estacao"].isna().any():
            raise ValueError(
                "Erro ao mapear meses para estações: valores nulos detectados."
            )

        print("Pré-visualização dos dados meteorológicos:")
        print(data.head())

        return data
    except Exception as e:
        raise RuntimeError(f"Erro ao carregar dados meteorológicos: {e}")
