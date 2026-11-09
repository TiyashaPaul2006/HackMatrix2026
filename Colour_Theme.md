# Cyber Sentinel Design System — COLOR_THEME NOW

**Platform:** AI-Powered Web Threat Detection & Digital Trust Intelligence  
**Design System Name:** Cyber Sentinel (Obsidian Slate & Neon Threat Spectrum)  

---

## 1. Master Color Palette Reference

| Color Name | Visual Swatch | Hex Code | RGB Value | Purpose & Assigned UI Component |
| :--- | :---: | :--- | :--- | :--- |
| **Obsidian Canvas** | `[ ■ ]` | `#080C14` | `8, 12, 20` | Base background across all 7 pages; anti-glare for continuous SOC operations |
| **Slate Surface** | `[ ■ ]` | `#0F172A` | `15, 23, 42` | Container surface: cards, 16-feature matrix tables, modal dialogs, and navigation sidebars |
| **Elevated Surface / Border** | `[ ■ ]` | `#1E293B` | `30, 41, 59` | Structural dividers: card outlines, table row dividers, secondary inputs, inactive tab borders |
| **Cyber Cyan** | `[ ■ ]` | `#06B6D4` | `6, 182, 212` | Primary CTA: "Scan Target URL" button, active navigation indicator, input focus rings |
| **Electric Blue** | `[ ■ ]` | `#3B82F6` | `59, 130, 246` | Secondary actions: metadata hyperlinks, export triggers, API connectivity status indicator |
| **Emerald Safe** | `[ ■ ]` | `#10B981` | `16, 185, 129` | Safe state: "Legitimate" verdict badge (99.98%), valid SSL badge, passing security headers |
| **Crimson Threat** | `[ ■ ]` | `#EF4444` | `239, 68, 68` | Critical alert: "Phishing" verdict card, expired SSL certificates, "Block Domain" button |
| **Warning Amber** | `[ ■ ]` | `#F59E0B` | `245, 158, 11` | Suspicious / Warning: expiring SSL (<30 days), missing HSTS/CSP, "Report Suspicious" CTA |
| **Amethyst XAI** | `[ ■ ]` | `#8B5CF6` | `139, 92, 246` | Explainable AI (SHAP): baseline attribution bar, model comparison metrics (RF vs XGBoost) |
| **Pure Slate White** | `[ ■ ]` | `#F8FAFC` | `248, 250, 252` | Primary text: main headers, verdict text, numeric metrics, high-contrast button labels (18.5:1) |
| **Cool Grey Text** | `[ ■ ]` | `#94A3B8` | `148, 163, 184` | Secondary text: 16 feature names, column headers, timestamps, helper descriptions |

---

## 2. Component-Level Color Allocations

### A. Interactive Buttons
* **Primary "Scan Target URL"**: Gradient `#06B6D4` → `#3B82F6` with `#FFFFFF` text and cyan glow on hover (`box-shadow: 0 0 16px rgba(6, 182, 212, 0.4)`).
* **Critical "Block Domain"**: Solid Crimson `#EF4444` hover to `#DC2626` with red glow.
* **Safe "Confirm Legitimate"**: Solid Emerald `#10B981` hover to `#059669`.
* **Action "Report Suspicious"**: Warning Amber `#F59E0B` hover to `#D97706`.
* **Secondary "Export JSON / CSV"**: Elevated Slate `#1E293B` with `#F8FAFC` text and `#334155` border.

### B. Threat Status & Verdict Badges
* **Legitimate Verdict**: `rgba(16, 185, 129, 0.12)` fill with `#10B981` border and `#34D399` text.
* **Phishing Verdict**: `rgba(239, 68, 68, 0.14)` fill with `#EF4444` border and `#F87171` text.
* **Heuristic Warning**: `rgba(245, 158, 11, 0.12)` fill with `#F59E0B` border and `#FBBF24` text.
* **Explainable AI (SHAP)**: `rgba(139, 92, 246, 0.12)` fill with `#7C3AED` border and `#C4B5FD` text.

### C. Explainable AI (SHAP Waterfall Bars)
* **Threat Drivers** (e.g., `path_length > 80`, `has_ip_address = 1`): Crimson Red `#EF4444` bar pushing score toward Phishing.
* **Trust Drivers** (e.g., `https_flag = 1`, `tld_popularity = high`): Emerald Green `#10B981` bar pushing score toward Legitimate.
* **Base Value Marker**: Amethyst Purple `#8B5CF6`.

### D. Digital Trust Score ($0–100$)
* **Optimal ($80–100$)**: Emerald `#10B981` radial arc.
* **Fair ($50–79$)**: Amber `#F59E0B` radial arc.
* **Critical / Dangerous ($0–49$)**: Crimson `#EF4444` radial arc.

---

## 3. Tailwind CSS Drop-in Configuration

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        cyber: {
          canvas: '#080C14',
          surface: '#0F172A',
          elevated: '#1E293B',
          hover: '#27354E',
          cyan: '#06B6D4',
          'cyan-hover': '#0891B2',
          blue: '#3B82F6',
          purple: '#8B5CF6',
        },
        threat: {
          safe: '#10B981',
          'safe-hover': '#059669',
          warning: '#F59E0B',
          'warning-hover': '#D97706',
          critical: '#EF4444',
          'critical-hover': '#DC2626',
        }
      }
    }
  }
}
```

