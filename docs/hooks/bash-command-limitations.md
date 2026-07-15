# Bash Command Analyzer Boundaries

The analyzer deliberately tokenizes command text without evaluating shell
expansions or running any program. Covered paths are normalized and evaluated
by the shared file-access engine. The following boundaries are intentional.

## LIMIT-VARIABLE-EXPANSION

- **Example:** `p=.env; cat $p`
- **Risk:** A protected path assembled through variables is not visible as a
  literal operand.
- **Boundary:** Parameter expansion, indirect expansion, and sourced variables
  are not evaluated because doing so would require shell execution or a full
  shell interpreter.
- **Safer alternative:** Pass an explicit sanitized fixture path, or use the
  native Read tool so its path is evaluated directly.

## LIMIT-INTERPRETER-ESCAPES

- **Example:** `python3 -c 'open(chr(46)+"env").read()'`
- **Risk:** Another interpreter can construct and access a protected path at
  runtime.
- **Boundary:** Embedded Python, Ruby, Node, Perl, and similar source is never
  executed or semantically interpreted by this hook.
- **Safer alternative:** Use a reviewed script with sanitized fixtures and
  access protected paths only through an explicit human-approved workflow.

## LIMIT-RECURSIVE-PARENT-SCAN

- **Example:** `grep -r TOKEN .`
- **Risk:** A recursive scan rooted above a protected file can read it without
  naming the protected path as an operand.
- **Boundary:** The analyzer evaluates explicit command operands; it does not
  enumerate directory descendants or predict each program's recursive walk.
- **Safer alternative:** Search an explicit source directory that excludes
  secret-bearing locations, or use the Grep tool with a narrow verified path.

## LIMIT-DYNAMIC-URLS

- **Example:** `curl "$TARGET_URL"`
- **Risk:** A URL assembled through variables, substitutions, aliases, or
  runtime program state can contain secret material that is not visible in the
  literal command text.
- **Boundary:** The analyzer checks only literal `http://` and `https://`
  operands for configured `curl` and `wget` commands. It does not expand shell
  state, execute commands, resolve DNS, follow redirects, or inspect request
  bodies. Malformed literal URL and percent-escape forms fail closed.
- **Safer alternative:** Pass an explicit reviewed `.invalid` URL without
  credentials, or use WebFetch so its literal `url` field is checked directly.

## Additional syntax boundary

Dynamic glob results, process substitution, aliases, functions, sourced shell
state, and program-specific option semantics are not expanded. Literal glob
operands such as `.e??`, quote concatenation, command substitution containing a
literal protected operand, tilde paths, traversal paths, and configured command
case variants are covered. Any new unsupported construct must be added here
with a reproduction, risk, boundary, and safer alternative before it can be
treated as an accepted product boundary.
