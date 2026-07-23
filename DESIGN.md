# Design System Specification: Kinetic Enterprise

This document specifies the design system and guidelines extracted from the **Smart Multi-Agent Ticketing System** (Stitch project `projects/1931970269353763529`). It is engineered for high-stakes enterprise environments prioritizing data density, automated status tracking, and clear UI state visual cues.

---

## 1. Brand Identity & Strategy

* **Brand Personality:** Precise, Intelligent, Vigilant.
* **Design Philosophy:** Corporate Modern with a Minimalist focus. Maximize data density while ensuring clean readability on mobile screens.
* **Visual Anchors:** 
  * Tonal layering and low-contrast borders (1px) instead of heavy shadows.
  * Structural layouts with strict alignment.
  * Clear visual differentiation for automated actions/AI pipelines.

---

## 2. Color Palette

The color scheme is designed for high-density light-mode screens. Below is the breakdown of colors and their intended semantic use.

### Brand & Core Colors
| Token | HEX Value | Description |
| :--- | :--- | :--- |
| **Primary (Action Blue)** | `#004AC6` | Primary buttons, active states, and core interactive boundaries. |
| **Primary Container** | `#2563EB` | Active highlights, selections, and focus indicators. |
| **Secondary (Indigo)** | `#4648D4` | Secondary interactive items and neutral action borders. |
| **Secondary Container** | `#6063EE` | Muted background highlights for secondary info blocks. |
| **AI/Agent Pipeline (Purple)** | `#8B5CF6` | Automated agent processes, bot replies, and trigger events. |

### Neutrals & Backgrounds
| Token | HEX Value | Description |
| :--- | :--- | :--- |
| **Background / Surface** | `#F7F9FB` | Main viewport canvas backdrops. |
| **Surface Dim** | `#D8DADC` | Used for divider lines and deactivated backgrounds. |
| **Surface Container Lowest**| `#FFFFFF` | Core ticket card backgrounds, input containers, and sheet overlays. |
| **Surface Container Low** | `#F2F4F6` | Secondary panel backgrounds. |
| **Surface Container** | `#ECEEF0` | Standard component backing / tab bar backgrounds. |
| **Surface Container High** | `#E6E8EA` | Active hover states on tables/lists. |
| **Surface Container Highest**| `#E0E3E5` | Deep outline focus frames. |
| **On Surface** | `#191C1E` | High-contrast body text and labels. |
| **On Surface Variant** | `#434655` | Secondary text, captions, and muted labels. |
| **Outline** | `#737686` | Standard structural borders. |
| **Outline Variant** | `#C3C6D7` | Muted grid lines. |

### Semantic / Feedback Colors
| Token | HEX Value | Description |
| :--- | :--- | :--- |
| **Success (Resolved)** | `#2E7D32` (Green) | Successful completion of tasks, healthy SLA status. |
| **Warning (In-Progress)**| `#EF6C00` (Amber) | Active attention required, pending external feedback. |
| **Error (Escalated/Breach)**| `#BA1A1A` | Critical SLA breaches, system errors, urgent failures. |

---

## 3. Typography

The design system utilizes the **Geist** font family for technical precision, compact width, and excellent legibility under high information density.

| Style Name | Font Family | Size | Weight | Line Height | Letter Spacing | Usage |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **headline-lg** | Geist | 24px | 600 (SemiBold) | 32px | `-0.02em` | Page Titles, Key Metrics |
| **headline-md** | Geist | 20px | 600 (SemiBold) | 28px | `-0.01em` | Section Headers, Modal Titles |
| **headline-sm** | Geist | 16px | 600 (SemiBold) | 24px | Default | Card Headings |
| **body-lg** | Geist | 16px | 400 (Regular) | 24px | Default | Long-form reading, descriptions |
| **body-md** | Geist | 14px | 400 (Regular) | 20px | Default | Default table content, logs |
| **body-sm** | Geist | 13px | 400 (Regular) | 18px | Default | Micro-copies, secondary metadata |
| **label-md** | Geist | 12px | 500 (Medium) | 16px | `0.02em` | Column Headers, Tag Labels |
| **label-sm** | Geist | 11px | 600 (SemiBold) | 14px | `0.05em` | Pill Badges, Status labels |
| **mono-ticket** | Geist / Mono | 13px | 500 (Medium) | 18px | `0.01em` | Ticket IDs, code elements |

---

## 4. Spacing & Layout

All dimensions are built on an **8px base grid** to ensure consistency across responsive break-points.

* **Safe Margins:** 16px (1rem) on all outer screen margins for mobile viewports.
* **Component Stacking:** 12px (0.75rem) vertical gap between list cards.
* **Internal Padding:** 
  * X-axis: 16px (1rem)
  * Y-axis: 12px (0.75rem)
* **Bottom Navigation:** Fixed bottom bar for primary navigation (Queue, Dashboard, Settings). Must respect platform safe-area insets.

---

## 5. Shape & Elevation Rules

To maintain the technical and precise aesthetic:
* **Borders over Shadows:** Use `1px` solid borders (typically using `#E2E8F0` or `#C3C6D7`) to define components. Avoid heavy drop-shadows.
* **Border Radii:**
  * Cards, Inputs, & Containers: `4px` (`0.25rem`) for a sharp, high-performance feel.
  * Buttons: `6px` (`0.375rem`) for a slightly softer tactile feel.
  * Status Badges & Tags: Fully rounded (`9999px` / pill-shaped) to instantly stand out from cards and buttons.
* **Active States:** When a card is selected or active, apply a subtle Indigo-tinted shadow (`#6366F1` at low opacity) to visually elevate it.
* **Backdrop Blur:** Modals and bottom sheets use a `10px` backdrop blur (`backdrop-filter: blur(10px)`) combined with a dark semi-transparent fill to isolate focus while maintaining interface context.

---

## 6. Components Best Practices

1. **Ticket Cards:**
   * Feature the Ticket ID (`mono-ticket` style) in the top-left.
   * Priority indicators must be represented as a colored left border stripe (Red for Escalated, Amber for In-Progress, Green for Resolved).
   * Include the AI pipeline badge (Purple icon/label) if handled by an AI Agent.
2. **Timeline (Agent Pipeline Tracing):**
   * Use vertical dotted indicator lines connecting chronological events.
   * Each event must include a timestamp and status icon showing the owner (AI Agent vs. Human).
3. **Data Visualization:**
   * Mini-sparklines for live volume checking and progress metrics.
   * Compact circular progress gauges for SLA percentage tracking.
