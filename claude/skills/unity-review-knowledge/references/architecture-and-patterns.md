# Architecture & Design Patterns for Unity

*Distilled from: Modular game architecture with ScriptableObjects (Unity 6) + Level up your code with design patterns and SOLID (Unity 6 edition)*

---

## SOLID Principles

### Single Responsibility (SRP)

- Each class has one reason to change
- Classes exceeding 200–300 lines should be split
- Don't mix data with logic in the same class
- Don't pile multiple responsibilities into one MonoBehaviour — decompose:
  - Bad: `Player` handles input, movement, audio, health
  - Good: `PlayerInput`, `PlayerMovement`, `PlayerAudio`, `PlayerHealth` with `[RequireComponent]`

### Open-Closed (OCP)

- Classes must be open for extension, closed for modification
- **Flag**: Long switch/if chains for type checking — use polymorphism instead
- Use abstract base classes + interfaces: adding a new type = new subclass, not editing existing code

### Liskov Substitution (LSP)

- Derived classes must be substitutable for their base class
- **Flag**: `NotImplementedException` in overrides, methods that do nothing in subclasses
- Prefer composition over inheritance; favor interfaces over deep class hierarchies

### Interface Segregation (ISP)

- No client should depend on methods it doesn't use
- Keep interfaces small and focused: `IMovable`, `IDamageable`, `IExplodable` — not `IUnitStats`
- Unity serialization note: Unity can't serialize interface-type fields directly. Cast from serialized `MonoBehaviour` field:
  ```csharp
  [SerializeField] private MonoBehaviour interactableObject;
  if (interactableObject is IInteractable interactable) interactable.Interact();
  ```

### Dependency Inversion (DIP)

- High-level modules depend on abstractions, not concrete implementations
- **Flag**: Direct concrete references between unrelated systems
- Pattern: `Switch` depends on `ISwitchable`, not `Door` — works with any switchable object

---

## ScriptableObject Patterns

### When to Use ScriptableObjects

**Use for:**
- Static/shared config data (enemy stats, item definitions, audio collections)
- Data that needs Editor access without GameObject overhead
- Reducing duplicate data via shared references (flyweight pattern)
- Event channels for decoupled communication

**Don't use for:**
- Data that persists between sessions (use JSON/XML/MessagePack)
- Real-time mutable game state (use MonoBehaviours)
- Scene-specific objects needing Transform

### Key Differences from MonoBehaviour

- No `Update`/`Start` — limited callbacks: `Awake`, `OnEnable`, `OnDisable`, `OnDestroy`, `OnValidate` (Editor only)
- Data persists in Editor after Play mode (can cause stale state bugs)
- Methods must be called explicitly from a MonoBehaviour — no player loop auto-invocation

### Cleanup Rule

Null references before Destroy:
```csharp
mySOReference = null;  // Do this BEFORE Destroy
Destroy(scriptableObjectInstance);
```

### Data Container Pattern

- Store shared config in SOs; reference from MonoBehaviours
- Instance-specific state stays on MonoBehaviour, shared data on SO
- Reduces memory (shared reference vs duplicated data per instance)

### Dual Serialization

- Edit time: ScriptableObjects (convenient in Editor)
- Runtime persistence: JSON/XML (player-accessible, moddable)
- Use `JsonUtility.FromJsonOverwrite()` to populate SOs from file

### Extendable Enums

- Use empty or data-rich SOs as type identifiers instead of C# enums
- Advantages: no reorder bugs, designer-extensible, no recompilation to add values
- Compare via reference equality: `if (itemA == itemB)`

### Delegate Objects (Strategy Pattern)

- Put behavior in SOs, not just data:
  ```csharp
  public abstract class EnemyAI : ScriptableObject
  {
      public abstract void MoveUnit(EnemyUnit unit);
  }
  ```
- Swap behavior at runtime by reassigning SO reference
- Open-closed: add new AI without touching consuming code

### Event Channels (Observer via SOs)

- ScriptableObject-based events for fully decoupled communication
- Avoids singletons and direct references between systems
- **Critical**: Always unsubscribe in `OnDisable`/`OnDestroy` to prevent leaks
- Create typed variants: `VoidEventChannelSO`, `IntEventChannelSO`, etc.
- Add Inspector buttons to manually raise events for debugging

### Runtime Sets

- SO that maintains a `List<T>` of active objects (replaces `FindObjectOfType`)
- Objects add themselves in `OnEnable`, remove in `OnDisable`
- Faster than scene search; designer-friendly; easily extensible
- Limitation: Won't serialize scene references in Inspector — use `[HideInInspector]` or public property

---

## Design Patterns

### Factory Pattern

- Encapsulate object creation with initialization logic
- Use when: spawning enemies/items/projectiles with setup requirements
- Combine with object pool for performance
- Dictionary lookup by ID for runtime type selection

### Object Pool Pattern

- Pre-allocate and reuse frequently created/destroyed objects
- Use built-in `UnityEngine.Pool` namespace (Unity 2021+)
- `ObjectPool<T>` with create/get/release/destroy callbacks
- Set `collectionCheck = true` to catch double-returns in Editor
- Initialize pools during loading screens
- Set maximum size to prevent unbounded growth

### Singleton Pattern

**Use sparingly.** Singletons break SOLID, introduce global state, and harm testability.

- Acceptable for: single-instance managers (audio, game state) where alternatives are impractical
- Always prefer alternatives first: SO event channels, Runtime Sets, dependency injection
- If used: DontDestroyOnLoad + duplicate removal in `Awake()`
- **Flag**: More than 2–3 singletons in a project — indicates coupling problem

### Command Pattern

- Encapsulate actions as objects with `Execute()` and `Undo()`
- Use for: undo/redo, action queues, turn-based games, replay systems
- Maintain undo/redo stacks; clear redo on new command
- Consider history size limits for memory management

### State Pattern

- Encapsulate state-specific behavior in separate state objects
- Each state has `Enter()`, `Execute()`, `Exit()`
- Use for: character locomotion, game states, AI behavior
- Combine with Animator: each state maps to AnimatorState
- Advanced: hierarchical states (SuperState with sub-states)

### Observer Pattern

- Decouple via publish-subscribe
- Publisher fires event, doesn't know subscribers
- **Critical**: Unsubscribe in `OnDisable()` to prevent memory leaks and null reference errors
- Naming: `event Action<int> DamageReceived` (publisher), `OnDamageReceived(int amount)` (handler)
- For cross-scene/system communication: use SO event channels instead of direct subscription

### MVC / MVP

- **Model**: Data + logic (pure C# or ScriptableObject)
- **View**: Visual presentation (MonoBehaviour/UI)
- **Controller/Presenter**: Mediates between Model and View
- Benefit: Model is testable without Unity; View is swappable
- Use events to decouple Model→View notifications

---

## Anti-Patterns to Flag

| Anti-Pattern | Why It's Bad | Alternative |
|---|---|---|
| God object / manager class | Does too much, hard to test/modify | Split by responsibility |
| Singleton for everything | Global state, hidden dependencies | SO events, Runtime Sets, DI |
| Deep inheritance hierarchy | Fragile, LSP violations | Composition + interfaces |
| Direct cross-system references | Tight coupling | Events, SO channels, interfaces |
| Switch on type | OCP violation — must modify to extend | Polymorphism |
| Public fields everywhere | No encapsulation | `[SerializeField]` private + public property |
| `FindObjectOfType` in gameplay | Slow scene search every call | Cache reference, Runtime Sets |
| `GetComponent` in Update | Per-frame allocation overhead | Cache in Awake/Start |
