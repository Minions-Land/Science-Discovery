You are a blind judge for a Stage 2 validation of academic-writing rules. Two responses (RED and BLUE) were produced by the same model from the same fixture. One had writing rules injected; the other did not. You do not know which is which.

## Fixture brief

# Fixture: S2 — Related Work (NLP Reasoning)

## Role
You are a Writer agent drafting the Related Work section for a NeurIPS 2026 paper on chain-of-thought reasoning in language models.

## Brief
Write a Related Work section (3 paragraphs, organized by method class) for the following paper:

**Paper**: ReasonFlow — combining learned reasoning templates with retrieval-augmented chain-of-thought for multi-step mathematical reasoning. Achieves 89.2% on GSM8K and 67.4% on MATH, with 5× fewer inference tokens than standard CoT.

**Method classes to cover**:
1. Chain-of-thought prompting and its variants (CoT, Zero-shot CoT, Auto-CoT, Complexity-based CoT)
2. Retrieval-augmented generation for reasoning (RAG-CoT, REPLUG, Self-RAG)
3. Learned reasoning templates / program synthesis (PAL, PoT, MathCoder, ToRA)

## Expected output
3 paragraphs by method class. Each paragraph: model + algorithm + implementation detail + why-prior-insufficient + connection to this paper. No itemize/enumerate. Full prose.


## RED response

## Related Work

Chain-of-thought (CoT) prompting has emerged as a foundational technique for improving reasoning in large language models. Seminal work demonstrated that explicitly generating intermediate reasoning steps substantially improves performance on multi-step reasoning tasks. Subsequent variants including Zero-shot CoT, which eliminates the need for in-context examples, and Auto-CoT, which automatically selects diverse examples for demonstration, have refined the approach. Complexity-based CoT further optimizes example selection by prioritizing demonstrations with intermediate reasoning steps of varying difficulty. However, these methods remain fundamentally limited by their reliance on prompt-based guidance without learned structure; they do not adapt reasoning patterns to specific problem domains or optimize the computational cost of reasoning chains. ReasonFlow addresses this gap by learning domain-specific reasoning templates that can be applied systematically across problem instances, reducing the need for exhaustive step-by-step generation.

Retrieval-augmented generation has proven effective for grounding language model outputs in external knowledge, and recent work has extended this paradigm to reasoning tasks. RAG-CoT integrates retrieval of relevant examples or knowledge into the reasoning process, while REPLUG and Self-RAG introduce mechanisms for retrieving and ranking supporting passages during generation. These approaches recognize that reasoning quality improves when models can access relevant external information. Yet retrieval-augmented reasoning methods typically treat retrieval and reasoning as separate stages, retrieving context before reasoning begins rather than dynamically adapting retrieval based on intermediate reasoning states. ReasonFlow complements retrieval-augmented approaches by combining learned reasoning templates with selective retrieval, enabling more efficient reasoning chains that retrieve information only when necessary and leverage structured reasoning patterns to guide both retrieval and generation.

Program synthesis and learned reasoning templates represent an alternative direction for structured reasoning. Methods such as PAL (Program-Aided Language models), PoT (Program of Thought), MathCoder, and ToRA translate reasoning problems into executable programs or intermediate representations that can be verified and optimized. These approaches achieve strong performance by leveraging symbolic computation and structured problem decomposition. However, they typically require either explicit program synthesis capabilities or domain-specific intermediate languages, limiting their applicability to domains where such representations are not naturally available. ReasonFlow generalizes this insight by learning flexible reasoning templates that capture domain-specific problem-solving patterns without requiring explicit program synthesis, achieving comparable efficiency gains while maintaining the flexibility of natural language reasoning and enabling integration with retrieval-augmented mechanisms for knowledge-grounded reasoning.


## BLUE response

Chain-of-thought prompting has emerged as a foundational technique for improving reasoning in language models. Wei et al. introduced CoT prompting, which encourages models to generate intermediate reasoning steps before producing a final answer, significantly improving performance on multi-step reasoning tasks. Zero-shot CoT extended this by showing that a simple prompt like "Let's think step by step" can elicit reasoning without task-specific examples. Auto-CoT further automated the selection of diverse reasoning examples, while Complexity-based CoT prioritized examples by reasoning complexity to better match problem difficulty. Despite these advances, standard CoT approaches suffer from inefficiency: they generate verbose reasoning chains that consume substantial inference tokens without guaranteeing optimal reasoning paths. ReasonFlow addresses this limitation by learning compact reasoning templates that capture essential reasoning patterns, reducing token consumption by 5× while maintaining or exceeding accuracy on mathematical reasoning benchmarks.

Retrieval-augmented generation has been adapted to enhance reasoning by grounding intermediate steps in external knowledge. RAG-CoT integrates retrieval into the chain-of-thought process, fetching relevant documents or examples to support each reasoning step. REPLUG and Self-RAG further refined this approach by allowing models to retrieve and evaluate supporting evidence dynamically during reasoning. These methods recognize that reasoning quality improves when models can access relevant external information, yet they remain computationally expensive due to repeated retrieval calls and the need to process retrieved context alongside generated reasoning. ReasonFlow complements this direction by combining learned templates with selective retrieval, enabling the model to retrieve only when necessary and to integrate retrieved information into pre-learned reasoning structures, thereby reducing both the number of retrieval operations and the total inference cost.

Learned reasoning templates and program synthesis approaches take a different angle by training models to generate structured reasoning representations rather than natural language chains. PAL (Program-Aided Language models) generates Python code to solve problems, PoT (Program of Thought) extends this to multi-step reasoning, and MathCoder combines code generation with in-context learning for mathematical problem-solving. ToRA (Tool-integrated Reasoning Agent) similarly leverages symbolic tools and learned reasoning patterns. While these methods achieve strong performance by leveraging structured representations, they typically require either extensive fine-tuning, specialized training data, or complex prompting strategies to generate valid and efficient programs. ReasonFlow builds on this foundation by learning reasoning templates that are more interpretable and efficient than full program synthesis yet more structured than natural language chains, achieving competitive performance on GSM8K (89.2%) and MATH (67.4%) while maintaining the efficiency gains of template-based reasoning.


## Your output (STRICT JSON, no other text)

```json
{
  "winner": "RED" | "BLUE" | "tie",
  "reasoning": "<= 100 words on what specifically distinguishes the winner",
  "skill_effect_estimate": "Prevents real failure" | "Calibrates response" | "Matches baseline" | "Degrades response",
  "confidence": "high" | "medium" | "low"
}
```
