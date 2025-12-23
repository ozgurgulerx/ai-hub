# Why Training MoEs Is So Hard

This is a practitioner write-up capturing why “frontier-quality” *smallish* MoEs (e.g., <20B total params) are difficult to train, and what interventions helped when running research-scale experiments on limited hardware.

Status: **Unverified** (treat as informed notes; validate against primary sources and your own experiments).

---

recently, i have found myself wanting a small, research focused training repo
that i can do small experiments on quickly and easily. these experiments range
from trying out new attention architectures (MLA, SWA, NSA, KDA - all pluggable) to multi-precision training to most
recently multi optimizer setups with 'new' optimizers. i tried the 3 major
contenders (Nemo, Megatron and Torchtitan) but for many and various reasons they
very much did not fit the bill for my purposes and were all pretty painful to
setup, use and get running stably. I once again missed my tooling from google
and re-writing my production training stack for this purpose (which is tailor
made for large infrastructure monitoring and stability) also felt like a poor
use of time and would make both the old and the new repo worse off for it.

This did get me thinking however, why was training frontier quality 'smallish'
MoEs (say under 20B params total) so difficult? why didnt the repo / lib i
wanted already exist? After thinking about it for a while, most of the
challenges i could come up with came down to 3 different things:

- flops / flop efficiency
- load balancing / router stability
- data quality and quantity

## Flops

