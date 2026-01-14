# SOTA Scorecard: Mechanistic Interpretability

*Generated: 2026-01-14 18:12:23*

---

This scorecard synthesizes the provided benchmark and results data for mechanistic interpretability, offering an overview of evaluation landscapes, method performance, and emerging areas.

## Mechanistic Interpretability SOTA Scorecard

### 1. Benchmark Overview Table

| Benchmark Name | Description | Tasks | Metrics | ArXiv ID |
|:---------------|:------------|:------|:--------|:---------|
| **MIB: A Mechanistic Interpretability Benchmark** | A benchmark with two tracks (circuit localization and causal variable localization) spanning multiple tasks and models, favoring methods that precisely and concisely recover relevant causal pathways or causal variables in neural language models. | Indirect Object Identification (IOI), Arithmetic (Addition and Subtraction), Multiple-choice Question Answering (MCQA), AI2 Reasoning Challenge (ARC) - Easy, AI2 Reasoning Challenge (ARC) - Challenge | Integrated Circuit Performance Ratio (CPR), Integrated Circuit-Model Distance (CMD), AUROC (for InterpBench model with known ground-truth circuits), Interchange Intervention Accuracy (IIA), Mean-Squared Error (MSE) | 2504.13151 |
| **InterpBench** | A collection of 86 semi-synthetic yet realistic transformers with known circuits for evaluating mechanistic interpretability techniques, generated using Strict Interchange Intervention Training (SIIT). It aims to validate circuit discovery methods when the true algorithm is known. | 85 Tracr circuits (various algorithmic tasks, both classification and regression), Indirect Object Identification (IOI) (simplified version) | Interchange Intervention Accuracy (IIA), Strict Interchange Intervention Accuracy (SIIA), Node effect, Normalized KL divergence, Area Under the Curve (AUC) of ROC curves for circuit discovery techniques | 2407.14494 |
| **RAVEL (Resolving Attribute–Value Entanglements in Language Models)** | A dataset and benchmark designed to evaluate interpretability methods on their ability to localize and disentangle the attributes of different types of entities encoded as text inputs to language models (LMs). It focuses on assessing how well methods can isolate individual explanatory factors in model representations. | Attribute Disentanglement (for various entity types like City, Nobel Laureate, Verb, Physical Object, Occupation, each with multiple attributes like Country, Language, Field, Color, Duty) | Cause score, Iso score, Disentangle score (weighted average of Cause and Iso) | 2402.17700 |
| **CausalGym** | A benchmark that adapts and expands the SyntaxGym suite of tasks to evaluate interpretability methods on their ability to causally affect model behavior, specifically focusing on finding linear features in LMs that influence linguistic behaviors. | 29 linguistic tasks (e.g., Subject-Verb Number Agreement, Negative Polarity Item Licensing, Filler-Gap Dependencies, Garden Path effects, Gross Syntactic State) | Log odds-ratio (to measure causal effect), Selectivity (difference between odds-ratios on original task and control task) | 2402.12560 |
| **SAEBench: A Comprehensive Benchmark for Sparse Autoencoders in Language Model Interpretability** | A comprehensive evaluation suite that measures Sparse Autoencoder (SAE) performance across eight diverse metrics, spanning interpretability, feature disentanglement, and practical applications like unlearning. It aims to provide a standardized framework for comparing different SAE architectures and training methodologies. | Concept Detection (Sparse Probing, Feature Absorption), Interpretability (Automated Interpretability via LLM Judge), Reconstruction (Loss Recovered), Feature Disentanglement (Unlearning, Spurious Correlation Removal, Targeted Probe Perturbation) | L0 norm (sparsity), Loss Recovered, Automated Interpretability Score, k-Sparse Probing (accuracy of linear probe on top-k latents), Cause Metric (RAVEL), Isolation Metric (RAVEL), Disentangle Score (RAVEL), Absorption Score (complement of absorption), Unlearning Score (degraded accuracy on forget set while maintaining retain set accuracy), Spurious Correlation Removal (SSHIFT), Targeted Probe Perturbation (STPP) | 2503.09532 |
| **FIND (Function INterpretation and Description)** | A benchmark suite for evaluating automated interpretability methods on functions whose structure is known a priori. It contains procedurally generated functions resembling components of neural networks, and accompanying ground-truth descriptions. Methods are evaluated on their ability to generate descriptions (natural language or code) that explain function behavior. | Function interpretation (numeric functions, string functions, synthetic neural modules: Entities, Relations) | Normalized Mean-Squared Error (NMSE) (for code-based numeric function interpretations), Exact matching binary test (for code-based string function interpretations), Unit testing protocol (LM evaluator selects correct I-O pair from description) (for language-based string function interpretations and synthetic neural modules) | 2309.03886 |
| **RIPPLE EDITS** | A diagnostic benchmark of 5K factual edits designed to evaluate how well knowledge editing (KE) methods handle the 'ripple effects' of edits on related facts in language models. It proposes novel evaluation criteria that go beyond checking if an individual fact has been successfully injected. | Factual Knowledge Editing (evaluating ripple effects across various relations and entity types) | Logical Generalization (LG), Compositionality I (CI), Compositionality II (CII), Subject Aliasing (SA), Preservation (PV), Relation Specificity (RS) | 2307.12976 |
| **AxBench** | A large-scale benchmark for steering and concept detection in language models, using synthetic data. It evaluates model-control methods, including prompting and finetuning baselines, along two utility axes: concept detection and model steering. | Concept Detection (for open-vocabulary concepts), Model Steering (long-form generation with concept-based interventions) | Area Under the ROC Curve (AUROC) (for concept detection), F1 score (for concept detection under class imbalance), Overall steering score (harmonic mean of Concept score, Instruct score, Fluency score), Winrate (against SAEs for steering) | 2501.17148 |

