# Architecture & Design Patterns for Unity

*Distilled from: Modular game architecture with ScriptableObjects (Unity 6) + Level up your code with design patterns and SOLID (Unity 6 edition)*

---

## SOLID Principles

### Single Responsibility (SRP)

- Each class has one reason to change
- Split classes that exceed 200–300 lines
- Do not mix data with logic in the same class
- Do not assign multiple responsibilities to one MonoBehaviour. Decompose it:
  - Bad: `Player` handles input, movement, audio, health
  - Good: `PlayerInput`, `PlayerMovement`, `PlayerAudio`, `PlayerHealth` with `[RequireComponent]`

### Open-Closed (OCP)

- Classes must be open for extension and closed for modification
- **Flag**: Long switch/if chains used for type checking. Use polymorphism instead
- Use abstract base classes and interfaces. Add each new type as a subclass instead of editing existing code

### Liskov Substitution (LSP)

- Derived classes must be substitutable for their base class
- **Flag**: `NotImplementedException` in overrides and methods that do nothing in subclasses
- Prefer composition over inheritance. Favor interfaces over deep class hierarchies

### Interface Segregation (ISP)

- No client should depend on methods it does not use
- Keep interfaces small and focused: `IMovable`, `IDamageable`, `IExplodable` — not `IUnitStats`
- Unity cannot serialize fields of interface type directly. Cast a serialized `MonoBehaviour` field:
  ```csharp
  [SerializeField] private MonoBehaviour interactableObject;
  if (interactableObject is IInteractable interactable) interactable.Interact();
  ```

### Dependency Inversion (DIP)

- High-level modules depend on abstractions, not concrete implementations
- **Flag**: Direct concrete references between unrelated systems
- In this pattern, `Switch` depends on `ISwitchable`, not `Door`. This design works with any switchable object

---

## ScriptableObject Patterns

### When to Use ScriptableObjects

**Use for:**
- Static or shared configuration data, such as enemy stats, item definitions, and audio collections
- Data that needs Editor access without GameObject overhead
- Shared references to reduce duplicate data with the flyweight pattern
- Event channels for decoupled communication

**Do not use for:**
- Data that persists between sessions. Use JSON/XML/MessagePack instead
- Real-time mutable game state. Use MonoBehaviours instead
- Scene-specific objects that need a Transform

### Key Differences from MonoBehaviour

- ScriptableObjects have no `Update`/`Start` methods and support only limited callbacks: `Awake`, `OnEnable`, `OnDisable`, `OnDestroy`, and `OnValidate` (Editor only)
- ScriptableObject data persists in Editor after Play mode and can cause stale state bugs
- Methods require explicit calls from a MonoBehaviour. The player loop does not invoke them automatically

### Cleanup Rule

Set references to null before calling Destroy:
```csharp
mySOReference = null;  // Do this BEFORE Destroy
Destroy(scriptableObjectInstance);
```

### Data Container Pattern

- Store shared configuration in SOs and reference it from MonoBehaviours
- Keep instance-specific state on a MonoBehaviour and shared data on an SO
- Reduce memory use by sharing one reference instead of duplicating data per instance

### Dual Serialization

- Use ScriptableObjects at edit time because they are convenient in Editor
- Use JSON/XML for runtime persistence (player-accessible and moddable)
- Use `JsonUtility.FromJsonOverwrite()` to populate SOs from a file

### Extendable Enums

- Use empty or data-rich SOs as type identifiers instead of C# enums
- These SOs avoid reorder bugs. Designers can extend them without recompiling
- Compare values by reference equality: `if (itemA == itemB)`

### Delegate Objects (Strategy Pattern)

- Put behavior in SOs, not only data:
  ```csharp
  public abstract class EnemyAI : ScriptableObject
  {
      public abstract void MoveUnit(EnemyUnit unit);
  }
  ```
- Swap behavior at runtime by reassigning the SO reference
- The open-closed principle lets you add new AI without changing consuming code

### Event Channels (Observer via SOs)

