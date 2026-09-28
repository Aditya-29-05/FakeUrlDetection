# PhishGuard — Animated Cybersecurity Framework

## 1. Objective

Upgrade the existing PhishGuard website with a premium, modern, animated cybersecurity visual framework.

The animation should make the website feel like a professional AI/cybersecurity product rather than a basic dashboard.

### Critical Requirement

**DO NOT ADD SAMPLE DATA.**

The website must not contain:

* Sample URLs
* Demo scan results
* Fake scan history
* Fake prediction results
* Fake confidence values
* Fake statistics
* Hardcoded SAFE/PHISHING results
* Randomly generated prediction results
* Fake users
* Fake analytics

All application data must continue to come from:

1. Actual user input
2. Actual ML prediction
3. Actual backend API
4. Actual MongoDB data

The animation is purely visual and must never generate or modify application data.

---

# 2. Existing Application Must Be Preserved

Before making changes:

1. Inspect the existing project.
2. Understand the current React structure.
3. Understand the current API integration.
4. Understand how URL prediction currently works.
5. Do not rewrite working functionality unnecessarily.

The existing architecture must remain:

```text
React Frontend
      ↓
FastAPI Backend
      ↓
Feature Extraction
      ↓
ML Model
      ↓
Prediction
      ↓
MongoDB History
```

The animation must be added around the existing application.

Do NOT move ML logic into React.

---

# 3. Main Visual Concept

Create a:

# Cybersecurity Network Framework

The framework should look like a dynamic digital security network.

Visual elements:

* Moving grid
* Floating nodes
* Connecting lines
* Small particles
* Data-flow particles
* Subtle scanning waves
* Network pulses
* Depth/parallax effect
* Smooth transitions

The animation should visually communicate:

```text
URL
 ↓
Analysis
 ↓
Feature Extraction
 ↓
Machine Learning
 ↓
Security Result
```

without displaying fake processing data.

---

# 4. Recommended Technology

Use the simplest technology that integrates well with the existing project.

Preferred:

### Option A — Three.js

Use Three.js if the existing application can support it cleanly.

Possible visual elements:

* 3D particles
* Floating nodes
* Connecting network lines
* Camera movement
* Depth
* Mouse interaction

### Option B — HTML Canvas

Use Canvas if Three.js would add unnecessary complexity.

Canvas is preferred if:

* The current project is simple.
* Performance is more important.
* The animation only needs 2D network effects.

### Option C — CSS

Use CSS for simple effects such as:

* Grid movement
* Glowing borders
* Pulse animations
* Scan lines
* Page transitions

Do not add a large animation library just for simple CSS effects.

---

# 5. Animation Architecture

Create the animation as a reusable component.

Suggested structure:

```text
frontend/
└── src/
    ├── components/
    │   ├── CyberNetworkBackground.jsx
    │   ├── ScanAnimation.jsx
    │   ├── AnimatedGrid.jsx
    │   └── PageTransition.jsx
    │
    ├── pages/
    │   ├── Dashboard.jsx
    │   ├── Result.jsx
    │   └── History.jsx
    │
    └── styles/
        └── animations.css
```

Do not create all animation logic directly inside `App.jsx`.

---

# 6. Background Framework

Create a full-page animated cybersecurity background.

It should contain:

```text
                ●
               / \
              /   \
        ●────●─────●
         \    \    /
          \    ●──●
           \  /
            ●
```

Nodes should:

* Move slowly.
* Have subtle opacity changes.
* Connect dynamically.
* Avoid covering important text.
* Stay behind application content.

The movement should feel organic.

Do not make nodes move extremely fast.

---

# 7. Animated Grid

Add a subtle digital grid behind the interface.

Example concept:

```text
────────────────────────────
│    │    │    │    │    │
│────┼────┼────┼────┼────│
│    │    │    │    │    │
│────┼────┼────┼────┼────│
│    │    │    │    │    │
────────────────────────────
```

The grid can slowly move horizontally/vertically or use a subtle perspective effect.

Requirements:

* Very low opacity.
* Must not reduce text readability.
* Must not cause visual distraction.
* Must remain responsive.

