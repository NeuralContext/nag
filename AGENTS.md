## Reference Material
If you are requested to "only" or "exclusively" or "just" review one or more artifacts, only review those. If you are not provided with explicity guidance on what to review before starting, review all of the files in the docs/design folder and adhere to all of the design, architecture, guidance, constraints, process, and goals outlined in those documents.

## Dev Environment
- Poetry is used to manage dependencies and execute scripts and run applications
- Run all poetry commands (e.g. compile, lint, tests) using the Poetry environment (e.g. `poetry run ...`) and do not use the system Python interpreter for repository validation.
- If `poetry run check` fails with numerous import errors, it's probably due to your sandbox environment. Run `poetry run check` outside your sandbox environment if this happens.

## Agent resources — `.agents/`

`.agents/` contains agent-facing material, shared by every coding agent:

- `.agents/specs/` — spec files relevant to the current feature under development. These are ephemeral and will be removed after each feature is completed.
- `.agents/skills/` — the skills both agents load, each self-contained. Codex reads this path natively; `.claude/skills` is a symlink to it so Claude Code sees the same files. Edit skills here only, never through the symlink's own path.

This file is the root instruction file; `CLAUDE.md` is a symlink to it.

## Testing Instructions
- `poetry run fmt`, `poetry run lint`, `poetry run check` (type checking), and `poetry run pytest -m "fast"` and `poetry run pytest -m "slow"` should always be executed and all issues should be fixed before considering a task/spec complete. It is okay to carry some broken tests forward if a larger feature is split across multiple specs. Fix issues in the 'fast' tests first to reduce cycle time.
- If you want to run tests that are marked `very_slow`, you should ask first -- prefer running the other tests.
- All spec implementations should include directions for creating integration tests that verify functionality and correctness.
    - Integration tests should use the real db and broker with the existing test fixtures / patterns to manage db and exchange creation and tear-down. Integration tests should not use mocks for infrastructure components except for OpenAI calls  and Embedding creation. Those may be mocked.

## Code and Comment Expectations
- Code should be self-documenting. Classes and functions should be focused, with concise but expalanatory names.
- There are several reasons to consider breaking something into one or more functions:
    - Code reuse--if the same or very similar code is / will be needed somewhere else, consider creating a function
    - Code readibility--instead of adding a comment, create a function whose name clarifies the intent (e.g. _record_exclusive_task_outcome).
- The following guidelines should be considered when determining if a new function should be added:
    - A function should be decomposed into smaller functions if it contains more than 50 lines of code (including comments)
    - A function should be elminiated if it contains less than 2 lines of code
    - If a new function will decrease readability or introduce complexity significantly consider using a class or other programming abstraction
    - If a large comment is needed to explain something, consider decomposing into a function or class where names and docstrings obviate the need for the comment
- Comments should be extremely concise and describe WHY something occurred. Do not document HOW something is done or WHAT something does in the comments.
    - Docstrings are a small exception in that they may give a very concise description of what an attribute contains, how a function should be used, or what a class represents. They should be concise and focus on aspects that are not self-evident from the name or structure of the code.
- Design trade-off and architecture decisions should not be recorded in comments. They should be recorded in the ADR of the feature spec.
- When adding new docstrings, they should generally be a single line. With rare exceptions they can extend to two lines, never more.
    - Existing docstrings in the code or longer docstrings modified by developers are fine and should not be modified unless you are specifically modifying that function/class/module/attribute. In that case, do not try to minimize the docstring to meet the guidelines.
- Inline comments should almost always be a single line with rare exceptions going to two lines.
- Comments should be minimal and infrequent. The code is authoritative and should be clean with naming standards that meet the following:
    - function names represent what the function does (e.g. clean, get_id, reserve_slot, etc.)
    - class names reflect what the class represents as a component or structure (e.g. ExclusiveTaskSlot, ClassificationGuide, Rule, etc.)
    - variable and field names reflect what the variable contains or represents. They typically do not indicate the type with the exception being cases where the type is integral to its purpose (disambiguation, etc)

## Documentation
- Documentation should be minimal with a few high-level design documents
    - Should focus on the following:
        - High level goals and guidelines
        - Why high level capabilities / functionality exist
        - Why certain constraints have been imposed (focusing on problem domain / customer reasons)
        - Caveats, limitations, and goals that impose restrictions or caveats on the system or it's design
        - High level architectural guidelines
        - Architecture Decision Record for high level architectural decisions and impact
        - Important algorithms / Intellectual Property should be outlined in pseudocode / diagrams
    - Should NOT be comprehensive
    - Should NOT describe what the code does
    - Should NOT be considered as authoritative but should be considered as cooperative with the code
        - If significant discrepancies exist they should be resolved
        - The documentation is a high-level overview
        - The code is the self-documenting implementation.
    - Should focus on high-level concepts that cannot be pulled easily from the code
- Medium-fidelity specs are useful during feature develompent but should not be maintained or referred to after feature completion (merge complete)
- General rule: well-written code IS the documentation

## General Expectations
- Never commit code to the git repository unless you are requested to do so
- Do not make changes unless the task requires it or the prompt specifically requests it.
- Do not use intitiative to "fix things" or "improve things"
- When reviewing code or documents, if there are only trivial issues or minor documentation issues just say "Looks good to me.". 
- When reviewing code or documents, keep the review to the changes made or areas of code impacted by the change. Unless specifically told to do so, do not expand scope beyond this.
- When design tradeoffs are not clear in the documentation or a decision is made that isn't intuitive and may lead to peer review confustion, add a design decision row to the Architecture Decision Record in docs/design/architecture-decision-record.md

## Project State
- This project is currently a greenfield project. Do not worry about database migrations or preserving legacy deployments.
    - The single caveat is that version controlled data used for testing, scripts, etc. must be migrated if breaking changes occur.
- If you see issues that would cause breakage if a legacy production deployment existed, add a note that you're not capturing these items as we're still in greenfield development.

## Communication Style
- Be professional
- Be concise
- Do not use filler phrases like "this is where it bites", "your instinct is right", "you are right to question", "which I should have flagged instead of", "Good challenge", etc.
    - Be direct. If you or I were wrong, just say "This was incorrect."
    - If there are options to consider, just say "Here are several options to consider."