- ScriptableObject-based events enable fully decoupled communication
- This approach avoids singletons and direct references between systems
- **Critical**: Always unsubscribe in `OnDisable`/`OnDestroy` to prevent leaks
- Create typed variants: `VoidEventChannelSO`, `IntEventChannelSO`, etc.
- Add Inspector buttons to manually raise events for debugging

### Runtime Sets

- Use an SO that maintains a `List<T>` of active objects and replaces `FindObjectOfType`
- Objects add themselves in `OnEnable` and remove themselves in `OnDisable`
- Runtime sets are faster than scene searches, designer-friendly, and easily extensible
- Limitation: Runtime sets do not serialize scene references in the Inspector. Use `[HideInInspector]` or a public property

---

## Design Patterns

### Factory Pattern

- Encapsulate object creation with initialization logic
- Use factories when spawning enemies, items, or projectiles with setup requirements
- Combine factories with an object pool for performance
- Use a dictionary lookup by ID for runtime type selection

### Object Pool Pattern

- Pre-allocate and reuse frequently created and destroyed objects
- Use the built-in `UnityEngine.Pool` namespace (Unity 2021+)
- Configure `ObjectPool<T>` with create/get/release/destroy callbacks
- Set `collectionCheck = true` to catch double-returns in Editor
- Initialize pools during loading screens
- Set maximum size to prevent unbounded growth

### Singleton Pattern

**Use sparingly.** Singletons break SOLID, introduce global state, and harm testability.

- Singletons are acceptable for single-instance managers (audio, game state) when alternatives are impractical
- Always prefer alternatives first: SO event channels, Runtime Sets, dependency injection
- If you use a singleton, call `DontDestroyOnLoad` and remove duplicates in `Awake()`
- **Flag**: More than 2–3 singletons in a project — indicates coupling problem

### Command Pattern

- Encapsulate actions as objects with `Execute()` and `Undo()`
- Use commands for undo/redo, action queues, turn-based games, and replay systems
- Maintain undo/redo stacks. Clear the redo stack when you issue a new command
- Consider history size limits for memory management

### State Pattern

- Encapsulate state-specific behavior in separate state objects
- Each state has `Enter()`, `Execute()`, `Exit()`
- Use states for character locomotion, game states, and AI behavior
- Combine the pattern with Animator. Map each state to AnimatorState
- For advanced behavior, use hierarchical states with a SuperState and sub-states

### Observer Pattern

- Decouple systems through publish-subscribe
- A publisher fires an event and does not know its subscribers
- **Critical**: Unsubscribe in `OnDisable()` to prevent memory leaks and null reference errors
- Use this naming: `event Action<int> DamageReceived` (publisher) and `OnDamageReceived(int amount)` (handler)
- For communication across scenes and systems, use SO event channels instead of direct subscriptions

### MVC / MVP

- **Model**: Contains data and logic in pure C# or a ScriptableObject
- **View**: Provides visual presentation through MonoBehaviour/UI
- **Controller/Presenter**: Mediates between the Model and the View
- This separation makes the Model testable without Unity and the View swappable
- Use events to decouple Model→View notifications

---

## Anti-Patterns to Flag

| Anti-Pattern | Why It's Bad | Alternative |
|---|---|---|
| God object / manager class | Handles too much and becomes hard to test or modify | Split by responsibility |
| Singleton for everything | Creates global state and hidden dependencies | SO events, Runtime Sets, DI |
| Deep inheritance hierarchy | Creates fragile code and LSP violations | Composition and interfaces |
| Direct cross-system references | Create tight coupling | Events, SO channels, interfaces |
| Switch on type | Violates OCP because extension requires modification | Polymorphism |
| Public fields everywhere | Exposes fields without encapsulation | `[SerializeField]` private fields and a public property |
| `FindObjectOfType` in gameplay | Runs a slow scene search on every call | Cache a reference, Runtime Sets |
| `GetComponent` in Update | Adds per-frame allocation overhead | Cache in Awake/Start |
