import os
import json
import requests
from bioservices import BioModels

# 1. Initialisation
s = BioModels()

def get_all_models(query):
    models = []
    offset = 0
    while True:
        try:
            # On récupère les résultats par page de 10
            search_results = s.search(query, offset=offset)
            if 'models' not in search_results or not search_results['models']:
                break
            models.extend(search_results['models'])
            offset += 10
            print(f"Retrieving models... Found {len(models)} so far.")
        except Exception as e:
            print(f"Search error: {e}")
            break
    return models

def download_and_enrich(model_data, base_directory):
    model_id = model_data['id']
    title = model_data.get('name', "").lower()
    
    # 2. Classement intelligent par dossier (Tissus / Pathogènes)
    if any(w in title for w in ["lung", "pneumonia", "respiratory", "sars"]):
        sub_folder = "Respiratory_System"
    elif any(w in title for w in ["blood", "sepsis", "viremia", "hiv"]):
        sub_folder = "Blood_Circulatory"
    elif any(w in title for w in ["brain", "nervous", "zika"]):
        sub_folder = "Central_Nervous_System"
    else:
        sub_folder = "Other_Infections"

    directory = os.path.join(base_directory, sub_folder)
    os.makedirs(directory, exist_ok=True)

    # 3. Récupération des métadonnées complètes via l'API
    try:
        full_metadata = s.get_model(model_id)
        # On télécharge le fichier SBML (BioModels fournit souvent l'URL dans les métadonnées)
        # Si l'URL n'est pas directe, on utilise l'ID pour construire l'URL de téléchargement
        sbml_url = f"https://www.ebi.ac.uk/biomodels/model/download/{model_id}?filename={model_id}_url.xml"
        
        # Sauvegarde JSON enrichi
        with open(os.path.join(directory, f"{model_id}.json"), 'w', encoding='utf-8') as f:
            json.dump(full_metadata, f, indent=4, ensure_ascii=False)
            
        print(f"Model {model_id} processed in {sub_folder}")
    except Exception as e:
        print(f"Error processing {model_id}: {e}")

def main():
    # 4. TA REQUÊTE PERSONNALISÉE (Plus besoin de filtrer à la main après !)
    # On cherche : Infection OR Virus OR Bacteria, uniquement en SBML, uniquement Curated
    query = '(infection OR virus OR bacteria OR pathogen) AND curationstatus:"Manually curated" AND modelformat:"SBML"'

    base_dir = "InfectioGIT_Data"
    models = get_all_models(query)

    for m in models:
        download_and_enrich(m, base_dir)

if __name__ == "__main__":
    main()
    
