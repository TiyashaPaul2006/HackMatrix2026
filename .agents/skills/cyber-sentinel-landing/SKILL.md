---
name: cyber-sentinel-landing
description: Design, implementation, and maintenance guide for the Cyber Sentinel Landing Page, ensuring exact pixel-perfect adherence to the Obsidian Slate & Neon Threat Spectrum design system.
---

# Cyber Sentinel Landing Page Skill

This skill defines the exact component architecture, visual styling, typography, and API integrations for the Cyber Sentinel Landing Page (`/`).

## 1. Visual Identity & Palette Tokens
- **Canvas Base:** `#080C14` (Obsidian Canvas)
- **Card Surface:** `#0B111E` / `#0F172A` (Slate Surface)
- **Dividers & Borders:** `#1E293B` / `#334155`
- **Primary CTA & Focus:** `#06B6D4` (Cyber Cyan)
- **Secondary CTA & Links:** `#3B82F6` (Electric Blue)
- **Verdict Safe:** `#10B981` (Emerald)
- **Verdict Threat:** `#EF4444` (Crimson)
- **Warning Amber:** `#F59E0B`
- **Text:** `#F8FAFC` (Pure Slate White) and `#94A3B8` (Cool Grey)

## 2. Typography Rules
- **Space Grotesk:** Display headlines, big metric digits (`99.9868%`), and card titles.
- **Inter:** Body copy, subtitles, navigation links, and button labels.
- **JetBrains Mono:** URLs, feature keys, `URI` badge, confusion matrix values, and technical metadata.

## 3. Structural Sections
1. **Fixed Header:** 64px, shield logo, `CYBER SENTINEL`, nav (`Scanner`, `How it works`, `Evaluation`), `API reference`, and `Open scanner ↗` button.
2. **Hero:** Eyebrow `● URL THREAT ANALYSIS / XGBOOST + SHAP`, headline `"Web threat detection, with evidence."`, subtitle, 56px command bar with `URI` badge and `Scan target URL →` button, quick demo pills (`google.com`, `192.168.1.1`, `godaddysites.com`), and 3-point telemetry strip (`XGBoost`, `16 engineered features`, `SHAP TreeExplainer`).
3. **Analysis Pipeline:** Eyebrow `ANALYSIS PIPELINE`, title `"Three parts of a website assessment"`, 3 cards (`01 / CLASSIFY`, `02 / EXPLAIN`, `03 / ASSESS`).
4. **Recorded Model Results:** Large benchmark card with title `"Evaluation, not marketing claims."`, `100,872 CLEANED URL RECORDS`, 4 metric blocks (`99.9868%`, `99.9895%`, `0.9999995`, `15,131`), confusion matrix strip (`TN: 5,606`, `FP: 1`, `FN: 1`, `TP: 9,523`), and amber validation note.
5. **Footer:** Brand mission, `EXPLORE` links, `DEVELOPER` links, copyright, and `OBSIDIAN SLATE / NEON THREAT SPECTRUM` tagline.

