# SOTA Scorecard: Mechanistic Interpretability

*Generated: 2026-01-13 18:00:05*

---

This scorecard synthesizes the provided benchmark and results data for mechanistic interpretability methods. It covers two key benchmarks: MIB and InterpBench, evaluating methods across circuit localization and causal variable localization tasks.

### 1. Benchmark Overview Table

| Benchmark Name | ArXiv ID | Description | Tasks | Key Metrics |
| :------------- | :------- | :---------- | :---- | :---------- |
| **MIB: A Mechanistic Interpretability Benchmark** | 2504.13151 | A benchmark for comparing mechanistic interpretability (MI) methods in neural language models. It features two tracks: circuit localization, which evaluates how well methods discover causal subgraphs (circuits), and causal variable localization, which assesses the alignment of high-level conceptual variables with low-level neural features. It provides standardized datasets, models, and metrics to evaluate method efficacy. | **Circuit Localization:** Indirect Object Identification (IOI), Arithmetic (addition and subtraction), Multiple-choice Question Answering (MCQA), AI2 Reasoning Challenge (ARC) (Easy and Challenge subsets)<br>**Causal Variable Localization:** IOI (disentangling subject token and position signals), Arithmetic (two-digit addition, localizing 'carry-the-one' variable), MCQA (localizing answer position and answer token), RA VEL (Resolving Attribute–Value Entanglements in Language Models) (disentangling country, continent, and language attributes of city entities), ARC (Easy) (localizing answer position and answer token) | **Circuit Localization:** Integrated Circuit Performance Ratio (CPR) (higher is better), Integrated Circuit-Model Distance (CMD) (closer to 0 is better), AUROC (on InterpBench-trained IOI model with known ground truth circuits), Weighted edge count (for circuit size)<br>**Causal Variable Localization:** Interchange Intervention Accuracy (IIA) (for MCQA, ARC, Arithmetic, RA VEL; higher is better), Mean-squared error (MSE) (for IOI; lower is better) |
| **InterpBench: Semi-Synthetic Transformers for Evaluating Mechanistic Interpretability Techniques** | 2407.14494 | A collection of 86 semi-synthetic, yet realistic, transformers with known ground-truth circuits. It employs Strict Interchange Intervention Training (SIIT) to create models that implement specific RASP programs or simplified versions of known circuits (like IOI), enabling rigorous and controlled evaluation of circuit discovery techniques. | 85 Tracr circuits (algorithmic tasks like word count, token classification, sequence reversal, Fibonacci numbers, etc.), Simplified Indirect Object Identification (IOI) circuit. | Area Under the Curve (AUC) of ROC curves for edge-level (for circuit discovery techniques), Node effect (percentage of times output changes when intervening on a node), Normalized KL divergence (for categorical tasks), Interchange Intervention Accuracy (IIA), Strict Interchange Intervention Accuracy (SIIA), Correlation coefficients between SIIT and 'natural' models' accuracy after ablation |

### 2. Leaderboard Tables

#### MIB: A Mechanistic Interpretability Benchmark

**Circuit Localization - Integrated Circuit-Model Distance (CMD)** (Lower is better)

| Rank | Method | Average CMD | Average CPR (Higher is better) | InterpBench AUROC (Higher is better) |
| :--- | :----- | :---------- | :----------------------------- | :----------------------------------- |
| **1** | **EAP-IG-act. (CF)** | **0.07** | **1.21** | **0.81** |
| 2 | EAP-IG-inp. (CF) | 0.07 | 1.62 | 0.71 |
| 3 | Hybrid-Ens (Mondorf et al., 2025) | 0.03 | 1.83 | N/A |
| 4 | P-Ens (Mondorf et al., 2025) | 0.04 | 1.59 | N/A |
| 5 | S-Ens (Mondorf et al., 2025) | 0.04 | 1.76 | N/A |
| 6 | ILP + PNR + Bootstrapping (Nikankin et al., 2025a) | 0.09 | 1.77 | N/A |
| 7 | ILP + PNR (Nikankin et al., 2025a) | 0.08 | N/A | N/A |
| 8 | UGS | 0.09 | 1.04 | 0.74 |
| 9 | EAP (CF) | 0.10 | 0.90 | 0.73 |
| 10 | IPE (CF) (Brunello et al., 2025) | 0.38 | 1.01 | N/A |
| 11 | EActP (CF) | 0.29 | 1.45 | 0.28 |
| 12 | EAP (mean) | 0.19 | 0.49 | 0.78 |
| 13 | EAP (OA) | 0.19 | 0.65 | 0.77 |
| 14 | ILP + Bootstrapping (Nikankin et al., 2025a) | N/A | 2.50 | N/A |
| 15 | NAP-IG (CF) | 0.33 | 0.82 | 0.62 |
| 16 | NAP (CF) | 0.43 | 0.52 | 0.30 |
| 17 | IFR | 0.55 | 0.48 | 0.71 |
| 18 | Random | 0.72 | 0.27 | 0.44 |

**Causal Variable Localization - Interchange Intervention Accuracy (IIA)** (Higher is better)

| Rank | Method | Average IIA | Average MSE (Lower is better) |
| :--- | :----- | :---------- | :---------------------------- |
| **1** | **DAS** | **0.70** | **2.14** |
| 2 | Non-linear featurizer (Hirlimann et al., 2025) | 0.87 | N/A |
| 3 | Orthogonal non-linear projection (Hirlimann et al., 2025) | 0.80 | N/A |
| 4 | DBM | 0.64 | 2.29 |
| 5 | DBM + PCA | 0.58 | 2.29 |
| 6 | DBM + SAE | 0.60 | N/A |
| 7 | Full Vector | 0.50 | 2.64 |

#### InterpBench: Semi-Synthetic Transformers for Evaluating Mechanistic Interpretability Techniques

