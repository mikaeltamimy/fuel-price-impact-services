# Hausse des carburants 2026 : quel impact sur le tertiaire ?

Estimation, branche par branche, de ce que coûte la hausse du gazole de 2026 aux entreprises du tertiaire marchand en France.

> **English summary.** Branch-level estimate of the 2026 diesel price shock on French market services, built from Eurostat supply-and-use tables and INSEE fuel prices. At the 23 September 2026 price (+46% vs. 2025), fuel absorbs about 3% of the gross operating surplus of market services if firms pass nothing on to customers. That rises to 21% in transport and warehousing, against 1.5% for all other services combined.

**Étude complète (PDF, 8 pages)** : [etude/etude_hausse_carburants_tertiaire.pdf](etude/etude_hausse_carburants_tertiaire.pdf). Elle contient le contexte des prix, la méthode, les trois indicateurs par branche, les enquêtes auprès des entreprises, les limites et les sources.

## Résultats

Le 23 septembre 2026, le gazole est à 2,40 €/L, soit +46 % par rapport à la moyenne 2025 (1,64 €/L). Si les entreprises ne répercutent rien sur leurs prix de vente :

| Périmètre | Poids du carburant dans les coûts (2025 → 23 sept.) | Points de taux de marge perdus | Part de l'EBE absorbée |
| --- | --- | --- | --- |
| Tertiaire marchand | 1,6 % → 2,3 % | −0,8 | 3,2 % |
| Transport et entreposage | 8,1 % → 11,4 % | −5,1 | 20,7 % |
| Tertiaire hors transport | 0,8 % → 1,1 % | −0,4 | 1,5 % |

![Poids du carburant dans les coûts, par branche](images/poids_carburant_par_branche.png)

Le surcoût atteint environ 15 Md€ par an, dont 8,5 Md€ pour le transport et l'entreposage. Le détail des 17 groupes de branches est dans `resultats/resultats_par_branche.csv` et dans l'onglet *Calculs* du classeur Excel.

## Méthode

1. **Structure de coûts par branche.** Le tableau des emplois de la comptabilité nationale donne, pour chaque branche, ses achats de produits pétroliers (C), sa production (P), sa valeur ajoutée (VA) et son excédent brut d'exploitation (EBE). L'année retenue est 2019, la dernière qui ne soit perturbée ni par le Covid ni par la crise énergétique de 2022.
2. **Passage à 2025.** Entre 2019 et 2025, le gazole a moins augmenté que les prix en général. Les achats de carburant sont donc multipliés par un facteur k = (1,64 / 1,44) ÷ (124,43 / 104,95) = 0,96.
3. **Scénarios de prix.** La hausse g est calculée par rapport à la moyenne 2025 :
   - A : moyenne de mars à août 2026, soit 2,11 €/L (+29 %) ;
   - B : prix du 23 septembre 2026, soit 2,40 €/L (+46 %).
4. **Indicateurs.** On note ΔC = C × g le surcoût.
   - Poids du carburant dans les coûts = C × (1 + g) ÷ (P − EBE + ΔC)
   - Perte de taux de marge = EBE ÷ VA − (EBE − ΔC) ÷ (VA − ΔC)
   - Part de l'EBE absorbée = ΔC ÷ EBE
5. **Périmètre.** Tertiaire marchand : commerce, transport, hébergement-restauration, information-communication, finance-assurance, immobilier (hors loyers imputés), services aux entreprises, arts-loisirs et services aux ménages. L'administration, l'enseignement, la santé et les associations sont exclus.

### Exemple : transports terrestres, scénario B

| Étape | Calcul | Résultat |
| --- | --- | --- |
| Carburant ajusté à 2025 | 7 838 M€ × 0,96 | 7 529 M€ |
| Coûts de production | 99 127 − 15 602 | 83 525 M€ |
| Poids du carburant en 2025 | 7 529 ÷ 83 525 | 9,0 % |
| Surcoût | 7 529 × 0,46 | 3 498 M€ |
| Poids après la hausse | 7 529 × 1,46 ÷ (83 525 + 3 498) | 12,7 % |
| Taux de marge | 33,2 % → 27,8 % | −5,4 points |
| Part de l'EBE absorbée | 3 498 ÷ 15 602 | 22,4 % |

## Limites

- **Borne haute.** Le calcul suppose aucune répercussion sur les prix et aucune adaptation (moins de kilomètres). Le transport routier de marchandises, par exemple, peut indexer ses prix sur le gazole.
- **Un seul prix pour tous les produits pétroliers.** La hausse du gazole sous-estime celle du kérosène et du fioul, qui sont peu taxés. Elle surestime le coût pour les entreprises qui font le plein dans une station au prix plafonné.
- **Structure de 2019.** Les flottes et les usages ont pu évoluer depuis.
- **Moyennes de branche.** Une PME de services itinérants est bien plus exposée que la moyenne de sa branche.
- **Effets indirects exclus** : hausse des prix des fournisseurs, baisse de la demande.
- **Transport par eau** : son EBE était négatif en 2019, les ratios de marge ne sont donc pas significatifs.

## Contenu du dépôt

```
├── calcul_impact_carburant.py          # calcul complet (Python + pandas)
├── impact_carburant_tertiaire.xlsx     # même calcul en formules Excel, paramètres modifiables
├── etude/
│   └── etude_hausse_carburants_tertiaire.pdf # l'étude complète
├── images/
│   └── poids_carburant_par_branche.png
├── data/
│   ├── eurostat_naio_10_cp16_FR_2019.csv     # données d'entrée par branche (M€)
│   └── prix_carburants_insee_mensuels.csv    # prix mensuels gazole et SP95-E10
└── resultats/
    └── resultats_par_branche.csv       # sortie du script
```

## Reproduire

```bash
pip install pandas
python calcul_impact_carburant.py
```

Dans le classeur Excel, les cellules bleues de l'onglet *Paramètres* peuvent être modifiées, par exemple le prix du scénario B. Tout se recalcule.

## Sources

- Eurostat, [naio_10_cp16](https://ec.europa.eu/eurostat/databrowser/view/naio_10_cp16/default/table) : tableau des emplois à prix d'acquisition, France, 2019 (produits CPA_C19, P1, B1G, B2A3G).
- Eurostat, [prc_hicp_aind](https://ec.europa.eu/eurostat/databrowser/view/prc_hicp_aind/default/table) : indice des prix à la consommation harmonisé, moyenne annuelle, France.
- INSEE, prix moyens de vente au détail en métropole : [gazole mensuel (000442588)](https://www.insee.fr/fr/statistiques/serie/000442588), [gazole annuel (010533883)](https://www.insee.fr/fr/statistiques/serie/010533883), [SP95-E10 mensuel (010596132)](https://www.insee.fr/fr/statistiques/serie/010596132).
- prix-carburant.eu, [prix moyens au 23 septembre 2026](https://prix-carburant.eu/article/prix-carburants-2026-09-23).
- Enquêtes citées dans l'analyse : [Bpifrance Le Lab, 83e baromètre TPE-PME](https://presse.bpifrance.fr/bpifrance-le-lab-presente-le-83eme-barometre-semestriel-des-tpe-pme-dans-un-paysage-morose-les-pme-industrielles-resistent/?lang=fra) (juillet 2026) ; [CPME](https://cpme17.fr/enquete-cpme-les-tpe-pme-sous-haute-tension-au-premier-semestre-2026/) (mai 2026).

---

Analyse : Mikael Tamimy, septembre 2026.
