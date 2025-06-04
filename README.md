# Plasma Metabolomic Profiling in Patients with Rheumatoid Arthritis  
**Identifies Biochemical Features Indicative of Quantitative Disease Activity**

**DOI**: [https://doi.org/10.1186/s13075-021-02537-4](https://doi.org/10.1186/s13075-021-02537-4)  
**Authors**: Benjamin Hur, Vinod K. Gupta, Harvey Huang, Kerry A. Wright, Kenneth J. Warrington, Veena Taneja, John M. Davis III, and Jaeyun Sung  
**Contact**: hur.benjamin@mayo.edu  
**Corresponding Author**: sung.jaeyun@mayo.edu  

---

## 🧪 1. Differentially Abundant Metabolites

- Script:  
  `src/linear_model_r1/MLR_R_categorical_diff_2class_public.r`

- Wrapper shell script:  
  `analysis/differential_abundance_public/2class/run.sh`

---

## 🔍 2. Feature Selection for Quantitative Disease Activity in RA

- Python pipeline for LOO-CV feature selection:  
  `src/machine_learning_public/All_IN_ONE_FeatureSelection_CV_LOO.py`

- Shell wrapper:  
  `analysis/selection_scheme_public/run.sh`

---

## 📊 3. Additional Statistical Analyses

- **Drug effect modeling**  
  Investigates csDMARD, TNFi-bDMARD, non-TNFi-bDMARD, MTX, and PRED effects on metabolite abundance:  
  `src/statistics/drug_effect_lmer_R.ipynb`

- **Confounding analysis**  
  Tests if confounders (drug, smoking, age, etc.) differ between high and low disease activity groups:  
  `src/statistics/ftest_comfounds.ipynb`

- **McNemar test**  
  Analyzes prescription differences between visit 1 and visit 2:  
  `code/statistics/mcnemar_test_R.ipynb`

---

## 📁 Data

- **Training Dataset (n=128)**  
  `data/discovery_cohort/`

- **Test Dataset (n=12)**  
  `data/validation_cohort/`

---

## 🔗 Citation

If you use this repository, please cite:  
**Hur et al.,** *Arthritis Research & Therapy*, 2021. DOI: [10.1186/s13075-021-02537-4](https://doi.org/10.1186/s13075-021-02537-4)
