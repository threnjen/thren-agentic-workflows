I have an unusual evaluation request.

On branch: phase/06e-goldenpath I have reverse-engineered feature decomposition documents in `dev/feature`. These are the "ground truth" docs.
On branch: phase/06e-update-decomp, I have feature documents produced by the feature decomposer agent (attached) in `dev/feature`. These are the "test docs".

the docs on `phase/06e-goldenpath` should be considered the "ground truth" decomposition docs.
I want you to compare these two sets of feature docs, and write output to `eval/feature_decomp_eval_round_5.md` about:

- how well the test docs match up for quality
- what the test docs did well
- what the test docs failed at
- evaluate the feature decomposer agent (attached) and look for opportunities to improve the agent or associated skills to reach output closer to the ground truth
- provide any other meaningful insights as to why elements were missed in the test docs

be sure to provide an overall probability score; see `eval/feature_decomp_eval_round_3.md` for a sample report (but do not use its insights, evaluate it only for formatting)