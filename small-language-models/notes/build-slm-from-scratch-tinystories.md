# Build a Small Language Model (SLM) From Scratch (TinyStories pipeline)

This note distills a tutorial-style walkthrough titled **“Build a Small Language Model (SLM) From Scratch”** (Shravan Kumar, Jul 25, 2025).

It describes an end-to-end pipeline for training a small GPT-style model on **TinyStories** using a **GPT-2-compatible tokenizer** and a **disk-backed binary token corpus**.

## Framing (as stated in the source)

- “Small language model” is framed as **< 1B parameters**.  
- The tutorial explores whether a **~10–15M parameter** model can generate coherent text.

These are presented as the author’s framing/questions, not a universal standard.

## Pipeline Overview (Distilled)

### 1) Dataset: TinyStories

- Uses the **TinyStories** dataset (`roneneldan/TinyStories`) from Hugging Face.
- Mentions ~**2M** training rows and ~**20k** validation rows.

### 2) Tokenization → a single binary token stream

Goal: convert all text samples into token IDs and store them sequentially on disk.

- Tokenizer: **GPT-2 encoding** via `tiktoken.get_encoding("gpt2")`.
- Processing function returns `{ ids, len }` per example (`ids = enc.encode_ordinary(text)`).
- Writes token IDs into `train.bin` / `validation.bin` as a single flat array using `numpy.memmap`.
- Uses `np.uint16` with the claim that GPT-2 token IDs fit `< 65536`.
- Writes in shards/batches (example shows `total_batches = 1024`) and flushes at the end.

Why disk / memmap (as described):

- Enables training over corpora larger than RAM by mapping the binary file into memory.

### 3) Creating input/output batches (next-token prediction)

The model is trained as a next-token predictor:

- Sample a random start index `i`
- `x = tokens[i : i + block_size]`
- `y = tokens[i + 1 : i + 1 + block_size]` (shifted by one)

Implementation detail (from the excerpt):

- A `get_batch(split)` function re-creates the memmap each batch to avoid a memory leak (citing a StackOverflow reference).
- Uses `pin_memory()` and `non_blocking=True` for faster CPU→GPU transfer when on CUDA.

### 4) Model: GPT-style transformer

The excerpt sketches a GPT-like architecture:

- Token embeddings + positional embeddings
- Stack of transformer `Block`s (multi-head self-attention + MLP)
- Final layer norm + linear language-model head
- Weight tying between token embeddings and output head

Example configuration from the excerpt:

- `vocab_size=50257`, `block_size=128`
- `n_layer=6`, `n_head=6`, `n_embd=384`
- `dropout=0.1`, `bias=True`

### 5) Training loop (pre-training)

The tutorial’s training loop structure:

- Sample batches from `train.bin`
- Forward pass → logits + cross-entropy loss
- Backprop with **gradient accumulation** (example mentions accumulation over **32** steps)
- Optimizer: `AdamW` with weight decay
- Learning rate schedule: warmup (`LinearLR`) then decay (`CosineAnnealingLR`)
- Mixed precision via `torch.amp.autocast` and (optionally) `GradScaler`
- Periodic evaluation; save best model parameters by validation loss

Note: the excerpt shows `learning_rate = 1e-4` and `min_lr = 5e-4`, which appears inconsistent (min > base). Treat the exact values as “example code” requiring verification.

### 6) Inference (generation)

- Load best saved weights.
- Generate next tokens iteratively with:
  - temperature scaling
  - optional `top_k` filtering
  - multinomial sampling

## Practical Takeaways (From the walkthrough)

- Disk-backed token corpora (`*.bin` via memmap) are a pragmatic way to train on large text without holding the full dataset in RAM.
- Keeping a fixed `block_size` and simple `(x, y)` shifting is the standard autoregressive LM training recipe.
- Small GPT-style models can be trained with familiar tooling (PyTorch, AdamW, warmup + cosine schedule, mixed precision, gradient accumulation).

## References (as provided)

- TinyStories paper (linked in the tutorial): `https://arxiv.org/abs/2305.07759`
- TinyStories dataset: `https://huggingface.co/datasets/roneneldan/TinyStories`
- `tiktoken` repo: `https://github.com/openai/tiktoken`
- nanoGPT training loop referenced in the excerpt: `https://github.com/karpathy/nanoGPT`

## Appendix: Raw Notes (Preserved)

The source includes detailed code blocks for:

- dataset tokenization with `datasets.map(...)`
- writing `train.bin` via `numpy.memmap` and dataset sharding
- `get_batch(split)` using shifted targets and CUDA `pin_memory()`
- GPT class skeleton (embeddings → blocks → head; weight tying; generate loop)
- training configuration (warmup + cosine, AdamW, GradScaler, gradient clipping)
