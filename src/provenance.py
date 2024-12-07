from prov.model import ProvDocument, PROV
import os


def generate_provenance():
    """
    Gera um documento de proveniência para o pipeline do projeto.
    """
    prov_doc = ProvDocument()

    prov_doc.add_namespace("ex", "http://example.org/")

    # Agente
    developer = prov_doc.agent(
        "ex:developer",
        {
            PROV["type"]: PROV["Person"],
            "prov:label": "Desenvolvedor do Projeto",
            "prov:name": "Raphael",
            "prov:email": "raphael.mauricio@gmail.com",
        },
    )

    # Entidades
    cotton_data_entity = prov_doc.entity(
        "ex:cotton_data",
        {
            PROV["type"]: "Dataset",
            "prov:label": "Dados do Algodão",
            "prov:location": "data/raw/AlgodoSerieHist.xlsx",
        },
    )
    weather_data_entity = prov_doc.entity(
        "ex:weather_data",
        {
            PROV["type"]: "Dataset",
            "prov:label": "Dados Meteorológicos",
            "prov:location": "data/raw/weather_sum_all.csv",
        },
    )

    # Atividades
    load_data_activity = prov_doc.activity(
        "ex:load_data",
        startTime="2024-11-25T10:00:00",
        endTime="2024-12-05T10:05:00",
    )
    seasonal_analysis_activity = prov_doc.activity(
        "ex:seasonal_analysis",
        startTime="2024-11-30T10:10:00",
        endTime="2024-12-05T10:20:00",
    )

    # Relacionamentos: Agente e Atividades
    prov_doc.wasAssociatedWith(load_data_activity, developer)
    prov_doc.wasAssociatedWith(seasonal_analysis_activity, developer)

    # Relacionamentos: Atividades e Entidades
    prov_doc.used(load_data_activity, cotton_data_entity)
    prov_doc.used(load_data_activity, weather_data_entity)
    prov_doc.used(seasonal_analysis_activity, cotton_data_entity)
    prov_doc.used(seasonal_analysis_activity, weather_data_entity)

    # Resultados gerados
    seasonal_results = prov_doc.entity(
        "ex:seasonal_results",
        {"prov:label": "Resultados de Tendências Sazonais"},
    )
    prov_doc.wasGeneratedBy(seasonal_results, seasonal_analysis_activity)

    return prov_doc


def save_provenance(prov_doc: ProvDocument, filename="outputs/provenance.json"):
    """
    Salva o documento de proveniência no formato JSON, garantindo que o diretório exista.
    """
    # Resolver o caminho absoluto com base no diretório atual do script
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Diretório do script atual
    full_path = os.path.join(base_dir, filename)

    # Garantir que o diretório de saída exista
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    # Salvar o arquivo
    with open(full_path, "w") as file:
        file.write(prov_doc.serialize(indent=2))


# Exemplo de uso
if __name__ == "__main__":
    prov_doc = generate_provenance()
    save_provenance(prov_doc, filename="outputs/provenance.json")
    print("Documento de Proveniência Gerado e Salvo!")
