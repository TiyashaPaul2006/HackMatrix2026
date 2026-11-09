# HackMatrix: Workspace Rules & Implementation Guidelines

## 🎯 Rule 1: Page Simplicity & Minimalist Scope Policy

When planning, designing, or implementing any new page or component for this project, adhere strictly to the following principles:

1. **Keep Pages as Simple as Possible:**
   - Every page must have a clear, singular focus and a clean, uncluttered layout.
   - Avoid visual noise, decorative bloat, and redundant panels.

2. **Include Only What Is Expected:**
   - Implement strictly what has been explicitly requested, expected, or required for that page's core functionality.
   - Do not make speculative additions or anticipate unrequested workflows.

3. **Zero Feature Bloat:**
   - Never overload a single page with a massive amount of unnecessary, secondary, or irrelevant features.
   - If a feature is not essential to the primary objective of the page, do not include it.

4. **Purpose-Driven Components:**
   - Every element, card, or control on a page must serve an immediate, justifiable operational purpose directly tied to the page's core task.

---

## 🛡️ Rule 2: Mandatory Anti-AI-Slop Directive (Strict Reference to `AI_Slops.md`)

When implementing, designing, or planning anything new for this project's frontend (as well as backend and architecture), the agent **must necessarily avoid all forms of AI slop** and strictly refer to [`AI_Slops.md`](./AI_Slops.md) as the authoritative negative standard.

### Core Enforcement Mandates:
1. **Mandatory Cross-Check Against `AI_Slops.md`:**
   - Before drafting any frontend plan, wireframe, or component implementation, the agent must cross-check against the patterns documented in [`AI_Slops.md`](./AI_Slops.md) to guarantee none are present.

2. **Zero "Dashboard Disease" & Fake Telemetry:**
   - Never render fake circular gauges, oscillating wave charts, or speedometer widgets powered by `Math.random()` or hardcoded dummy arrays.
   - Every metric, progress bar, or number must tie directly to real data from the FastAPI inference pipeline (`POST /predict`, `POST /predict/batch`) or real system states.

3. **Zero Ghost Toggles & Phantom Buttons:**
   - Do not add speculative controls (e.g., non-functional "AI Turbo Mode", dead dropdown filters, decorative slider bars) that do not connect to real backend endpoints or state handlers.

4. **Zero Aesthetic Overkill:**
   - Eliminate gratuitous visual noise: no stacking 5 layers of glassmorphic blur, blinding neon outer glows, or heavy CPU-choking background animations that reduce contrast or degrade operational clarity.

5. **Substance Over Scale:**
   - Prefer a single, robust, cleanly coded, and fully working URL scan card over a sprawling multi-tab dashboard filled with non-functional placeholders.

---

## 🎨 Rule 3: Mandatory Design System & Specification Adherence

When building, designing, or implementing any new page, component, or part of this project, the agent **must strictly refer to and build according to the following design system specifications**:

1. **[`Colour_Theme.md`](./Colour_Theme.md):**
   - Strictly apply the defined 60-30-10 palette (`#060D1A` base, `#00E5FF` cyan signature, `#FF3B3B` phishing alert / `#00E676` safe green).
   - Use the exact CSS tokens and hex values defined for cards, borders, text, and alert stages.

2. **[`Text_Style.md`](./Text_Style.md):**
   - Strictly follow the 12-font catalog, semantic typography systems, type scale (sizes in px), font weights, line heights, and letter spacings.
   - Headings in `Orbitron` / `Outfit` / `Space Grotesk`, telemetry/URLs in `JetBrains Mono`, body copy in `Plus Jakarta Sans`, and badges in `Rajdhani` / `Chakra Petch`.

3. **[`Background.md`](./Background.md):**
   - Use the specified non-AI inertial scroll and GPU-accelerated background architectures (e.g., `PacketFlowBackground`, `ThreatContourBackground`, `CyberRadarBackground`, `ChromaticVoidBackground`) and integrate the `BackgroundController` switcher.

### 🌟 Page-Specific Rule for the Landing Page:
- While developing or planning the **Landing Page** (`/`), the file **[`Hero_Section.md`](./Hero_Section.md)** (alongside **[`Landing_Page.md`](./Landing_Page.md)**) **must also be strictly referred to and followed**, specifically implementing:
  - The 3D Interactive Cyber Threat Globe architecture with 60+ FPS Fresnel GLSL shaders.
  - The functional real-time URL Quick-Scan bar wired directly to FastAPI `POST /predict`.
  - The glassmorphic floating HUD cards with verified benchmark metrics.