---

# 8. Network Nodes

Create multiple animated nodes.

Each node can contain:

```text
●
```

with a subtle pulse:

```text
● → ◉ → ●
```

Use randomized positions only for visual animation.

IMPORTANT:

Random visual node positions are allowed.

Random application predictions are NOT allowed.

Never use random values for:

* Confidence
* Prediction
* Risk score
* URL result
* Scan history
* ML output

---

# 9. Connecting Lines

Connect nearby nodes using animated lines.

Example:

```text
●────────●
 \       /
  \     /
   ●───●
```

Lines should:

* Fade in/out smoothly.
* Move slowly.
* Use subtle opacity.
* Avoid excessive brightness.

The network should look like a cybersecurity infrastructure.

---

# 10. Data Flow Particles

Add small particles travelling through network connections.

Example:

```text
●───────●───────●
    →       →
```

Particles should represent visual data movement only.

They must NOT represent real requests unless explicitly connected to actual application state.

Do not claim:

> "This particle represents your URL being analyzed."

unless the animation is actually connected to that event.

---

# 11. URL Analysis Animation

When the user clicks:

```text
Analyze URL
```

show a professional scanning animation.

Example:

```text
┌─────────────────────────────────┐
│                                 │
│       ANALYZING URL             │
│                                 │
│   ────────────────►             │
│                                 │
│       SCANNING                  │
│                                 │
└─────────────────────────────────┘
```

Use:

* Moving scan line
* Pulsing border
* Rotating/animated security icon
* Progress-like visual effect

IMPORTANT:

Do not display fake processing percentages.

Do NOT show:

```text
37%
62%
89%
```

unless those percentages represent real backend progress.

For the current application, simply use:

```text
Analyzing URL...
```

or:

```text
Analyzing
Extracting features
Running model
```

only if these stages correspond to actual application states.

---

# 12. Result Animation

When the backend returns the real prediction:

Animate the result card.

Example sequence:

```text
Result container
      ↓
Fade in
      ↓
Scale 0.96 → 1
      ↓
Risk/confidence visualization
      ↓
Feature cards
      ↓
Explanation section
```

Do not invent any values.

Use the actual API response.

---

# 13. Risk Visualization

If the current backend provides a real model confidence/risk value, animate that actual value.

For example:

```text
Actual backend value
        ↓
Animated visualization
        ↓
Final displayed value
```

Do not generate a fake value for animation.

Do not use:

```javascript
Math.random()
```

to generate a fake risk score.

Do not hardcode:

```javascript
const confidence = 87;
```

---

# 14. Cybersecurity Scan Effect

Create a scanning effect around the analysis area.

Possible effect:

```text
┌───────────────────────────────┐
│                               │
│       URL ANALYSIS            │
│                               │
│  ═══════════════════════       │
│          ↑                    │
│       SCANNING                │
│                               │
└───────────────────────────────┘
```

The scanning line should move smoothly.

Use CSS animations or Canvas.

---

# 15. Hero Section Animation

The main dashboard/landing section should have the animated framework behind it.

Recommended structure:

```text
┌──────────────────────────────────────────────┐
│                                              │
│       Animated Cyber Network                 │
│                                              │
│             PHISHGUARD                       │
│                                              │
│       AI-Powered URL Security                │
│                                              │
│   ┌────────────────────────────────────┐     │
│   │ Enter URL...                       │     │
│   └────────────────────────────────────┘     │
│                                              │
│             [ Analyze URL ]                  │
│                                              │
│       ●────●────●────●                       │
│                                              │
└──────────────────────────────────────────────┘
```

The framework should remain behind the content.

---

# 16. Mouse Interaction

If technically appropriate, add subtle mouse interaction.

For example:

* Nodes slightly move toward the mouse.
* Network reacts subtly.
* Background shifts slightly.
* Particles respond to pointer movement.

Keep the effect subtle.

Do not make the entire page move aggressively.

---

# 17. Scroll Animation

Add subtle scroll-based animation.

Examples:

### Hero

```text
Fade + slight movement
```

### Features

```text
Cards appear as user scrolls
```

### Analysis section