### 2. Leaderboard Tables

#### MIB: A Mechanistic Interpretability Benchmark

**Circuit Localization Track (Lower CMD is better, Higher CPR/AUROC is better)**

| Method               | InterpBench AUROC | IOI GPT-2 CMD | IOI GPT-2 CPR | IOI Qwen-2.5 CMD | IOI Qwen-2.5 CPR | Arithmetic Llama-3.1 CMD | Arithmetic Llama-3.1 CPR |
|:---------------------|:------------------|:--------------|:--------------|:-----------------|:-----------------|:-------------------------|:-------------------------|
| **EAP-IG-act. (CF)** | **0.81**          | **0.03**      | 1.82          | **0.01**         | **1.63**         | **0.00**                 | 0.98                     |
| EAP-IG-inp. (CF)     | 0.71              | **0.03**      | 1.85          | 0.02             | 1.63             | **0.00**                 | 0.99                     |
| EAP-IG-inputs (CF) (2510.25786) | N/A         | **0.03**      | **1.89**      | 0.02             | 1.73             | **0.01**                 | 0.98                     |
| EAP-IG-act. (CF) (2510.25786) | N/A         | 0.02          | 1.84          | **0.01**         | 1.61             | **0.00**                 | 0.98                     |
| EAP (CF)             | 0.73              | **0.03**      | 1.2           | 0.15             | 0.26             | 0.01                     | 0.55                     |
| UGS                  | 0.74              | **0.03**      | 0.97          | **0.03**         | 0.98             | 0.20                     | 1.17                     |
| UGS (2510.25786)     | N/A               | 0.04          | 0.97          | 0.02             | 1.00             | 0.19                     | **1.17**                 |
| EAP (OA)             | 0.77              | 0.3           | 0.95          | 0.16             | 0.7              | 0.11                     | 0.29                     |
| EAP (mean)           | 0.78              | 0.29          | 0.29          | 0.18             | 0.71             | 0.07                     | 0.35                     |
| IFR                  | 0.71              | 0.42          | 0.58          | 0.69             | 0.31             | 0.22                     | 0.89                     |
| NAP-IG (CF)          | 0.62              | 0.27          | 0.76          | 0.2              | 0.29             | 0.18                     | 0.39                     |
| NAP (CF)             | 0.3               | 0.38          | 0.28          | 0.33             | 0.3              | 0.28                     | 0.27                     |
| Random               | 0.44              | 0.75          | 0.25          | 0.72             | 0.28             | 0.75                     | 0.25                     |
| EActP (CF)           | 0.28              | 0.02          | **2.3**       | 0.49             | 1.21             | 0.36                     | 0.85                     |

