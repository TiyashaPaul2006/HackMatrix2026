# Cyber Sentinel Background Architecture — React Bits DotGrid

**Platform:** AI-Powered Web Threat Detection & Digital Trust Intelligence  
**Design System:** Cyber Sentinel (Obsidian Slate & Neon Threat Spectrum)  
**Target:** Dynamic Interactive Background Integration (Subtle & Soft-Blurred)

---

## 1. Global Background Engine: `<DotGrid />` (React Bits)

The entire application uses an interactive, hardware-accelerated WebGL 2.0 `<DotGrid />` component (JavaScript + CSS from React Bits). It is styled with a subtle `1.2px` hardware filter blur and reduced `65%` opacity layer so it recedes comfortably into the dark canvas without distracting from foreground operational cards and typography.

### Active Configuration:
```jsx
{/* Overall Full-App Interactive WebGL Background: React Bits DotGrid */}
<div className="fixed inset-0 pointer-events-none z-0 overflow-hidden bg-[#080C14]">
  <div className="w-full h-full scale-[1.02] filter blur-[1.2px] opacity-65">
    <DotGrid
      baseColor="#14404e"
      activeColor="#06b6d4"
      shape="square"
      dotSize={5}
      gap={15}
      proximity={180}
      strength={0.5}
      bounce={0}
      tension={0.6}
      returnDuration={1}
      shockRadius={400}
      shockStrength={6}
      swell={1}
      stretch={0.5}
      glow={0.5}
      fade={0}
      intro={true}
      clickShock={false}
      opacity={0.7}
    />
  </div>
</div>
```

---

## 2. Parameter Specification

| Prop / Filter | Value | Operational Justification |
| :--- | :--- | :--- |
| **`filter blur-[1.2px]`** | `1.2px` | Softens the sharp pixel square edges into an ambient, luminous glow. |
| **`opacity`** | `65% / 0.7` | Reduces visual contrast so forensic cards and typography remain the focal point. |
| **`scale-[1.02]`** | `102%` | Prevents edge clipping artifacts along viewport borders caused by CSS blur filters. |
| **`baseColor`** | `#14404e` | Deep cyan-tinted slate matrix that blends seamlessly into the `#080C14` Obsidian canvas. |
| **`activeColor`** | `#06b6d4` | Pure Cyber Cyan token (`#06B6D4`), matching primary telemetry highlights. |
| **`shape`** | `"square"` | Precision Cartesian forensic aesthetic, reinforcing technical SecOps design language. |
| **`dotSize`** | `5` | $5\text{px}$ dots for crisp resolution without overwhelming foreground content. |
| **`gap`** | `15` | $15\text{px}$ spacing providing a dense, structured micro-matrix grid. |
| **`proximity`** | `180` | $180\text{px}$ cursor reaction envelope for smooth, responsive cursor proximity lighting. |
| **`strength`** | `0.5` | Controlled kinetic push ensuring dots gently deflect without aggressive disorientation. |
| **`bounce`** | `0` | Zero rubber-banding for sharp, stable forensic telemetry behavior. |
| **`tension`** | `0.6` | Coupled neighbor tension for fluid elastic ripple effects across the grid. |
| **`returnDuration`** | `1` | $1\text{s}$ gentle decay back to resting state. |
| **`shockRadius`** | `400` | $400\text{px}$ propagation radius. |
| **`shockStrength`** | `6` | Defined shockwave amplitude. |
| **`swell`** | `1` | Smooth $1\times$ dot expansion while illuminated. |
| **`stretch`** | `0.5` | Dynamic motion streaks along velocity vectors. |
| **`glow`** | `0.5` | Soft neon ambient halo around active points. |
| **`intro`** | `true` | Expanding concentric ring boot animation on page initialization. |
| **`clickShock`** | `false` | Click shockwaves deactivated to preserve focus during UI interactions. |

---

## 3. File Architecture

- **Component:** [`frontend/src/components/backgrounds/DotGrid.jsx`](file:///d:/Competition/Hackmatrix/frontend/src/components/backgrounds/DotGrid.jsx)
- **Stylesheet:** [`frontend/src/components/backgrounds/DotGrid.css`](file:///d:/Competition/Hackmatrix/frontend/src/components/backgrounds/DotGrid.css)
- **Mounted in:** [`frontend/src/pages/LandingPage.jsx`](file:///d:/Competition/Hackmatrix/frontend/src/pages/LandingPage.jsx) (fixed viewport container at `z-0` behind `z-10` content layer).
