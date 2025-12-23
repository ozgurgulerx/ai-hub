# OLMo

OLMo models are a highlight because they are fully transparent and come with detailed technical reports.

## Architecture notes (OLMo 3 vs Qwen3; to verify)

In the meantime, here's a side-by-side architecture comparison with Qwen3:

1. OLMo 3 is relatively similar to Qwen3, but it's likely evolving from OLMo 2 rather than being directly inspired by Qwen3.
2. Similar to OLMo 2, OLMo 3 uses a post-norm flavor instead of pre-norm; OLMo 2 reported it stabilizes training.
3. The 7B model still uses multi-head attention (like OLMo 2). To improve efficiency and shrink KV cache size, it uses sliding window attention (similar to Gemma 3).

Next, looking at the 32B model:

4. It's the same architecture scaled up, and proportions (e.g., FFN expansion) roughly match Qwen3.
5. A plausible explanation is that the architecture started somewhat smaller than Qwen3 due to a smaller vocabulary, then increased intermediate size expansion (e.g., ~5x in Qwen3 to ~5.4x in OLMo 3) to land at 32B for direct comparison.
6. The 32B model uses grouped query attention (GQA).

