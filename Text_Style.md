# TEXT_STYLES NOW: Tripartite Typography Architecture + Kelly Slab

**Platform:** AI-Powered Web Threat Detection & Digital Trust Intelligence  
**Design System:** Cyber Sentinel  
**Target Fonts:** Kelly Slab (Hero & Feature Headlines) • Space Grotesk (Display) • Inter (Interface) • JetBrains Mono (Technical / Code)

---

## 1. The Core Font Stack

1. **Kelly Slab (Editorial Feature Headlines)**
   * **Role:** Primary Hero headline (*"Web threat detection, with evidence."*) and Pipeline section title (*"Three parts of a website assessment"*).
   * **Character:** Architectural slab-serif with industrial proportions, lending a distinctive cyber-forensic identity.

2. **Space Grotesk (Display & Alert Headlines)**
   * **Role:** High-visibility impact headlines, threat verdict banners, trust score numbers, evaluation benchmark metrics.
   * **Character:** Geometric, modern, unmissable alert presence.

3. **Inter (Operational UI & Standard Text)**
   * **Role:** Primary application interface, navigation links, form labels, buttons, status pills, and descriptive tooltips.
   * **Character:** Neutral, clean, optimized for high optical legibility across dense dashboard screens.

4. **JetBrains Mono (Technical, Lexical & Data)**
   * **Role:** Raw Target URLs, 16 extracted lexical features, numeric derived values, SHAP attribution deltas, SSL ciphers, and HTTP headers.
   * **Character:** Zero-confusion glyphs (`0` vs `O`, `1` vs `l`), strict tabular alignment for numeric matrices.

---

## 2. Component-by-Component Typography Matrix

| Component & Page Role | Token Name | Font Family | Size & Weight | Tracking | Purpose |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Hero Main Headline** | `hero-title` | Kelly Slab | `48px–56px` | `+0.02em` | *"Web threat detection, with evidence."* |
| **Analysis Pipeline Headline** | `section-title` | Kelly Slab | `28px–32px` | `+0.02em` | *"Three parts of a website assessment"* |
| **Threat Verdict Headline** (P2) | `display-xl` | Space Grotesk | `22px` • 800 Bold | `+0.03em` (Uppercase) | Immediate threat classification (`CRITICAL THREAT — PHISHING`) |
| **Trust Score Figure** (P4) | `display-2xl` | Space Grotesk | `36px` • 800 Bold | `-0.02em` | Prominent radial gauge score (`94 / 100`) |
| **Dashboard Metric Digits** (P1) | `stat-number` | Space Grotesk | `32px` • 800 Bold | `-0.02em` | Global scan counts (`128,490`) & catch rates (`62.9%`) |
| **Raw Inspected Target URL** (P1, P2) | `mono-url` | JetBrains Mono | `13.5px` • 500 Medium | `-0.01em` | Unmistakable lexical URL display |
| **16-Feature Key Names** (P2) | `mono-feature` | JetBrains Mono | `12.5px` • 500 Medium | `0.0em` | Lexical feature identifiers (`url_entropy`, `path_length`) |
| **16-Feature Derived Values** (P2) | `mono-value` | JetBrains Mono | `13px` • 700 Bold | `0.0em` | Exact extracted figures (`4.81 bits`, `52 chars`) |
| **SHAP Impact Delta** (P2) | `mono-delta` | JetBrains Mono | `12px` • 800 Bold | `0.0em` | Model attribution numbers (`+0.42`, `-0.35`) |
| **Primary Action Button CTA** (All) | `btn-label` | Inter | `13px` • 700 Bold | `+0.01em` | High-contrast CTA labels (`Scan Target URL`, `Open scanner`) |
| **Verdict Status Badges** (All) | `badge-pill` | Inter | `11px` • 700 Bold | `+0.04em` (Uppercase) | Color-coded status tags (`SAFE`, `CRITICAL`, `ELEVATED`) |
| **HTTP Security Header Name** (P4) | `mono-header` | JetBrains Mono | `12.5px` • 600 SemiBold | `0.0em` | Precise header keys (`Strict-Transport-Security`, `CSP`) |
| **Model Benchmark Metrics** (P6) | `mono-metric` | JetBrains Mono | `13px` • 700 Bold | `0.0em` | Accuracy ($99.987\%$), Recall ($99.989\%$), ROC ($1.0000$) |

---

## 3. Tailwind CSS Drop-in Configuration

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      fontFamily: {
        kelly: ['"Kelly Slab"', 'serif'],
        display: ['"Space Grotesk"', 'system-ui', 'sans-serif'],
        ui: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'ui-monospace', 'monospace'],
      },
    },
  },
};
```