*(Note: Best scores are highlighted. Some methods have additional results for other tasks/models not shown for brevity, e.g., MCQA, ARC. EAP-IG-act. (CF) shows very strong overall performance across CMD, especially for Llama-3.1, and high AUROC.)*

**Causal Variable Localization Track (Higher IIA is better, Lower MSE is better)**

| Method     | ARC(E) Gemma-2 OAnswer IIA Mean | MCQA Gemma-2 OAnswer IIA Mean | RAVEL Gemma-2 ACont IIA Mean | IOI GPT-2 SPos MSE | IOI GPT-2 STok MSE |
|:-----------|:--------------------------------|:------------------------------|:-----------------------------|:-------------------|:-------------------|
| **DAS**    | **0.88**                        | **0.95**                      | **0.75**                     | **2.20**           | **2.08**           |
| DBM        | 0.82                            | 0.84                          | 0.66                         | 2.22               | 2.35               |
| DBM+PCA    | 0.78                            | 0.57                          | 0.63                         | 2.24               | 2.33               |
| DBM+SAE    | 0.7                             | 0.73                          | 0.64                         | N/A                | N/A                |
| Full Vector | 0.63                            | 0.61                          | 0.48                         | 2.45               | 2.82               |

*(Note: DAS consistently outperforms other methods across IIA scores for causal variable localization and achieves the lowest MSE on IOI tasks.)*

#### InterpBench

**Edge AUROC (median) (Higher is better)**

| Method                                      | Edge AUROC (median) | Notes                                                                                                                                                                                                                                                                                                                                                               |
|:--------------------------------------------|:--------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Automatic Circuit Discovery (ACDC)**      | **0.95**            | ACDC showed strong performance. Statistically different (p-value < 0.05) from Node SP, Edge SP, and EAP. Statistically indistinguishable from EAP with integrated gradients (p-value >= 0.05).                                                                                                                                                                           |
| Edge Attribution Patching with IG (EAP-ig)  | 0.90                | A strong contender, performing comparably to ACDC (p-value >= 0.05, A12 effect size = 0.555, indicating ACDC is slightly better but not statistically significant).                                                                                                                                                                                                   |
| Edgewise Subnetwork Probing (Edge SP)       | 0.75                | Performed worse than ACDC (p-value = 0.028417, A12 effect size = 0.541). Statistically indistinguishable from EAP with integrated gradients (p-value >= 0.05).                                                                                                                                                                                                          |
| Subnetwork Probing (Node SP)                | 0.65                | Performed significantly worse than ACDC (p-value = 0.000427, A12 effect size = 0.742).                                                                                                                                                                                                                                                                              |
| Edge Attribution Patching (EAP)             | 0.20                | Performed poorly, significantly worse than ACDC (p-value = 0.000061, A12 effect size = 0.91).                                                                                                                                                                                                                                                                         |

#### RAVEL (Resolving Attribute–Value Entanglements in Language Models)

**Disentangle Score (Higher is better)**

| Method             | Disentangle_Entity | Disentangle_Context | Notes                                                                                                                                     |
|:-------------------|:-------------------|:--------------------|:------------------------------------------------------------------------------------------------------------------------------------------|
| **MDAS**           | **0.601**          | **0.656**           | Multi-task extension of DAS. Achieves state-of-the-art results on RAVEL.                                                                  |
| DAS                | 0.565              | 0.573               | Learns a linear subspace with a training objective defined using interchange interventions. Trained with counterfactual supervision.      |
| MDBM               | 0.537              | 0.539               | Multi-task extension of DBM. Shows improved disentanglement over DBM.                                                                     |
| DBM                | 0.522              | 0.498               | Differential Binary Masking. Learns a binary mask to select neurons, trained with counterfactual supervision.                               |
| RLAP               | 0.488              | 0.509               | Relaxed Linear Adversarial Probe. Supervised probe method that learns a linear subspace.                                                  |
| SAE                | 0.486              | 0.468               | Sparse Autoencoder. Achieved lowest Disentangle scores among non-baseline methods.                                                        |
| Full Rep. (Baseline) | 0.405              | 0.395               | Baseline method: simply replaces the full representation without any interpretability technique.                                          |
| PCA                | 0.395              | 0.391               | Principal Component Analysis. Achieved lowest Disentangle scores among non-baseline methods (even lower than Full Rep. on Entity). |