training dense models is pretty straight forward these days. the training
dynamics are mostly coupled, and if you have enough params in the architecture,
the model will pretty much learn despite your many mistakes (this has bitten me in
the ass more than once). [DeepSeek-style ultra-sparse](https://arxiv.org/abs/2412.19437v2) MoEs are different because your training dynamics are
somewhat decoupled. Only a portion of your MLPs are active for a given token,
and as training goes on, the active experts change and evolve over time. this is
what makes multi epoch training and data rephrasing so effective for MoEs
(especially larger ones). You get large inference efficiency wins and small
training efficiency wins but at the cost of decoupled training dynamics (makes
it hard to predictably and stably train) and you have to dump a lot more flops
in to make sure you learn a somewhat optimal routing policy and that the experts
involved in the various policies are adequately trained. Well this is where the
flops / flop efficiency challenge arises. The first challenge is that, by
nature, ultra-sparse MoEs take up a tremendous amount of HBM to load up the
experts but means you have a lot GPUs required and thus a lot of idle GPUs in
your system. FSDP (and the various other sharding topologies) are mostly a relic
of dense training, and do not do a very good job of adequately leveraging all
those stranded flops. This leads to (low) single digit MFUs for most people's
ultra-sparse MoE training. And while there are handful of ways of addressing
that (much more on this in the future) i focused on 2 specific things:

- new sharding topology (a novel expert-parallel dispatch system that keeps GPUs busy)
- mixed precision training

## Load Balancing / Router Stability

i will leave the new sharding topology for its own dedicated write up, but mixed precision training is a no-brainer. You have all this stranded HBM, so reduce expert precision and cut that baby by 1/2 or 1/4 (fp8 and nvfp4 respectively). That's good in theory, but in practice mixed precision training usually takes MORE HBM as you have to keep your master weights and grads in a higher precision, then quantize the master weights down to its lower precision representation and cache them for the next forward pass. So it helps inference efficiency (which as more and more flops go to RL and inference, this is a real win) but at the cost of even more HBM and more flops during training. Reducing the mixed precision overhead is something that should be a specific area of focus. However, anything you touch that reduces precision and accuracy of the weights ultimately leads to instability in the rest of the training dynamics. For MoE the first place this usually shows up is router stability.

The DeepSeek-V3 tech report describes a very elegant aux loss free training setup where there are very few knobs and the dynamics are very clear. These are clearly tools designed for the experienced user as getting the dynamics correct with only a very few knobs is incredibly difficult. Crucially, DeepSeek relies heavily on massive batch sizes to stabilize their routers - a luxury we don't have when doing research on limited hardware. So we have to work extra hard to make our small runs stable, efficient and informative. As i began experimenting with replicating their setup, specifically for mixed precision experts, it became very clear that the grads were far too small for fp8 or nvfp4 causing the routers to not learn and the experts to starve. I tried everything under the sun to make this work first with reduced precision backwards passes and eventually even with fp32 master weights and grads but the router collapse persisted. A well timed paper was the Character AI blog post describing their various int8 stability interventions. I tried them all but they ended up making the system much much less stable. So i went through them one at a time. The first one was muP embedding scaling of 10.66 and the logits scaling of 0.125. There were a bunch of very obvious wins here other than router stability, but one clear thing these scales did was took the very very small fp8 and nvfp4 expert grads and scaled them to the point where the ROUTER WAS FINALLY LEARNING! However, these wins also caused the bf16 grad norm to absolutely explode and the 'normal best practice' grad clipping and grad scaling was preventing any learning from happening. So, the solution? Remove all clipping and YOLO! Finally, we had stable mixed precision routers training. The other Kaiju intervention that ended up being incredibly useful was a single bungee virtual scalar at the output of the experts pre output norm initialized at 2.0 to match the bf16 grad scale and thus training dynamics such that nvfp4 and fp8 more or less presented the same loss curves as the baseline bf16 training runs (FP8-BF16 gap reduced from ~0.8 to <0.1 at 3k steps). There are many more tricks and 'best practices' used here (more about all of those in future posts as well) but the headlines were:

- add muP scaling
- remove all other clipping and live on the wild side
- bungee virtual scalar pre output norm
- keep aux loss free and tokens choice routing (cause we know the difference between right and wrong in this house)

## Data

Now that we had reasonably stable training dynamics, it became clear that if i ever wanted to share this repo with anyone, we would need some better data to really get the most out of this training lib. Another well timed release was [OLMo-3](https://allenai.org/blog/olmo3) with its open source data mixture recipe (shout out Ai2!!). However, when i tried using the OLMo-3 mixture directly from huggingface, i was getting pretty terrible results (compared to my typical FineWeb-Edu baseline). So, the data spelunking began and ... the datasets were pretty dirty. So, i did what any crazy person would do and i set out to build a frontier inspired data pipeline so i could really get the most out of this training repo.

The pipeline has a few key components:

- **Heuristic pre-filters**: Language ID, length filters, MinHash dedup, n-gram repetition, perplexity outliers, toxicity - the standard stuff to remove obvious garbage before spending GPU cycles
- **SeqIO-style dynamic mixtures**: Deterministic, resumable sampling that maintains your target ratios (40% CC, 20% code, etc) regardless of total token budget - critical for proxy runs where you're not training on 6.7T tokens
- **Model-based quality scoring**: This is where it gets interesting

For the quality scoring, i followed the [Seed-Coder](https://arxiv.org/abs/2509.25149v1) pattern: use large oracle models to generate training labels, then distill into a fast classifier. I initially experimented with a few oracle models (Kimi-K2, DeepSeek-V3.2 and [gpt-oss](https://github.com/openai/gpt-oss) 120B) but ended up keeping only the 120B class models as oracles - they were consistently the best at nuanced quality judgments. The oracles scored a sample of data across five dimensions for general content (helpfulness, correctness, coherence, complexity, verbosity - each 0-4) and four dimensions for code (readability, modularity, clarity, reusability - each 0-10). I then took a frozen gpt-oss 20B backbone and attached two small heads:

- **Probe head** at layer 18: Mean-pooled hidden states → Linear(2880→5). Ultra cheap, catches obvious garbage early
- **Judge head** at layer 24: Full sequence attention → small transformer encoder → Linear(512→5). More expensive but catches nuanced quality issues

The early-exit design is key - if Probe scores below threshold, we skip Judge entirely. At scale this saves ~15% compute while maintaining quality. The thresholds (τ_drop, τ_keep) are calibrated on a held-out set to hit target keep rates.

To my surprise, my keep rate for the OLMo-3 dataset was about 30% for CC and internet sources, and 50% for code, math and science. That's a lot of filtering, but the proxy model evals showed clear improvements over the unfiltered baseline.

We finally had a reasonably functional system that approximated all the things i loved about my large scale training infra and the great tools i had used before but was purpose built for training small MoEs for research and small model production runs. However, the repo had gotten trashed as a result of the constant experimentation and troubleshooting. Also, my dev team consists of me and a fleet of AI agents. As Vik recently said, "Live by the slop, die by the slop" and while i am normally very studious and strict on 'NO SLOP IN THIS HOUSE' the debris from all night troubleshooting and corpses of various abandoned experiments littered my repo. The configuration and bootstrapping complexity had also exploded. What had started out inspired by [nanochat](https://github.com/karpathy/nanochat) now looked a lot more like Megatron (no offense).

The result? We can now do meaningful MoE research on limited hardware - a 7B2A proxy on a single B200 GPU, a 16B4A on a single 8×B200 node - both hitting 30-40k tokens/sec/GPU. More importantly, the scaling is predictable: our 1→8 GPU runs show consistent behavior, which gives us confidence that research done on small proxies will transfer to larger runs. We'll be validating 32 and 64 GPU scaling next.

The solution? Start over and rewrite it all from scratch with the motivation to share it with the larger community. So, that is what i am doing now. Over the next few weeks, i will be releasing the various training repos, blog posts, data grading model weights and w&b style visualization and experiment tracking systems to the community. There is also a roadmap with full inference engines etc on the horizon. It's going to take a little longer than i had hoped due to both the scope of ambition and full re-write but i hope the community finds this as useful as i have.

---

## References

- [DeepSeek-V3 Technical Report](https://arxiv.org/abs/2412.19437v2)
- [Inside Kaiju: Building Conversational Models at Scale](https://blog.character.ai/inside-kaiju-building-conversational-models-at-scale/)
- [Moonlight: A Compute-Efficient MoE Training Framework](https://arxiv.org/abs/2506.03524)
- [Seed-Coder Technical Report](https://arxiv.org/abs/2509.25149v1)
- [OLMo-3: The Best Fully Open Model of its Class](https://allenai.org/blog/olmo3)

## Artifact (TODO)

- Picture of an early FP8 training run from the NViz dashboard (not yet added to repo).

