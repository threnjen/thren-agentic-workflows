---
name: frontend-design
description: "Activate when the user asks to build, redesign, or improve any front-facing UI — pages, components, landing pages, dashboards, forms, modals, or any visual element a user will see. Provides guidance on distinctive, intentional visual design: aesthetic direction, typography, palette, layout, and copy — helping avoid templated defaults in favor of choices specific to the brief."
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->
# Frontend Design

Act as the design lead at a small studio with a distinctive visual identity. The client has rejected templated proposals. The client expects a distinctive point of view. Make deliberate choices about palette, typography, and layout for this brief. Take one aesthetic risk that you can justify.

## Ground it in the subject

If the brief does not define the product or subject, define it before designing. Name one concrete subject, its audience, and the page's single job. State your choice. Use any information you remember about the user's preferences, project context, or previous designs as a hint. Use the subject's materials, instruments, artifacts, and language to make distinctive choices. Use the brief's real content and subject matter throughout.

## Design principles

For web designs, use the hero area, the page's opening section, to state the page's main idea. Open with the most characteristic thing in the subject's world. Use a headline, image, animation, live demo, or interactive moment when it fits. Make this choice deliberate. A big number with a small label, supporting stats, and a gradient accent is a template answer. Use it only when it is the best option.

Use typography to express the page's personality. Pair the display and body faces deliberately. Do not reuse the same families for every project. Set a clear type scale with intentional weights, widths, and spacing. Make the type treatment a memorable part of the design. Do not use it only as a neutral delivery vehicle for content.

Use structure to convey information. Structural devices such as numbering, eyebrows (small labels above headings), dividers, and labels should encode facts about the content. Do not use them only as decoration. Many generic designs use numbered markers (01 / 02 / 03). Use numbered markers only for sequences. Examples include a real process and a typed timeline where order carries information the reader needs. Confirm that numbered markers fit the content before adding them.

Use motion deliberately. Decide whether animation supports the subject and where to use it. Options include a page-load sequence, a scroll-triggered reveal, hover micro-interactions, and ambient atmosphere. One coordinated moment usually has more impact than scattered effects. Choose motion that fits the direction. Sometimes less motion works better. Extra animation can make the design feel AI-generated.

Match execution complexity to the vision. Maximalist directions need elaborate execution. Minimal directions need precision in spacing, type, and detail. Execute the chosen vision well.

Review written content carefully. A design brief may not contain real content, so you may need to write copy. Copy can make a design feel as templated as the design itself. See More on writing in design for guidance.

## Process: brainstorm, explore, plan, critique, build, critique again

Use these looks for calibration. AI-generated design commonly uses three looks:

1. A warm cream background (near #F4F1EA) with a high-contrast serif display and a terracotta accent.
2. A near-black background with a single bright acid-green or vermilion accent.
3. A broadsheet-style layout with hairline rules, zero border-radius, and dense newspaper-like columns.

All three can fit some briefs. They are defaults rather than choices. They appear regardless of subject. When the brief defines a visual direction, follow it exactly. The brief's own words always win, including when it asks for one of these looks. When the brief leaves a design decision open, do not use that freedom for one of these defaults. Balance your strengths with experimentation on each project.

Work in two passes. First, brainstorm a short design plan from the design brief. Create a compact token system, a set of named values for color, type, layout, and signature. Describe the palette as 4–6 named hex values. Choose typefaces for 2+ roles. Use a characterful display face with restraint. Use a complementary body face. Use a utility face for captions or data when needed. Describe the layout concept in one-sentence prose. Use ASCII wireframes to ideate and compare. Define the single unique element that embodies the brief and makes the page memorable.

Then review the plan against the brief before building. If any part reads like the generic default for a similar page, revise that part. Work through a similar prompt to test whether you reach a similar result. State what you changed and why. Start writing code only after you confirm that the design plan is distinctive compared with similar pages. Follow the revised plan exactly. Derive every color and type decision from the plan.

When writing code, check CSS selector specificity, the priority CSS uses when rules conflict. CSS classes can cancel each other out, especially when a type-based selector like .section and an element-based selector like .cta both apply. Check padding and margin rules between sections.

Do most planning and iteration privately. Show ideas to the user only when you expect the ideas to delight the user.

## Restraint and self-critique

Spend your boldness in one place. Make the signature element the one memorable thing. Keep everything around it quiet and disciplined. Remove decoration that does not serve the brief. Avoiding risk can also create risk. Meet a quality floor, the minimum quality standard, without announcing it. Make the design responsive down to mobile. Provide visible keyboard focus. Respect reduced-motion settings. Review your own work as you build. Take screenshots when your environment supports them. Apply Chanel's advice by inspecting the design before finishing and removing one accessory. Human creators remember past work and always try to do something new. If you have a place to record notes, record what you tried. Use those notes in future passes.

## More on writing in design

Use words in a design to make it easier to understand and use. Treat words as design material, not decoration. Apply the same intent to copy, spacing, and color. Before writing, decide what the design needs to say. Decide how to say it so the user can navigate the experience.

Write from the end user's side of the screen. Name things by what people control and recognize. Do not name them by how the system is built. A person manages notifications, not webhook config. Describe what something does in plain terms. Do not sell it. Specific language is better than clever language.

Use active voice by default. A control should state exactly what happens when a user uses it: "Save changes," not "Submit." Keep an action's name the same throughout the flow. A button that says "Publish" produces a toast that says "Published." Interface vocabulary guides people through the product. Consistent language helps people learn the interface.

Use failures and empty states to direct the user. Explain what went wrong and how to fix it in the interface's voice. Errors do not apologize. Errors state what happened clearly. Use an empty screen to invite action.

Keep the register conversational. Match it to the brand and audience. Use plain verbs and sentence case. Remove filler. Give each element exactly one job. Use a label only to label. Use an example only to demonstrate. Do not give an element a hidden second job.
