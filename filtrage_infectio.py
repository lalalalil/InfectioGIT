import os

# Configuration
source_dir = "AllBiomodels.xml"
output_file = "liste_modeles_infectieux.txt"

# Keywords
keywords = [
    # Pathogenic agents
    "virus", "bacteria", "pathogen", "fungi", "parasite", "prion",
    # Processus d'infection
    "infection", "immune response", "host-pathogen", "viral load", 
    "epidemic", "transmission", "vaccination", "antibiotic", "antiviral",
    # Major specific diseases
    "sars-cov-2", "covid-19", "hiv", "aids", "malaria", "tuberculosis", 
    "influenza", "flu", "ebola", "cholera", "zika", "dengue", "hepatitis",
    "pneumonia", "sepsis", "leishmaniasis", "trypanosoma"
]
print(f"Analyse des fichiers dans {source_dir}...")

infectious_count = 0

with open(output_file, "w") as out:
    for filename in os.listdir(source_dir):
        if filename.endswith(".xml"):
            path = os.path.join(source_dir, filename)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                    # Vérification si un mot-clé est présent
                    if any(word in content for word in keywords):
                        out.write(f"{filename}\n")
                        infectious_count += 1
            except:
                continue

print(f"Done! {infectious_count} infectious models detected.")
print(f"The list has been saved to: {output_file}")
