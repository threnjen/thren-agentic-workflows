# C# Style Conventions for Unity

*This reference is distilled from: Use a C# style guide for clean and scalable game code (Unity 6 edition)*

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

These prefixes apply only inside Unity assemblies. Non-Unity C# uses `_camelCase` for private fields (see `csharp-standards`). `[SerializeField]` fields are an exception. Use plain `camelCase` without a prefix (see `unity-development`).

| Scope | Prefix | Example |
|-------|--------|---------|
| Private member | `m_` | `m_movementSpeed` |
| Constant | `k_` | `k_MaxItems` |
| Static | `s_` | `s_instanceCount` |

Use the `this.` keyword instead of the `m_` prefix as an alternative. Keep the same convention across the codebase.

### Naming Rules

- **Booleans**: Prefix boolean names with a verb: `isDead`, `hasStarted`, `canJump`
- **Methods**: Start method names with a verb: `GetDirection`, `FindTarget`, `SetInitialPosition`
- **Bool-returning methods**: Phrase methods that return bool as questions: `IsGameOver()`, `HasStartedTurn()`
- **Variables**: Use nouns for variable names. Avoid abbreviations except in math and loops.
- **Events**: Name events with a verb phrase and tense: `OpeningDoor` (before), `DoorOpened` (after)
- **Event raisers**: Prefix event raisers with `On`: `OnDoorOpened()`
- **Do not**: Use jokes or puns, Hungarian notation, or redundant names (`Player.PlayerScore` → `Player.Score`)

### Enum Rules

- Use a singular noun for standard enum names: `enum FireMode`
- Use a plural noun for `[Flags]` enum names: `[Flags] enum AttackModes`
- Use PascalCase for enum names and values.
- Do not add a prefix or suffix to enum names.

---

## Code Organization

### Class Member Order

1. Place fields first.
2. Place properties second.
3. Place events and delegates third.
4. Place MonoBehaviour methods (`Awake`, `Start`, `OnEnable`, `OnDisable`, `OnDestroy`) fourth.
5. Place public methods fifth.
6. Place private methods sixth.

### File Rules

- Keep one MonoBehaviour in each file. Match the filename to the MonoBehaviour name.
- You may place other internal classes in the same file.
- Group dependent or similar methods together.
- Organize methods from high-level to detailed, like a newspaper.

### Namespace Conventions

- Use PascalCase for namespaces. Do not use symbols or underscores: `MyApplication.GameFlow`
- Use dot-separated sub-namespaces: `MyApplication.AI`, `MyApplication.UI`
- Mirror the folder structure in the namespace hierarchy.

---

## Formatting

### Braces & Indentation

- Choose Allman (opening brace on new line) or K&R (same line).
- Keep the brace style consistent.
- **Never omit braces**, even for single-line statements.
- Use four or two spaces for standard indentation, based on the team agreement. Enforce the choice through EditorConfig.
- Indent case statements from `switch`. Always include a default case.

### Spacing

- Use a single space after commas in arguments: `DoSomething(a, b, c)`
- Use a single space before flow-control parentheses: `while (x == y)`, not `while(x==y)`
- Use a single space around operators: `if (x == y)`, not `if (x==y)`
- Do not add a space between a method name and its parenthesis: `DoSomething()`, not `DoSomething ()`
- Limit line width to 80–120 characters.

### Vertical Spacing

- Leave two blank lines between variable declarations and methods.
- Leave two blank lines between classes and interfaces.
- Group related methods together.

### Regions

- Avoid `#region`. If your class needs regions, the class is too large. Break it into smaller classes.

---

## Properties & Serialization

- Use expression-bodied syntax for single-line read-only members: `public int MaxHealth => m_maxHealth;`
- Use auto-implemented properties for simple get/set members: `public int Health { get; private set; }`
- Use `[SerializeField]` on private fields because it provides better encapsulation than public fields.
- Use `[Range(min, max)]` for numeric Inspector fields.
- Group related data in `[Serializable]` structs or classes.
- Do not use redundant initializers, such as `= 0` on int or `= null` on reference types.

---

## Variables

- Write one declaration per line.
- Use `var` when the type is obvious from context: `var list = new List<int>();`
- Do not use `var` when the type is unclear from context: `var result = GetItems();`
- Favor readability by using `CanScrollHorizontally` instead of `ScrollableX`.
- Specify access modifiers consistently. Always write them, or always omit default access modifiers.

---

## Methods

- Keep argument counts low to improve readability and testability.
- Avoid side effects. Make each method do only what its name says.
- Do not use flag parameters to branch behavior. Create separate methods instead.
  - Bad: `GetAngle(bool returnRadians)`
  - Good: `GetAngleInDegrees()` and `GetAngleInRadians()`
- Avoid excessive overloading. Give each overload a distinct parameter count.

---

## Comments

- **Do not comment bad code. Rewrite it.**
- Well-named methods and variables replace most comments.
- Use `[Tooltip("...")]` on serialized fields instead of comments.
- Use `/// <summary>` XML tags for public API methods.
- Delete commented-out code. Use source control.
- Keep TODOs current. Delete TODOs that you will not complete (YAGNI).
- Do not use journal comments, attribution comments, or asterisk blocks.
- Useful comments explain "why", not "what".

---

## Guiding Principles

- **KISS**: Keep code simple. Avoid unnecessary complexity.
- **YAGNI**: Do not build features you might need. Build what you need now.
- **DRY**: Extract repeated logic into shared methods. Do not copy-paste.
- **SRP**: Make each class or method do one thing. If a class needs regions, the class is too big.
- **Consistency**: Apply the same approach to similar things everywhere.
- **Do not code around problems**: Investigate the root cause. Do not apply band-aids.

---

## Code Smells to Flag

- Flag classes that exceed approximately 200–300 lines.
- Flag methods with more than 3–4 parameters.
- Flag god objects that perform too many tasks.
- Flag duplicate or copy-pasted logic.
- Flag enigmatic or joke names.
- Flag small changes that require changes in many places (fragility).
- Flag code that cannot be reused without dragging dependencies (immobility).