```text
Subtle slide/fade
```

### Footer

```text
Simple fade
```

Do not animate every element.

---

# 18. Page Transitions

Use smooth transitions between:

```text
Dashboard
    ↓
Analysis Result
    ↓
History
    ↓
Details
```

Preferred:

* Fade
* Small translate
* Small scale

Avoid:

* Large rotations
* Fast zooms
* Flashing
* Excessive motion

---

# 19. Hover Animations

Cards:

```text
Normal
   ↓
Slight elevation
   ↓
Border highlight
```

Buttons:

```text
Normal
   ↓
Small scale
   ↓
Arrow/indicator movement
```

Navigation:

```text
Text
 ↓
Animated underline
```

All hover effects must have usable click/tap equivalents.

---

# 20. Professional Cybersecurity Design

The animation should feel like:

* AI security platform
* SOC dashboard
* Threat intelligence interface
* Modern cybersecurity SaaS

Avoid making it look like:

* Gaming website
* Hacker movie interface
* Cryptocurrency website
* Neon gaming UI
* Children's animation

Avoid excessive:

* Glow
* Blur
* Neon
* Particles
* Flashing effects

---

# 21. Performance Requirements

Animation must not significantly slow down the application.

Requirements:

* Use `requestAnimationFrame` correctly.
* Cancel animation frames when components unmount.
* Remove event listeners during cleanup.
* Avoid unnecessary React re-renders.
* Avoid creating thousands of particles.
* Keep animation complexity reasonable.
* Test on normal laptop hardware.
* Test mobile responsiveness.

Do not continuously update React state for every animation frame.

Prefer:

```text
Canvas
requestAnimationFrame
CSS animations
```

for continuous visual effects.

---

# 22. Responsive Design

The animation must work on:

* Desktop
* Laptop
* Tablet
* Mobile

On mobile:

* Reduce particle count.
* Reduce network density.
* Reduce animation complexity.
* Disable expensive 3D effects if necessary.

The UI must remain more important than the animation.

---

# 23. Accessibility

Respect:

```css
prefers-reduced-motion
```

When the user prefers reduced motion:

* Disable continuous movement.
* Disable unnecessary transitions.
* Keep the framework mostly static.
* Keep all functionality available.

Example:

```css
@media (prefers-reduced-motion: reduce) {
    * {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}
```

Do not rely on animation to communicate important information.

---

# 24. No Sample Data Policy

This is extremely important.

The animation must never introduce fake application information.

DO NOT create:

```text
Recent Scans
Google.com — SAFE
paypal-login.xyz — PHISHING
example.com — SAFE
```

DO NOT create fake dashboard statistics:

```text
1,248 URLs scanned
927 safe
321 phishing
```

DO NOT create fake charts.

DO NOT create fake history.

If there is no real data, display an empty state:

```text
No scans yet

Enter a URL above to begin your first security analysis.
```

---

# 25. No Fake ML Results

Never use:

```javascript
Math.random()
```

for:

* Prediction
* Confidence
* Risk
* Threat score
* Feature values

Never use:

```javascript
if (url.includes("google")) {
    return "SAFE";
}
```

Never hardcode:

```javascript
prediction = "PHISHING";
```

All predictions must come from the existing backend.

---

# 26. Animation State

The animation may react to real application states:

```text
IDLE
   ↓
ANALYZING
   ↓
SUCCESS
```

or:

```text
IDLE
   ↓
ANALYZING
   ↓
ERROR
```

Example:

```javascript
switch (status) {
    case "idle":
        // normal background animation
        break;

    case "analyzing":
        // scanning animation
        break;

    case "success":
        // result reveal
        break;

    case "error":
        // subtle error animation
        break;
}
```

These states must come from actual application state.

---

# 27. Error Animation

If the backend request fails:

Show a subtle error state.

Example:

```text
┌────────────────────────────┐
│                            │
│     Analysis Failed        │
│                            │
│  Unable to analyze URL.    │
│  Please try again.         │
│                            │
└────────────────────────────┘
```

Do not display:

* Stack traces
* Python paths
* Database credentials
* Internal server information

---

