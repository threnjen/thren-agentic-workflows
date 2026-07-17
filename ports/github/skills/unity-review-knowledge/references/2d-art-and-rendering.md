# 2D Art, Rendering & Animation Review Rules

*Distilled from: 2D game art, animation & lighting (Unity 6/LTS) + Tips to increase productivity with Unity 6*

---

## Sprite Setup

### Resolution & Scale

- Calculate required PPU: `Screen Height (px) ÷ (Orthographic Camera Size × 2)`
- Character height: 0.5–2 Unity units; Tilemap: 1 unit per tile
- **Flag**: Sprites scaled non-uniformly on root Transform — causes physics/rendering issues
- Paint at 2× target resolution, scale to 50% on export (hides imperfections)

### Sprite Editor

- Set Mesh Type: **Tight** to reduce overdraw on sprites with transparent areas
- Use Custom Outline for tight mesh around opaque pixels
- Use Custom Physics Shape for non-visual collision; keep shapes simple (performance cost per vertex)
- Assign normal maps AND mask maps via Sprite Editor > Secondary Textures
- **Flag**: Painting light/shadow directly on sprites when using 2D lights — use ambient occlusion only; lights will double-shade

### Atlasing

- **Flag**: Same texture in multiple sprite atlases — consolidate into one atlas
- Enable Alpha Dilation in Sprite Atlas settings to prevent texture bleeding
- Use Sprite Atlas for 2D projects; texture atlases + DCC tools for 3D

---

## 2D Lighting

### Normal Maps & Secondary Textures

- Enable Normal Maps on `Light2D` component to use sprite normal maps
- **Flag**: Normal maps with pre-painted directional light — will look flat with 2D lights
- Normal maps: R=X direction, G=Y direction, B=Z (surface angle encoding)
- Use `Sprite Custom Lit shader` for independent per-sprite lighting

### Performance

- Set Light > Normal Map Quality: **Fast** (not Accurate) for mobile targets
- **Flag**: Too many shadow-casting lights — each costs render state switches
- Use ONE shared `Sprites-Lit-Material` with secondary texture refs — don't create unique materials per sprite

---

## 2D Physics

- **Flag**: Using `MeshCollider` for 2D — use `PolygonCollider2D` instead
- Set `Rigidbody2D.BodyType: Static` for immovable geometry
- **Flag**: Moving Rigidbody2D via `transform.position` — use `AddForce()`, `MovePosition()`, or `velocity`
- Physics in `FixedUpdate()`, never `Update()`
- Define `Layer Collision Matrix` (Project Settings > Physics 2D) to disable unwanted pairs
- Use `Composite Collider 2D` with `Merge: Outline` to unify tilemap colliders

---

## Sorting & Draw Order

- Sort priority: Distance to camera → Order in Layer → Sorting Layer → Material
- Use `Sorting Group` on parent to group multi-part objects (characters, equipment)
- **Flag**: Too many Sorting Layers — use Order in Layer instead; excess layers limit batching
- Isometric games: set `Transparency Sort Axis: (0, 1, 0)` for Y-axis depth sorting
- **Flag**: Sorting Groups with wrong parent — each group processes independently

---

## Tilemap

- Use `Rule Tile` to auto-select edge/corner sprites based on neighbors
- Unity 6.1+: Use `AutoTile` for template-based tiling without manual rules
- **Flag**: Texture bleeding between tiles — enable Alpha Dilation + check seam settings
- Optimize colliders: `Composite Collider 2D` merges individual tile colliders

---

## Animation

### Rigging

- Design characters in neutral pose (unbent arms/legs) before rigging
- Use 2D Inverse Kinematics for natural limb movement — don't manually rotate every bone
- Set resolution higher than target PPU for skeletal animation (rotation pixelates at exact PPU)
- Test bone weights at joints (elbows/knees) with 45° alignment

### Sprite Animation Techniques

- Use Sprite Swap from Sprite Library for facial expressions, equipment changes
- PSD Importer: skip manual PNG export per layer
- Aseprite Importer: auto-generate Tilemap assets from `.aseprite` files

### Performance

- Avoid Animator for simple tweens — use DOTween or easing functions
- Avoid scale curves in clips (more expensive than translation/rotation)
- Set Culling Mode: "Based on Renderers" + disable "Update When Offscreen"
- Generic rigs over Humanoid when possible (Humanoid = 30–50% more CPU)
- Separate animating hierarchies — don't share common parents (threading bottleneck)

---

## VFX

- Particle System (CPU): thousands of particles, full physics, max compatibility
- VFX Graph (GPU): millions of particles, requires compute shader support
- Mobile: most devices lack compute shaders — use Particle System
- Use Camera Tiling + Frustum Culling on particles to skip off-screen work
- Use Sprite Lit shader in VFX Graph Output for particles that react to 2D lights

---

## Material & Shader Management

- Use `#pragma shader_feature` (not `multi_compile`) for material-specific variants — unused get stripped
- Create Material Variants for property tweaks — don't duplicate entire materials
- Use `Renderer.sharedMaterial`, NOT `Renderer.material` (avoids creating material instances)