#### CausalGym

**No specific results were provided in the collected data for CausalGym.** The entry only contained an "Ambiguities" section.

#### SAEBench: A Comprehensive Benchmark for Sparse Autoencoders in Language Model Interpretability

*(Note: SAEBench results are highly nuanced, depending on architecture, dictionary size, and specific metrics. The descriptions below summarize key performance trends rather than providing a simple ranking table.)*

*   **Matryoshka BatchTopK SAE**: **Best overall** for **Concept Detection** (5 of 8 metrics, especially L0 40-200) and **Feature Disentanglement** (5 of 8 metrics, especially L0 40-200). Shows **positive scaling** or minor degradation with dictionary size on disentanglement metrics (e.g., SCR improves, absorption degrades minimally). Achieved **best scores** on RAVEL, Feature Absorption (1-Absorption Score), Sparse Probing, Spurious Correlation Removal (SCR), and Targeted Probe Perturbation (TPP).
*   **BatchTopK SAE**: **Best performance** on the **Sparsity-Fidelity Frontier** at low L0 (<100), e.g., highest Loss Recovered (~0.98 for 65k width Gemma-2-2B at L0 ~50). Generally outperforms TopK, JumpReLU, Gated, Matryoshka, P-Annealing, and ReLU in this regime.
*   **TopK SAE & JumpReLU SAE**: Perform better than ReLU on the Sparsity-Fidelity Frontier at low L0, generally positioned after BatchTopK.
*   **Gated SAE**: Superior Loss Recovered compared to P-Anneal SAE, but outperformed by P-Anneal SAE on Feature Absorption.
*   **P-Annealing SAE**: Consistently outperforms Gated SAE on Feature Absorption, but has lower Loss Recovered.
*   **ReLU SAE**: The original SAE design. Exhibits **worst performance** on Loss Recovered among various architectures and **inverse scaling** on feature disentanglement metrics (e.g., SCR performance degrades with increasing dictionary size). Generally outperformed by other methods across most metrics, except for Sparse Probing (k=1) where it performs best for L0 > 200.
*   **Gemma-Scope SAEs (various architectures)**:
    *   **Loss Recovered & Automated Interpretability**: Consistently improves with increased width (16k to 1M latents).
    *   **Feature Absorption (1-Absorption Score), Spurious Correlation Removal (SCR), Targeted Probe Perturbation (TPP)**: Degrades at larger widths.
    *   **Unlearning Capability**: Best at earlier layers, significantly varies by layer (scores near zero for final evaluated layer).
    *   **Sparse Probing**: Scores increase at later layers.

#### FIND (Function INterpretation and Description)

**Interpretation Accuracy (Higher is better, NMSE < 0.1 means accuracy for that threshold)**

