# C# Style Conventions for Unity

*Distilled from: Use a C# style guide for clean and scalable game code (Unity 6 edition)*

---

## Naming Conventions

### Casing Rules

| Element | Casing | Example |
|---------|--------|---------|
| Local variables, parameters | camelCase | `maxHealthPoints` |
| Classes, public fields, methods, properties | PascalCase | `ExamplePlayerController` |
| Interfaces | `I` + PascalCase adjective | `IDamageable`, `IKillable` |
| Enums (singular noun) | PascalCase | `enum WeaponType` |
| Bitwise flag enums (plural) | `[Flags]` + PascalCase | `[Flags] enum AttackModes` |
| USS/UI Toolkit selectors | kebab-case (BEM) | `navbar-menu__shop-button--small` |

### Field Prefixes

Unity-scoped. These prefixes apply inside Unity assemblies only; non-Unity C# uses `_camelCase` for private fields (see `csharp-standards`). `[SerializeField]` fields are the further exception — plain `camelCase`, no prefix (see `unity-development`).

| Scope | Prefix | Example |
|-------|--------|---------|
| Private member | `m_` | `m_movementSpeed` |
| Constant | `k_` | `k_MaxItems` |
| Static | `s_` | `s_instanceCount` |

Alternative: Use `this.` keyword instead of `m_` prefix. Be consistent across codebase.

### Naming Rules

- **Booleans**: Prefix with verb — `isDead`, `hasStarted`, `canJump`
- **Methods**: Start with verb — `GetDirection`, `FindTarget`, `SetInitialPosition`
- **Bool-returning methods**: Phrase as question — `IsGameOver()`, `HasStartedTurn()`
- **Variables**: Use nouns, avoid abbreviations (except math/loops)
- **Events**: Verb phrase with tense — `OpeningDoor` (before), `DoorOpened` (after)
- **Event raisers**: Prefix with `On` — `OnDoorOpened()`
- **Don't**: Use jokes/puns, Hungarian notation, redundant names (`Player.PlayerScore` → `Player.Score`)

### Enum Rules

- Singular noun for standard enums: `enum FireMode`
- Plural for `[Flags]`: `[Flags] enum AttackModes`
- PascalCase for both name and values
- No prefix or suffix on names

---

## Code Organization

### Class Member Order

1. Fields
2. Properties
3. Events / Delegates
4. MonoBehaviour Methods (`Awake`, `Start`, `OnEnable`, `OnDisable`, `OnDestroy`)
5. Public Methods
6. Private Methods

### File Rules

- One MonoBehaviour per file; filename must match the MonoBehaviour name
- Other internal classes are permitted in the same file
- Group dependent/similar methods together
- Organize top-down like a newspaper: high-level methods first, details below

### Namespace Conventions

- PascalCase, no symbols/underscores: `MyApplication.GameFlow`
- Sub-namespaces via dot operator: `MyApplication.AI`, `MyApplication.UI`
- Mirror folder structure in namespace hierarchy

---

## Formatting

### Braces & Indentation

- Choose Allman (opening brace on new line) or K&R (same line) — be consistent
- **Never omit braces**, even for single-line statements
- Standard indent: 4 or 2 spaces (team agreement, enforce via EditorConfig)
- Indent case statements from switch; always include default case

### Spacing

- Single space after comma in arguments: `DoSomething(a, b, c)`
- Single space before flow control: `while (x == y)`, not `while(x==y)`
- Single space around operators: `if (x == y)`, not `if (x==y)`
- No space between method name and parenthesis: `DoSomething()`, not `DoSomething ()`
- Line width: 80–120 characters max

### Vertical Spacing

- Two blank lines between variable declarations and methods
- Two blank lines between classes and interfaces
- Group related methods together

### Regions

- Avoid `#region` — if your class needs regions, it's too large. Break into smaller classes.

---

## Properties & Serialization

- Expression-bodied for single-line read-only: `public int MaxHealth => m_maxHealth;`
- Auto-implemented for simple get/set: `public int Health { get; private set; }`
- Use `[SerializeField]` on private fields (better encapsulation than public)
- Use `[Range(min, max)]` for numeric Inspector fields
- Group related data in `[Serializable]` structs/classes
- Don't use redundant initializers (`= 0` on int, `= null` on reference types)

---

## Variables

- One declaration per line
- Use `var` when type is obvious from context: `var list = new List<int>();`
- Avoid `var` when ambiguous: `var result = GetItems();` — type unclear
- Favor readability: `CanScrollHorizontally` over `ScrollableX`
- Specify access modifiers consistently (either always explicit or always omit default)

---

## Methods

- Fewer arguments = better; reduce for readability and testability
- Avoid side effects — method should only do what its name says
- Don't use flag parameters to branch behavior; create separate methods instead
  - Bad: `GetAngle(bool returnRadians)`
  - Good: `GetAngleInDegrees()` and `GetAngleInRadians()`
- Avoid excessive overloading; each overload should have a distinct parameter count

---

## Comments

- **Don't comment bad code — rewrite it**
- Well-named methods/variables replace most comments
- Use `[Tooltip("...")]` on serialized fields instead of comments
- Use `/// <summary>` XML tags for public API methods
- Delete commented-out code (use source control)
- Keep TODOs current; delete ones you won't do (YAGNI)
- No journal comments, no attribution comments, no asterisk blocks
- Useful comments explain "why", not "what"

---

## Guiding Principles

- **KISS**: Keep code simple. Avoid unnecessary complexity.
- **YAGNI**: Don't build features you might need. Build what you need now.
- **DRY**: Extract repeated logic into shared methods. Don't copy-paste.
- **SRP**: Each class/method does one thing. If a class needs regions, it's too big.
- **Consistency**: Apply the same approach to similar things everywhere.
- **Don't code around problems**: Investigate root cause, don't apply band-aids.

---

## Code Smells to Flag

- Classes exceeding ~200–300 lines
- Methods with more than 3–4 parameters
- God objects doing too many things
- Duplicate/copy-pasted logic
- Enigmatic or joke naming
- Small changes requiring changes in many places (fragility)
- Code that can't be reused without dragging dependencies (immobility)
