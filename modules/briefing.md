# Briefing Module — extract execution from noise

Activates with `/designer-mestre briefing` (aliases `brief`, `traduz`) or automatically when the request arrives as a briefing (long text, email, transcribed audio, PDF, doc, WhatsApp screenshot). Runs **before** the task module. The result is a short list of what to execute, not a summary of the document.

## 1. Rules
- **Triage:** start from the current request and extract delivery verbs (e.g. organize assets, analyze creatives, create piece, export). Repetitions, revision history, reviewer names, links and general instructions only enter if they change one of these actions. An explicit current request beats old material; the briefing is a source, not an automatic task list.
- **Direction weights (internal, do not print the calculation):** `5` = text that goes **on the piece** (tag, headline, support, CTA: drives subject, topic and scene); `2` = piece-specific art note, used only if it reinforces the copy; `1` = general briefing context; `0` = history, already-completed revision, link or person merely mentioned. The higher weight wins a creative conflict. KV, rights, fidelity and explicit restrictions of the current request are mandatory limits, not points. A person, object or photo requirement cited outside the copy does not become a mandatory subject through repetition; only the explicit current request can promote them to a visual requirement.
- **Only what is necessary to execute.** For each action, keep the verifiable output, format/quantity when there is one, indispensable inputs and restrictions that affect execution. At triage, check the resolution of the main inputs (photos/logos): if it is a screenshot, thumbnail or low-resolution image (< 1200 px) that compromises the final piece, before warning, look for the larger original in the client's folders and at the source (`delivery.md` §2, proof 2); issue an immediate warning in `Blocks` and trigger the restoration flow (`image.md` §4). Strategy, media, budget, metrics and general context do not become items nor a discard section. Necessary deduction = `(assumed)`; do not invent deliverables.
- **Copy:** when the action includes a piece with text, transcribe the applicable text literally; do not rewrite or mix copy from other pieces. Copy not found in the client's source → ask: do you have the copy, or do you want me to create it with AI? Create only with the yes, and show the copy before assembling the piece.
- **Image:** use the weight-`5` copy to define the scene; look for a pertinent, authorized real photo when it serves that scene. If there is none, generate or compose another solution and identify the origin. A generic note about stock/real photo neither blocks nor imposes a portrait; stop only when the current request demands the specific asset or it is indispensable to fidelity/factual proof.
- **Conflict with the KV** (color, font, resource vetoed in `design_system.md`): point it out in 1 line when it affects the piece; the KV wins unless the user decides explicitly in the current request. A general briefing note does not change identity.
- **Questions:** at most 3, only those that prevent v1, each with the recommended option. The rest becomes a declared assumption.
- **Size:** fits on one screen. One line per action, in order of dependency and deadline. No introduction or briefing summary.

## 2. Output format
```
Do · [Client]
1. [Action + object + verifiable output]
2. [Action + object + verifiable output]

Needed to execute: [only files, literal copy, format and restrictions tied to the actions above]
Blocks: [only a gap that prevents one of the actions; up to 3 questions with recommendation]
Next step: [first action that can start now]
```
A line with no content disappears (do not write "none"). Several pieces can use a compact format/quantity table **inside the create action**, without replacing the action list.

## 3. After the translation
- Nothing blocks: go straight to the first action in the same response (organization, analysis or piece).
- Motion/video with voice: in the same response, extract the narration text per `video.md` §2.2 and write `Trabalho\narration.txt`; voice is a layer of the deliverable from the start, not of the revision.
- Save the list and applicable inputs as `briefing.md` in the request folder (`[AAAA]\[MM - Mês]\[AAAA-MM-DD] [TIPO] Título\`). `design_system.md` receives only durable brand learning, not the campaign list.
- The user's answer to a "Blocks" updates the affected line, without redoing the whole triage.

## 4. Reading sources
- PDF/Doc/email: read once. Screenshot/audio: transcribe only what changes an action or an indispensable input.
- Manager task (Ekyte etc.): list the comments at the start and treat the most recent link or copy as input; warn the user if it diverges from the briefing in use.
- Open only the links and folders needed for the extracted actions; a source that does not open or does not show the input on the 1st attempt → look for the same input in the client's folders and at the source (`delivery.md` §2, proof 2); only then ask, instead of insisting on the source. Failed access to irrelevant material does not block. Conflict that changes delivery, KV or copy: show excerpts and sources; ask only if there is no current decision from the user.