**Circuit Discovery - Edge-level ROC AUC** (Higher is better)

| Rank | Method | Edge-level ROC AUC | Notes (Statistical Significance vs. ACDC) |
| :--- | :----- | :----------------- | :--------------------------------------- |
| **1** | **Automatic Circuit DisCovery (ACDC)** | **0.85** | Significantly better than Node SP, Edge SP, and EAP. Indistinguishable from EAP-IG. |
| 2 | Edge Attribution Patching with integrated gradients (EAP-ig) | 0.80 | Statistically indistinguishable from ACDC (p-value >= 0.05). |
| 3 | Edgewise Subnetwork Probing (Edgewise SP) | 0.60 | Statistically significantly worse than ACDC (p-value < 0.05). |
| 4 | Subnetwork Probing (SP) | 0.50 | Statistically significantly worse than ACDC (p-value < 0.05). |
| 5 | Edge Attribution Patching (EAP) | 0.30 | Statistically significantly worse than ACDC (p-value < 0.05). |

### 3. Method Summary

*   **EAP-IG-act. (CF)**: Edge Attribution Patching with Integrated Gradients (interpolating activations) and Counterfactual ablations. This method stands out on MIB for Circuit Localization, achieving the best average CMD and the highest InterpBench AUROC score among the core EAP variants.
*   **EAP-IG-inp. (CF)**: Edge Attribution Patching with Integrated Gradients (interpolating inputs) and Counterfactual ablations. A strong performer in MIB Circuit Localization, similar to `EAP-IG-act. (CF)`.
*   **DAS (Distributed Alignment Search)**: Excels in MIB's Causal Variable Localization tasks, achieving the highest average IIA and strong MSE performance. It uses counterfactual datasets to find aligned features.
*   **Automatic Circuit DisCovery (ACDC)**: The top performer on InterpBench for circuit discovery (edge-level ROC AUC). It is statistically significantly better than most other baselines on this benchmark.
*   **EAP-ig (InterpBench Context)**: While EAP generally performs poorly on InterpBench, adding integrated gradients (EAP-ig) significantly boosts its performance, making it statistically indistinguishable from ACDC on InterpBench.
*   **Ensembling Methods (P-Ens, S-Ens, Hybrid-Ens)**: These methods, particularly Hybrid-Ens, show competitive performance in MIB Circuit Localization, often improving upon individual EAP variants, indicating the benefit of combining different attribution strategies.
*   **ILP-based methods (Nikankin et al., 2025a)**: Methods combining Integer Linear Programming (ILP) with Positive-Negative Ratio (PNR) and/or Bootstrapping also show very strong performance in MIB Circuit Localization, achieving low CMD and high CPR.
*   **Orthogonal non-linear projection / Non-linear featurizer (Hirlimann et al., 2025)**: These are extensions of DAS, showing excellent IIA scores for causal variable localization on Llama-3.1, indicating advancements in disentangling conceptual variables.
*   **DBM (Desiderata-based Masking)**: Performs reasonably well in MIB Causal Variable Localization, with variations like DBM + PCA and DBM + SAE exploring different feature spaces for interpretability.
*   **Random / Full Vector**: Serve as baselines, consistently showing the worst performance across relevant metrics, highlighting the efficacy of actual interpretability methods.

### 4. Gaps & Opportunities

1.  **Comprehensive Cross-Benchmark Evaluation**: While methods are evaluated on MIB and InterpBench, there's no single method that appears at the top across *all* metrics and tasks within both benchmarks. For instance, ACDC excels on InterpBench, but isn't explicitly listed with top scores in MIB's primary leaderboards (though EAP-IG, a related technique, does well). This suggests methods might specialize, and a unified evaluation framework or further meta-analysis could highlight more generalizable techniques.
2.  **Aggregation of Complex Metrics**: MIB has a rich set of tasks and models (e.g., IOI, Arithmetic, MCQA, ARC on GPT-2, Qwen, Gemma, Llama). Presenting an aggregated "average CMD" or "average IIA" provides a high-level view but might obscure nuances where a method performs exceptionally well on one specific task/model but poorly on others. More detailed sub-leaderboards for each task/model combination would be beneficial.
3.  **Missing Scores for Specific Metrics/Tasks**: Several methods have "N/A" for certain scores (e.g., ensembling methods on InterpBench AUROC, DBM + SAE on some IIA tasks, DBM + PCA/DBM on MSE). This indicates incomplete evaluation coverage, which might be due to computational costs or method applicability. Filling these gaps would provide a more complete picture.
4.  **Circuit Size/Sparsity Metrics**: The MIB description mentions "Weighted edge count (for circuit size)" as a metric, but this is not present in the results data. Understanding not just performance but also the *compactness* of discovered circuits is crucial for mechanistic interpretability. Evaluating methods on this aspect would add valuable insight.
5.  **Long-Tail Tasks and Models**: While MIB covers several tasks and models, the "85 Tracr circuits" in InterpBench represent a vast array of algorithmic tasks. The InterpBench results currently only report an aggregated "Edge-level ROC AUC." Deeper analysis into which *types* of Tracr circuits methods perform well or poorly on could reveal specific strengths and weaknesses.
6.  **Real-world vs. Semi-Synthetic Benchmarks**: InterpBench uses semi-synthetic transformers with known ground truth, which is excellent for rigorous evaluation. MIB uses larger, pre-trained language models. Exploring how methods developed and evaluated on semi-synthetic data generalize to more complex, "natural" models without ground truth circuits remains a critical area.
7.  **Efficiency and Resource Usage**: The current scorecard focuses on performance metrics. Future evaluations could incorporate metrics like computational cost, memory usage, or time to convergence for each method, especially given the scale of modern LMs. This would be important for practical adoption.