| Method                  | Numeric (Code - NMSE < 0.1) | Strings (Code - Exact Match) | Strings (Language - Unit Test) | Entities (Language - Unit Test) | Relations (Language - Unit Test) |
|:------------------------|:----------------------------|:-----------------------------|:-------------------------------|:--------------------------------|:---------------------------------|
| **AIA + MILAN (GPT-4)** | N/A                         | N/A                          | N/A                            | **0.89**                        | **0.92**                         |
| MILAN (GPT-4)           | N/A                         | N/A                          | N/A                            | **0.89**                        | 0.74                             |
| AIA (GPT-4)             | **0.33**                    | **0.23**                     | **0.82**                       | 0.56                            | 0.74                             |
| AIA + MILAN (GPT-3.5)   | N/A                         | N/A                          | N/A                            | 0.88                            | 0.68                             |
| MILAN (GPT-3.5)         | N/A                         | N/A                          | N/A                            | 0.81                            | 0.64                             |
| AIA (GPT-3.5)           | 0.12                        | 0.13                         | 0.66                           | 0.39                            | 0.64                             |
| AIA + MILAN (Llama-2-70b-chat) | N/A                | N/A                          | N/A                            | 0.62                            | 0.46                             |
| MILAN (Llama-2-70b-chat) | N/A                       | N/A                          | N/A                            | 0.61                            | 0.44                             |
| AIA (Llama-2-70b-chat)  | 0.01                        | 0.01                         | 0.33                           | 0.34                            | 0.47                             |
| AIA + MILAN (Llama-2-13b-chat) | N/A               | N/A                          | N/A                            | 0.58                            | 0.42                             |
| MILAN (Llama-2-13b-chat) | N/A                       | N/A                          | N/A                            | 0.54                            | 0.45                             |
| AIA (Llama-2-13b-chat)  | 0.0                         | 0.0                          | 0.33                           | 0.34                            | 0.46                             |

