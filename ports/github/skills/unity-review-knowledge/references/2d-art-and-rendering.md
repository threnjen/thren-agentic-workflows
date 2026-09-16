# 2D Art, Rendering & Animation Review Rules

*This reference is distilled from 2D game art, animation & lighting (Unity 6/LTS) and Tips to increase productivity with Unity 6.*

---

## Sprite Setup

### Resolution & Scale

- Calculate the required PPU (pixels per unit) with `Screen Height (px) ÷ (Orthographic Camera Size × 2)`.
- Use a character height of 0.5–2 Unity units.
- Set Tilemap scale to 1 unit per tile.
- **Flag**: Sprites that use non-uniform scale on the root Transform cause physics and rendering issues.
- Paint at 2× the target resolution.
- Scale the image to 50% on export to hide imperfections.

### Sprite Editor

- Set Mesh Type to **Tight** to reduce overdraw for sprites with transparent areas.
- Use Custom Outline to create a tight mesh around opaque pixels.
- Use Custom Physics Shape for non-visual collision.
- Keep the shapes simple because each vertex has a performance cost.
- Assign normal maps and mask maps through Sprite Editor > Secondary Textures.
- **Flag**: Directly painting light or shadow on sprites while using 2D lights causes double shading.
- Use ambient occlusion only.

### Atlasing

- **Flag**: Consolidate a texture that appears in multiple sprite atlases into one atlas.
- Enable Alpha Dilation in the Sprite Atlas settings to prevent texture bleeding.
- Use Sprite Atlas for 2D projects.
- Use texture atlases and DCC (digital content creation) tools for 3D projects.

---

## 2D Lighting

### Normal Maps & Secondary Textures

- Enable Normal Maps on the `Light2D` component to use sprite normal maps.
- **Flag**: Normal maps with pre-painted directional light look flat when 2D lights illuminate them.
- Normal maps encode surface angles with R=X for the X direction, G=Y for the Y direction, and B=Z.
- Use `Sprite Custom Lit shader` to light each sprite independently.

### Performance

- Set Light > Normal Map Quality to **Fast**, not Accurate, for mobile targets.
- **Flag**: Too many shadow-casting lights cause additional render state switches.
- Use one shared `Sprites-Lit-Material` with secondary texture references.
- Do not create unique materials for each sprite.

---

## 2D Physics

- **Flag**: Use `PolygonCollider2D` instead of `MeshCollider` for 2D.
- Set `Rigidbody2D.BodyType: Static` for immovable geometry.
- **Flag**: Do not move `Rigidbody2D` through `transform.position`.
- Move the `Rigidbody2D` with `AddForce()`, `MovePosition()`, or `velocity` instead.
- Run physics in `FixedUpdate()`, never in `Update()`.
- Define the `Layer Collision Matrix` in Project Settings > Physics 2D to disable unwanted pairs.
- Use `Composite Collider 2D` with `Merge: Outline` to unify tilemap colliders.

---

## Sorting & Draw Order

- Apply sorting priority in this order: Distance to camera → Order in Layer → Sorting Layer → Material.
- Use `Sorting Group` on the parent to group multipart objects, such as characters and equipment.
- **Flag**: Too many Sorting Layers limit batching.
- Use Order in Layer instead of extra Sorting Layers.
- For isometric games, set `Transparency Sort Axis: (0, 1, 0)` for Y-axis depth sorting.
- **Flag**: Each Sorting Group with the wrong parent processes independently.

---

## Tilemap

- Use `Rule Tile` to automatically select edge and corner sprites based on neighbors.
- For Unity 6.1+, use `AutoTile` for template-based tiling without manual rules.
- **Flag**: When texture bleeds between tiles, enable Alpha Dilation and check seam settings.
- Optimize colliders with `Composite Collider 2D`, which merges individual tile colliders.

---

## Animation

### Rigging

- Design characters in a neutral pose with unbent arms and legs before rigging.
- Use 2D Inverse Kinematics for natural limb movement.
- Do not manually rotate every bone.
- Set resolution higher than the target PPU for skeletal animation because rotation pixelates at exact PPU.
- Test bone weights at joints, such as elbows and knees, with 45° alignment.

### Sprite Animation Techniques

- Use Sprite Swap from Sprite Library for facial expressions and equipment changes.
- Use PSD Importer to skip manual PNG export for each layer.
- Use Aseprite Importer to auto-generate Tilemap assets from `.aseprite` files.

### Performance

- Avoid Animator for simple tweens.
- Use DOTween or easing functions instead.
- Avoid scale curves in clips because they cost more than translation or rotation.
- Set Culling Mode to "Based on Renderers".
- Disable "Update When Offscreen".
- Use Generic rigs instead of Humanoid when possible because Humanoid uses 30–50% more CPU.
- Separate animating hierarchies.
- Do not share common parents because they create a threading bottleneck.

---

## VFX

- Use Particle System (CPU, central processing unit) for thousands of particles, full physics, and maximum compatibility.
- Use VFX Graph (GPU, graphics processing unit) for millions of particles when compute shader support is available.
- On mobile, use Particle System because most devices lack compute shaders.
- Use Camera Tiling and Frustum Culling on particles to skip off-screen work.
- Use Sprite Lit shader in VFX Graph Output for particles that react to 2D lights.

---

## Material & Shader Management

- Use `#pragma shader_feature`, not `multi_compile`, for material-specific variants.
- Unity strips unused variants.
- Create Material Variants for property tweaks.
- Do not duplicate entire materials.
- Use `Renderer.sharedMaterial`, not `Renderer.material`, to avoid creating material instances.