# 28. Do Not Change Security Architecture

The animation must NOT:

* Fetch URLs.
* Open submitted websites.
* Follow redirects.
* Execute submitted JavaScript.
* Crawl websites.
* Download website files.
* Expose backend files.
* Expose ML models.
* Expose `.env`.
* Expose dataset files.

The URL remains an untrusted string.

---

# 29. Dependency Rules

Before installing a new library:

1. Check `package.json`.
2. Check whether the required functionality already exists.
3. Prefer existing dependencies.
4. Add a new dependency only when it provides meaningful value.

If Three.js is used, keep it isolated to the animation component.

Do not introduce multiple animation libraries unnecessarily.

---

# 30. Suggested Animation Components

Implement reusable components such as:

```text
CyberNetworkBackground
AnimatedGrid
NetworkParticles
ScanLine
AnalysisAnimation
ResultReveal
PageTransition
```

Keep responsibilities separated.

---

# 31. Suggested Final Experience

The final website should feel like:

```text
                 PHISHGUARD

       ┌─────────────────────────┐
       │                         │
       │    CYBER NETWORK        │
       │                         │
       │      ●────●             │
       │     /      \            │
       │    ●        ●           │
       │     \      /            │
       │      ●────●             │
       │                         │
       └─────────────────────────┘

              Enter URL

       ┌─────────────────────────┐
       │ https://................│
       └─────────────────────────┘

             [ Analyze URL ]

                    ↓

              ANALYZING...

        animated scanning framework

                    ↓

             REAL RESULT

       prediction from ML backend
```

The visual framework should make the application memorable while the actual data remains completely real.

---

# 32. Implementation Process

Implement in this order:

### Step 1

Inspect the existing frontend.

### Step 2

Identify the main dashboard/landing page.

### Step 3

Create the reusable animation component.

### Step 4

Add the animated background.

### Step 5

Add network nodes and connections.

### Step 6

Add moving grid.

### Step 7

Add subtle particles.

### Step 8

Connect animation state to the existing Analyze workflow.

### Step 9

Add scanning animation during the actual API request.

### Step 10

Add result reveal animation after the actual API response.

### Step 11

Add responsive behavior.

### Step 12

Add reduced-motion support.

### Step 13

Test performance.

### Step 14

Run the complete application.

---

# 33. Testing Checklist

Before finishing:

* [ ] Application starts successfully.
* [ ] Existing URL scanner still works.
* [ ] Backend API integration is unchanged.
* [ ] ML prediction is unchanged.
* [ ] MongoDB history is unchanged.
* [ ] No sample URLs were added.
* [ ] No fake statistics were added.
* [ ] No fake prediction was added.
* [ ] No random prediction exists.
* [ ] No random confidence exists.
* [ ] Animation works on desktop.
* [ ] Animation works on mobile.
* [ ] Animation does not cover text.
* [ ] Animation does not block buttons.
* [ ] Animation stops/cleans up correctly.
* [ ] Reduced-motion mode works.
* [ ] Browser console has no errors.
* [ ] No unnecessary dependencies were added.

---

# 34. Antigravity Agent Rules

While implementing this task:

1. Inspect the existing code before modifying it.
2. Do not rewrite working components unnecessarily.
3. Do not create sample data.
4. Do not fabricate ML results.
5. Do not hardcode predictions.
6. Do not move ML logic to frontend.
7. Do not expose backend code.
8. Do not expose model files.
9. Do not expose dataset files.
10. Do not expose environment variables.
11. Do not break existing API integration.
12. Keep animation logic modular.
13. Prefer performance-friendly animation techniques.
14. Test after each major change.
15. Fix root causes instead of hiding errors.
16. Keep the project runnable after every phase.
17. Update documentation if dependencies or architecture change.

---

# 35. Final Goal

Transform the current PhishGuard website into a polished cybersecurity product with a continuously moving visual framework.

The final result should communicate:

```text
SECURITY
    +
AI
    +
NETWORK
    +
ANALYSIS
```

through animation while keeping the actual application completely data-driven.

### Most Important Rule

**Animation should make the website amazing.**

**It must never fake the application's data.**
