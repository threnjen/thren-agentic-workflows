## Python Style

*When to referrence*: When writing new modules, creating new classes, or unfamiliar with project conventions.

### Logging
- Use Python's `logging` module for all output
- Never use `print()` statements
- Configure logging at application startup

### Configuration
- All configurable variables belong in a `config.py`
- No magic strings or hardcoded values in business logic
- Group related constants together
- Read environment variables in config file
- Provide sensible environment variable defaults where appropriate
- Validate required variables early

### Style
- Always prefer object-oriented programming
- Prefer classes over standalone functions for related functionality
- Use meaningful class names that describe their purpose
- Encapsulate related methods and state within classes

### Variables
- Do not use global variables

### Caching
- Use `~lru_cache` for expensive or repeated lookups
- Set appropriate maxsize based on expected usage
- Only use with hashable arguments

### Exception Handling
- Catch specific exceptions, not bare `except:`
- Custom exceptions end with `Error`
- Log errors with appropriate level
- Include context in error messages

### Naming
- `lower_with_under` for modules/functions/variables
- `CapWords` for classes
- `CAPS_WITH_UNDER` for constants
- `_prefix` for internal/private

### Imports
- One per line, sorted lexicographically
- Order: stdlib → third-party → local
- Full paths only, no relative imports
- Imports at the top of the file

### Type Annotations
- Required for public APIs
- Use `X | None` not `Optional[X]`
- Prefer `collections.abc` types for parameters
- Use `typing` module for complext types

### Docstrings
- Triple double quotes, summary ≤80 chars
- Include `Args:`, `Returns:`, `Raises:` sections

### Defaults
- Never mutable defaults (`[]`, `{}`)
- Use `None` with check: `if x is None: x = []`

### Functions
- Small and focused (~40 lines max)
- Avoid metaclasses, `__del__`, import hacks

## Communication

- No preamble/postamble unless requested
- No code comments unless asked
- No explanations for refusals
- Use ripgrep (`rg`) not `grep`/`find`
- Use Read/LS tools not `cat`/`head`/`tail`/`ls`
- Never guess URLs
