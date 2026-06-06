# Agentic AI Terminology: Model, Harness, Agents, Skills, and Hooks

**Purpose:** This document explains a few common agentic AI concepts in plain language, then goes a level deeper for people who want to understand how these systems are put together.

The goal is to make it easier to explain why the same prompt can behave differently in ChatGPT, GitHub Copilot, Claude Code, or another AI product — even when the underlying model is similar or identical.

---

## The Short Version

When people say "I'm using AI to help me code" or "I asked the AI to write this," there are actually several layers involved — not just one thing. Understanding those layers explains a lot of otherwise confusing behavior.

| Layer | What it is | Examples |
|---|---|---|
| **Model** | The AI brain doing the reasoning | GPT-4o, Claude Sonnet, Gemini |
| **Harness / Orchestrator** | The product wrapping the model | GitHub Copilot, Claude Code, Cursor, ChatGPT |
| **Agent** | A specialized role defined inside the harness | Planner Agent, Reviewer Agent, QA Agent |
| **Context** | Everything the model can "see" right now | Your file, conversation history, instructions |

---

## Basic Concepts

### Model (the AI Brain)

The model is the underlying AI that reads text and generates a response. It has been trained on large amounts of data and learned how to reason, write, and follow instructions.

The model itself is stateless — it does not remember previous conversations, does not browse the internet on its own, and does not take actions. It only reads what it is given and produces output.

**Examples:** Claude Sonnet 4.6, GPT-4o, Gemini 1.5 Pro

**Analogy:** The model is the engine. It is powerful on its own, but it does not decide where to drive or what route to take.

---

### Harness / Orchestrator (the Product Layer)

The harness is the product or tool that wraps around the model. It is responsible for deciding:

- What instructions to give the model (often without you seeing them)
- What information to include in each request
- How to handle the model's response
- Whether to call tools, run code, search files, or loop back with follow-up requests

This is why the same prompt can produce noticeably different results in ChatGPT versus GitHub Copilot versus Claude Code — even if all three are using the same underlying model. The harness shapes how the model behaves.

**Examples:** GitHub Copilot, Claude Code, Cursor, Windsurf, ChatGPT, Microsoft Copilot

**Analogy:** The harness is the vehicle and the driver combined. It decides where to go, what tools to use, and how to get there — the engine just powers it.

---

### Agent (a Specialized Role)

Inside a harness, it is common to define multiple agents. Each agent is a configured role with a specific job, a specific set of instructions, and sometimes access to specific tools.

Rather than having one general-purpose AI handle everything, you break the work into roles. A Planner Agent decides what needs to happen. An Implementer Agent writes the code. A Reviewer Agent checks the result. Each one is still powered by the same underlying model — they just have different instructions and responsibilities.

**Examples:** Planner, Implementer, QA Agent, Reviewer, Code Auditor

**Analogy:** Agents are like job roles on a team. Same company (harness), same talent pool (model), different responsibilities.

---

### Context (what the model can see)

Context is everything that gets passed to the model in a single request. This includes your prompt, any files or code you are working on, the conversation history so far, and any background instructions the harness has added.

The model can only work with what is in its context. It cannot remember what you said two days ago unless the harness has explicitly included it. It cannot see files it has not been shown. If something is not in context, it does not exist from the model's perspective.

Context has a limit (called the context window), and managing what goes in and out of it is one of the harness's most important jobs.

**Analogy:** Context is the whiteboard in the room. The model can only respond to what is written on it. The harness decides what gets written there.

---

## Advanced Concepts

*This section is for people who want to understand how agentic systems are actually structured and configured.*

### Skills (reusable instructions and behaviors)

A skill is a reusable, packaged set of instructions that can be given to an agent to extend what it knows how to do. Rather than rewriting the same guidance in every agent definition, you write it once as a skill and attach it where needed.

Skills are typically stored as files in the repository and loaded into an agent's context when it runs. They might cover things like: how to format commit messages, how to write tests for a specific framework, how to handle a particular kind of error, or what conventions the codebase follows.

Skills are composable — an agent can be given one skill or several, depending on what its job requires.

**Why it matters:** Skills are what allow agent behavior to be maintained and improved over time without rewriting every agent definition from scratch. They are the unit of reuse in a well-structured agentic system.

**Example:** A `python-testing-conventions.md` skill might be attached to both the Test Writer Agent and the QA Agent, so both operate with the same understanding of how tests should be structured in this codebase.

---

### Hooks (event-driven automation)

A hook is a trigger that fires automatically when a specific event occurs. In the context of agentic AI tooling, hooks allow you to connect agent behavior to events in the development workflow — without a human having to manually kick things off.

Examples of events that can trigger hooks: a file is saved, a pull request is opened, a commit is made, a test run completes, or a build fails.

When the hook fires, it can pass relevant context to an agent and let it take action. This is how you build workflows that run autonomously rather than requiring a human to type a prompt each time.

**Why it matters:** Hooks are what turn a collection of agents into a pipeline. Without hooks, you have a set of useful tools you spawn manually. With hooks, you have a system that responds to your work as it happens.

**Example:** A post-commit hook triggers the Code Auditor Agent with the diff. The agent checks for security issues and posts a comment to the PR automatically — no one had to ask it to.

---

### Tools (capabilities the model can spawn)

Tools are specific capabilities that the harness exposes to the model, allowing it to take actions beyond just generating text. When a model has access to tools, it can decide during its reasoning process to call one — and the harness will execute that call and return the result.

Common tools include: reading or writing files, running shell commands, executing code, searching the web, querying a database, or calling an external API.

Tools are what give an agentic system the ability to actually do things, not just say things.

**Important distinction:** The model decides *when* to use a tool and *what to pass to it*. The harness decides *which tools are available* and *actually executes them*. The model never runs code directly — it asks the harness to run it.

**Why it matters:** The set of tools available to an agent defines the boundary of what it can do. A model with no tools can only produce text. A model with file access, code execution, and API calls can perform meaningful work autonomously.

**Example:** A Planner Agent uses a file-read tool to inspect the codebase, a search tool to look up relevant documentation, and then writes its plan to a file using a file-write tool — all in one pass, with no human involved in the middle steps.

---

## Putting It Together

Here is how these layers interact in a typical agentic coding workflow:

1. A developer makes a commit. A **hook** detects the event.
2. The **harness** (e.g., Claude Code) assembles a **context**: the diff, the relevant files, and a loaded **skill** describing the project's code standards.
3. The harness routes this to the Code Auditor **Agent**, which has been configured with a specific role and set of instructions.
4. The **model** reads the context and reasons about what to do. It decides to call a **tool** to read one more file for additional context.
5. The harness executes the tool call and returns the result.
6. The model produces its output — a review comment — which the harness posts to the pull request.

The developer sees only the comment. Everything else happened in the layers underneath.

---

*For questions or corrections, reach out to the platform team.*
