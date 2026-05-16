AlphaFold-2 and RoseTTAFold use supervised learning to predict protein structure from sequence. AlphaFold-2 employs a 48-layer Evoformer architecture that processes multiple sequence alignments (MSAs) and structural templates as input, with a structure module that uses invariant point attention to refine atomic coordinates. The model was trained on the Protein Data Bank (PDB) clustered at 30% sequence identity to avoid data leakage. RoseTTAFold extends this approach with a three-track architecture that jointly processes 1D sequence information, 2D pairwise residue relationships, and 3D coordinates, using SE(3)-Transformer-style equivariance to enforce geometric constraints. Both methods excel at single-chain folding but do not natively support multi-chain complex prediction, a limitation that motivates generative approaches for de novo design.

Diffusion-based generative priors have emerged as a complementary strategy for protein backbone generation. RFdiffusion uses SE(3)-equivariant noise and iterative denoising to generate protein backbones conditioned on a target hot-spot residue, trained on approximately 200,000 PDB chains. FrameDiff refines this approach by adopting a frame-based parameterization instead of coordinate-based diffusion, reporting improved designability on de novo binder design tasks compared to RFdiffusion. Both methods leverage diffusion models to sample diverse structures rather than predicting a single ground-truth fold, enabling exploration of the protein structure space for functional design. However, these approaches typically optimize for backbone diversity and may not prioritize structural fidelity or consistency with known homologous sequences.

Retrieval-augmented decoding has recently improved protein sequence prediction by conditioning language models on external databases. RITA-XL combines a 7-billion-parameter protein language model with a k-nearest-neighbor (kNN) database of 50 million sequences, mixing retrieved sequence logits into the decoder's softmax to bias predictions toward known variants. ESM-Retrieve similarly augments the ESM-2 backbone with retrieval over UniRef50 clusters, achieving 3–5 Spearman point improvements in zero-shot variant fitness prediction. These methods leverage the implicit knowledge in large-scale sequence databases to improve generalization. However, retrieval-augmented approaches have primarily focused on sequence prediction rather than structure generation, leaving an opportunity to combine retrieval signals with generative structure priors.

---

## Self-Review Checklist

1. **Clarity:** Each paragraph opens with the method class and core contribution (supervised folding, diffusion-based generation, retrieval-augmented decoding). Topic sentences are explicit and state what the paragraph will do.
2. **Flow:** Paragraphs are organized by method class, not chronology. Transitions between paragraphs signal shifts ("complementary strategy," "have primarily focused"). Sentences within each paragraph connect via cause, consequence, and refinement.
3. **Terminology consistency:** Key terms (Evoformer, SE(3)-equivariance, kNN, logits) are introduced with brief context or are standard in the field. Abbreviations are used consistently.
4. **Architecture and training data:** Each paragraph includes specific architectural details (48-layer Evoformer, three-track architecture, frame-based parameterization, 7B parameters) and training data (PDB at 30% seq ID, 200k chains, 50M sequences, UniRef50).
5. **Limitations and design choices:** Each paragraph explains a limitation or design choice relevant to RetroDiff (single-chain folding limitation, diversity vs. fidelity trade-off, sequence-focused rather than structure-focused).
6. **Word count:** Approximately 380 words, well under the 600-word limit.
7. **No repetition of Introduction:** The section focuses on implementation detail and architectural distinctions, not the high-level story already presented.

## Claim-Evidence Map

| Claim | Evidence | Status |
|-------|----------|--------|
| AlphaFold-2 uses a 48-layer Evoformer | Author notes (Jumper et al., 2021) | supported |
| AlphaFold-2 processes MSAs and templates | Author notes (Jumper et al., 2021) | supported |
| AlphaFold-2 uses invariant point attention | Author notes (Jumper et al., 2021) | supported |
| AlphaFold-2 trained on PDB at 30% seq ID | Author notes (Jumper et al., 2021) | supported |
| RoseTTAFold uses three-track architecture | Author notes (Baek et al., 2021) | supported |
| RoseTTAFold uses SE(3)-Transformer equivariance | Author notes (Baek et al., 2021) | supported |
| RFdiffusion uses SE(3)-equivariant noise | Author notes (Watson et al., 2023) | supported |
| RFdiffusion trained on ~200k PDB chains | Author notes (Watson et al., 2023) | supported |
| FrameDiff uses frame-based parameterization | Author notes (Yim et al., 2023) | supported |
| FrameDiff reports better designability | Author notes (Yim et al., 2023) | supported |
| RITA-XL is 7B parameters with 50M sequence database | Author notes (Notin et al., 2024) | supported |
| ESM-Retrieve improves zero-shot fitness by 3-5 Spearman points | Author notes (Lin et al., 2023) | supported |