*(Note: GPT-4 consistently performs best across all tasks where it's evaluated, both for AIA and MILAN methods, and their combination. "AIA + MILAN" demonstrates superior performance on "Relations (Language - Unit Test)" compared to individual methods.)*

#### RIPPLE EDITS

**Average Score (Avg) across LG, CI, CII, SA, PV, RS (Higher is better)**

| Method             | Model        | Avg_RECENT | Avg_RANDOM | Avg_POPULAR | Notes |
|:-------------------|:-------------|:-----------|:-----------|:------------|:------|
| **ICE**            | **LLAMA**    | **82.8**   | **82.5**   | **81.3**    | In-Context Editing baseline. Shows very strong generalization and preservation. |
| **ICE**            | **GPT-3**    | **82.8**   | **90.3**   | 77.7        | In-Context Editing baseline. Especially strong on RANDOM edits. |
| ROME               | GPT-NeoX     | 71.4       | 58.3       | 59.7        | GPT-NeoX (20B parameters) model. |
| ICE                | GPT-NeoX     | 69.9       | 81.0       | **74.1**    | In-Context Editing baseline. |
| ROME               | LLAMA        | 60.8       | 48.7       | 49.4        | LLAMA (7B parameters) model. |
| MEMIT              | GPT-2        | 58.0       | 49.1       | 49.6        | GPT-2 XL model. |
| ROME               | GPT-J        | 57.5       | 48.8       | 48.4        | GPT-J (6B parameters) model. |
| ROME               | GPT-2        | 57.5       | 45.5       | 48.7        | GPT-2 XL model. |
| MEMIT              | GPT-J        | 55.0       | 48.4       | 50.2        | GPT-J (6B parameters) model. |
| MEND               | GPT-2        | 52.1       | 38.8       | 43.9        | GPT-2 XL model. |

*(Note: In-Context Editing (ICE) methods consistently achieve the highest average scores, particularly for larger models like LLAMA and GPT-3, demonstrating strong ripple effect handling across different edit types.)*

### 3. Method Summary

*   **Edge Attribution Patching (EAP) variants (EAP-IG-act., EAP-IG-inp., UGS)**: These methods, particularly when combined with Integrated Gradients (IG) and Counterfactual (CF) ablations, demonstrate **SOTA performance** in the **circuit localization track of MIB**, achieving the lowest Circuit-Model Distance (CMD) and high Integrated Circuit Performance Ratio (CPR) across various LMs (GPT-2, Qwen-2.5, Gemma-2, Llama-3.1). They also show strong AUROC on InterpBench when using Integrated Gradients. This suggests causal patching methods are effective for precise circuit recovery.
*   **Automatic Circuit Discovery (ACDC)**: **SOTA on InterpBench**, achieving the highest median Edge AUROC (0.95), proving highly effective in discovering known circuits in semi-synthetic transformers.
*   **Distributed Alignment Search (DAS) / Multi-task DAS (MDAS)**: DAS is **SOTA in the causal variable localization track of MIB**, showing the highest Interchange Intervention Accuracy (IIA) and lowest MSE for tasks like MCQA and IOI. MDAS is the **SOTA method for RAVEL**, excelling at disentangling attribute-value representations in LMs, highlighting the importance of identifying distributed features with multi-task supervision.
*   **Sparse Autoencoders (SAE) / Matryoshka BatchTopK SAE**: While the original ReLU SAE shows weaknesses, advanced SAE architectures like **Matryoshka BatchTopK SAE are SOTA on SAEBench** across multiple metrics for concept detection and feature disentanglement, showing positive scaling with dictionary size for interpretability. This indicates significant progress in learning sparse, interpretable features, though performance varies greatly with architecture and width.
*   **Automated Interpretability Agent (AIA) / MILAN**: These methods, especially when powered by large, capable LLMs like **GPT-4**, are **SOTA on FIND**, generating accurate natural language or code descriptions for function behavior. The combination of AIA and MILAN further boosts performance on complex tasks like 'Relations' interpretation.
*   **In-Context Editing (ICE)**: **SOTA on RIPPLE EDITS**, demonstrating superior handling of ripple effects in factual knowledge editing, especially for larger models like LLAMA and GPT-3. This suggests that leveraging the model's in-context learning abilities is highly effective for robust knowledge manipulation.
*   **Desiderata-Based Masking (DBM)**: Performs well in causal variable localization on MIB, and is improved by its multi-task extension (MDBM) on RAVEL.
*   **Random / Full Vector / PCA / Full Rep.**: These are generally baseline or simpler methods that consistently perform worse than specialized interpretability techniques across benchmarks (e.g., Random on MIB, Full Rep. and PCA on RAVEL, Full Vector on MIB causal variable localization).

### 4. Gaps & Opportunities

1.  **Standardized Benchmarking for CausalGym:** The lack of concrete results in the provided data for CausalGym highlights a potential gap. While the benchmark is defined, the absence of publicly available, regularly updated SOTA results makes it challenging to assess progress in evaluating interpretability methods for their ability to causally affect linguistic behaviors.
2.  **Cross-Benchmark Comparisons and Generalizability:** Many methods excel on one or two specific benchmarks. For example, EAP-IG variants are SOTA for circuit localization on MIB and InterpBench, while DAS/MDAS lead on RAVEL and MIB's causal variable localization. There's an opportunity to investigate if methods can generalize across different interpretability goals (e.g., circuit discovery vs. variable localization vs. feature disentanglement).
3.  **SAE Evaluation Complexity:** SAEBench reveals the complex interplay between SAE architecture, dictionary size, model size, and various metrics. Summarizing SOTA for SAEs is challenging due to these dependencies. A standardized way to aggregate or visualize performance across these dimensions, perhaps with recommended architectures/hyperparameters for specific use cases, would be beneficial.
4.  **Scaling to Larger, More Complex Models:** While some benchmarks evaluate on models like Llama-3.1 (MIB) or GPT-3/LLAMA (RIPPLE EDITS), many detailed interpretability analyses are still on smaller models (e.g., GPT-2 on MIB, Tracr circuits on InterpBench). There's a continuous need for benchmarks and methods that scale effectively to even larger, more complex frontier models.
5.  **Robustness and Reliability:** The distinction between "Mean" and "Best" IIA scores in MIB's causal variable localization suggests variability in method performance. Further research could focus on metrics and benchmarks that emphasize the robustness and reliability of interpretability methods, not just peak performance.
6.  **"Human-in-the-Loop" Evaluations:** While FIND includes "Automated Interpretability via LLM Judge," and some benchmarks imply human evaluation through descriptions, more explicit benchmarks for human-centered interpretability (e.g., how well explanations aid human understanding, debugging, or control) could be a crucial future direction.
7.  **Efficiency and Computational Cost:** The scorecard does not capture the computational cost or efficiency of these methods. This is a practical consideration for researchers and practitioners, especially for SOTA methods. Future benchmarks could integrate efficiency metrics.