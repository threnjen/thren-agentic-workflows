## A Model Experiment

Totally anecdotal, single-data-point testing experiment. I ran this in my game development project which is in C-sharp and Unity. The whole game is vibe-coded, as I do not know C-sharp. Coded entirely from the start of the project using the custom spec-driven agentic workflow steps 1-4 and the Debugger.

### The stage:

My agentic workflow has four distinct steps.

1. Project planner - for planning out large, high-level view of the project, dividing it into phases of distinct concerns, and bootstrapping the next phase document one at a time. This phase is the "WHY" and high level "WHAT" and has the bird's eye overall business requirements, objectives, project goals, and end state defined.
2. Phase refiner - Iterate on a single project phase until the phase's outcomes and deliverables are clearly defined, with acceptance criteria and feature set definitions. It establishes a clear deliverable and outcomes for the phase. Most Phases divide into 5-10 feature sets. This phase is the "WHAT". 
3. Feature decomposition - agent that decomposes each feature set into clear docs with acceptance criteria and task plans. It is in charge of researching and planning the implementation. This is the phase that determines "HOW". Produces a set of docs per feature with clear Acceptance Criteria and code implementation plan.
4. Feature execution - Agent that implements each feature bundle in the phase using a subagent, then does a blind review with a different subagent, then plans out any manual QA. This stage takes the longest amount of time to run and is the most expensive phase. It accounts for about 75% of the time to complete a full Phase from step 1-4.


### The method of the testing:

For a single game sub-phase (Phase 06e), I established a baseline starting point. I used my best available harness/model to fully plan and feature decompose (agent steps 1-3). Decomposition created 6 distinct feature bundles.
From there I started a **golden-truth** branch and, again using the best model available, did agent step 4 (execution). I then did extensive manual QA and iterated on the phase until everything worked exactly as intended in the game.

Then, for each of a combination of Harnesses/Models, I went back to the baseline and made a new branch.
Using the same set of docs from phases 1-3 as the **golden-truth** branch, I then executed using all of the models in the attached picture to create an ****eval-branch**** for each harness/model combo.

Models were blind scored using an `Eval Grader Agent` which started at the baseline and checked out the **eval-branch**, then compared the **eval-branch** implementation with **golden-truth**. 9 metrics were scored including components like Equivalence (how closely the implementation matched golden truth), Scope Discipline (how tight the changes were about not touching superfluous files), Robustness (edge catching/planning), and other metrics. Metrics were weighted according to importance. From all of this a final score was calculated, using the **golden-truth** as 10s in all categories.

### Interesting takeaways:

- Copilot harness always performs worse at execution than the same model in its native harness (copilot/gpt5.4 vs codex/gpt5.4 for example)
- With my agents, Phases 1-3 are most critical, and a cheap model can execute Phase 4 with relative success. Claude Opus 4.6 was barely better than Claude Haiku 4.5 (both in Claude Code harness).
- GPT 5.5-high was not better than GPT 5.4-high (notable because the cost/credits/usage difference is signficant)
- The outstanding runaway winner was Open Source Chinese model Deepseek v4Pro which is DIRT cheap to use. Drawback not represented is it is VERY slow.
- Overall takeaway: Quality of plan docs and decomposition docs are most important. If you use the agents, use your best available harness/model for planning and decomposition, and then you can pass off execution to a cheaper model.
- Anecdotally, I have still found the Copilot harness to do the best job at exploring/refining Planning docs. I would continue to use it for that. Codex and Claude Code will both start writing when we should still be iterating.


Again this only applied to my own project and only had one test per harness/model, but it was a fun and enlightening experiment.

![Model evaluation results](images/model_results.png)

