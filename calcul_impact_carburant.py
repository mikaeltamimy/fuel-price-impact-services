"""
Impact de la hausse des carburants 2026 sur le tertiaire marchand en France.

Calcule, pour chaque groupe de branches du tertiaire marchand :
  1. le poids des produits pétroliers dans les coûts de production,
  2. la perte de taux de marge (EBE / VA) si la hausse n'est pas répercutée,
  3. la part de l'excédent brut d'exploitation (EBE) absorbée par le surcoût,
  4. le surcoût annuel en euros (ordre de grandeur, volumes constants).

Hypothèse centrale : aucune répercussion sur les prix de vente, volumes inchangés.
Les résultats sont donc une borne haute du choc direct à court terme.

Usage : python calcul_impact_carburant.py
Entrées : data/eurostat_naio_10_cp16_FR_2019.csv, data/prix_carburants_insee_mensuels.csv
Sortie  : resultats/resultats_par_branche.csv
"""

from pathlib import Path

import pandas as pd

ICI = Path(__file__).parent

# --- Paramètres (sources dans le README) -------------------------------------
PRIX_GAZOLE_2019 = 1.44   # €/L, moyenne annuelle, INSEE série 010533883
PRIX_GAZOLE_2025 = 1.64   # €/L, moyenne annuelle, INSEE série 010533883
IPCH_2019 = 104.95        # indice des prix harmonisé, moyenne annuelle, Eurostat prc_hicp_aind
IPCH_2025 = 124.43
PRIX_GAZOLE_23_SEPT_2026 = 2.402  # €/L, moyenne nationale, prix-carburant.eu

# Facteur de passage de la structure 2019 aux prix relatifs de 2025 :
# le gazole a moins augmenté que les prix en général entre 2019 et 2025.
K = (PRIX_GAZOLE_2025 / PRIX_GAZOLE_2019) / (IPCH_2025 / IPCH_2019)


def scenarios(prix: pd.DataFrame) -> dict:
    """Hausse du prix du gazole par rapport à la moyenne 2025, pour chaque scénario."""
    crise = prix[(prix["mois"] >= "2026-03") & (prix["mois"] <= "2026-08")]
    prix_a = crise["gazole_eur_litre"].mean()
    return {
        "A": prix_a / PRIX_GAZOLE_2025 - 1,                  # moyenne mars-août 2026
        "B": PRIX_GAZOLE_23_SEPT_2026 / PRIX_GAZOLE_2025 - 1,  # niveau du 23 septembre 2026
    }


def indicateurs(carburant_2019, production, va, ebe, hausses) -> dict:
    """Les trois indicateurs pour une branche (ou un agrégat), montants en M€."""
    c = carburant_2019 * K            # achats de carburant, base 2025
    couts = production - ebe          # consommations intermédiaires + salaires + impôts sur la production
    marge = ebe / va
    res = {
        "carburant_2019_meur": carburant_2019,
        "valeur_ajoutee_meur": va,
        "ebe_meur": ebe,
        "taux_de_marge_avant": marge,
        "poids_couts_2025": c / couts,
    }
    for nom, g in hausses.items():
        surcout = c * g
        res[f"poids_couts_{nom}"] = c * (1 + g) / (couts + surcout)
        res[f"points_marge_perdus_{nom}"] = (marge - (ebe - surcout) / (va - surcout)) * 100 if ebe > 0 else None
        res[f"part_ebe_absorbee_{nom}"] = surcout / ebe if ebe > 0 else None
        # Ordre de grandeur en euros de 2025, à volumes 2019
        res[f"surcout_md_eur_{nom}"] = carburant_2019 * (PRIX_GAZOLE_2025 / PRIX_GAZOLE_2019) * g / 1000
    return res


def main() -> None:
    donnees = pd.read_csv(ICI / "data" / "eurostat_naio_10_cp16_FR_2019.csv")
    prix = pd.read_csv(ICI / "data" / "prix_carburants_insee_mensuels.csv", dtype={"mois": str})
    hausses = scenarios(prix)

    colonnes = ["achats_produits_petroliers_meur", "production_meur", "valeur_ajoutee_meur", "ebe_revenu_mixte_meur"]

    def calcul(df: pd.DataFrame, nom: str) -> dict:
        s = df[colonnes].sum()
        return {"groupe": nom, **indicateurs(*s.values, hausses)}

    lignes = [calcul(df, nom) for nom, df in donnees.groupby("groupe", sort=False)]
    lignes += [
        calcul(donnees, "TOTAL tertiaire marchand"),
        calcul(donnees[donnees["transport"] == "non"], "TOTAL hors transport"),
        calcul(donnees[donnees["transport"] == "oui"], "TOTAL transport et entreposage"),
    ]
    resultats = pd.DataFrame(lignes)

    sortie = ICI / "resultats" / "resultats_par_branche.csv"
    sortie.parent.mkdir(exist_ok=True)
    resultats.round(6).to_csv(sortie, index=False)

    print(f"Facteur k = {K:.4f} | hausse A = {hausses['A']:+.1%} | hausse B = {hausses['B']:+.1%}\n")
    vue = resultats.set_index("groupe")[
        ["poids_couts_2025", "poids_couts_B", "points_marge_perdus_B", "part_ebe_absorbee_B", "surcout_md_eur_B"]
    ]
    options = {"display.float_format": "{:.4f}".format, "display.width": 160,
               "display.max_columns": None, "display.max_colwidth": 38}
    with pd.option_context(*[x for kv in options.items() for x in kv]):
        print(vue.sort_values("part_ebe_absorbee_B", ascending=False))
    print(f"\nRésultats écrits dans {sortie.relative_to(ICI)}")


if __name__ == "__main__":
    main()
