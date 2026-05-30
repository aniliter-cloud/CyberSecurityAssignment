# 👻 Spectre Attack — Interactive Demo

> **CVE-2017-5753 · Educational Use Only**
> A fully self-contained HTML demo that walks you through the Spectre microarchitectural attack — from theory and analogy, through live interactive exploitation, to AI/ML-based defence.

---

## 📁 Files

| File | Description |
|------|-------------|
| `spectre_attack_enhanced.html` | Main interactive demo — open in any modern browser, no server needed |
| `Spectre_Attack.key` | Original Apple Keynote slide deck (source material) |
| `demo_je.html` | Original demo file (pre-enhancement baseline) |
| `README.md` | This file |

---

## 🚀 Quick Start

```bash
# Just open the HTML file — no build step, no dependencies
open spectre_attack_enhanced.html        # macOS
start spectre_attack_enhanced.html       # Windows
xdg-open spectre_attack_enhanced.html   # Linux
```

Or drag-and-drop the file into Chrome / Firefox / Edge / Safari.

> **Note:** Some browser security policies (strict COOP/COEP headers) may limit `SharedArrayBuffer` access. The simulations are JS-based and work fine without it; only a real native exploit would require it.

---

## 🗂️ Tab Structure & Flow

Follow the tabs in order for the intended narrative arc — **attacker first, defender last**.

```
📖 Theory  →  🧙 HP Analogy  →  ⏱ Demo 1  →  🧠 Demo 2  →  🔍 Demo 3  →  💻 PoC Code  →  🤖 AI/ML Solution
  (what)       (why it works)    (attack)      (attack)      (attack)      (attack)          (defence)
```

### Tab Breakdown

| Tab | What it covers |
|-----|---------------|
| **📖 Theory** | Spectre mechanics — speculative execution, cache side-channels, what can be stolen |
| **🧙 HP Analogy** | Hermione & Prof. Snape SVG cartoon scenes mapping every CPU concept to Hogwarts |
| **⏱ Demo 1: Cache Timing** | Live cache HIT vs MISS measurement using `performance.now()` |
| **🧠 Demo 2: Branch Training** | Animated branch predictor confidence bar — training then attack phase |
| **🔍 Demo 3: Probe Scan** | Full Flush+Reload simulation across all 256 probe array entries |
| **💻 Full PoC Code** | Annotated JavaScript Spectre Variant 1 exploit with mitigation patterns |
| **🤖 AI/ML Solution** | Four ML approaches (LSTM, NLP, RL, GNN) + interactive LSTM detection simulation |

---

## ✨ Features

- **Zero dependencies** — single HTML file, pure HTML/CSS/JS
- **SVG cartoon characters** — hand-drawn Hermione and Prof. Snape illustrate speculative execution
- **Three interactive demos** — clickable, animated, real-time
- **AI/ML detection simulation** — watch LSTM anomaly score rise during a simulated attack stream
- **Narrative flow** — tabs ordered so you experience the attack before the defence
- **Dark theme** — GitHub-inspired colour palette, Consolas monospace throughout
- **Mobile-friendly** — responsive grid, scrollable nav

---

## 🧙 The HP Analogy (Summary)

| Hogwarts World | CPU / Spectre World |
|----------------|---------------------|
| Hermione guessing ahead | Speculative Execution |
| Snape still writing the question | Slow RAM bounds-check in flight |
| Grabbing ingredient early | Speculative memory read of secret |
| Realising the guess was wrong | Branch misprediction detected |
| Putting the jar back | CPU rolls back architectural state |
| Footprints + powder on the floor | **Cache pollution — the side-channel!** |
| Attacker checks which cupboard has powder | Flush+Reload timing measurement |
| Deducing which ingredient she grabbed | Recovering the secret byte value |

---

## 🤖 AI/ML Defence Approaches Covered

| Technique | Purpose | Accuracy |
|-----------|---------|----------|
| **LSTM Neural Network** | Detect temporal HPC anomaly patterns in real time | ~97% |
| **NLP / CodeBERT** | Static scan for Spectre gadget shapes in source/binary | Pre-runtime |
| **Reinforcement Learning** | Dynamically tune IBPB/LFENCE overhead vs. threat level | ~40% overhead reduction |
| **Graph Neural Networks** | Flag uniform 256-node probe-array scan in memory graphs | Low false-positive |

---

## 🛡️ Mitigations Referenced

- **Retpoline** — compiler replaces indirect branches with return trampolines
- **IBRS / IBPB / STIBP** — Intel/AMD microcode flushes branch predictor on privilege transitions
- **KPTI** — Kernel Page Table Isolation separates user/kernel memory maps
- **LFENCE** — serialisation barrier inserted before bounds-checked reads
- **Index Masking** — bitwise AND forces indices within safe range regardless of speculation
- **Site Isolation** — browsers isolate origins into separate OS processes
- **Timer jitter** — `performance.now()` resolution reduced to ~100 µs post-Spectre

---

## 💡 What Else Could Be Added

### 🎯 Presentation Enhancements
- [ ] **Slide-by-slide mode** — arrow-key navigation that mirrors the Keynote deck structure, useful for classroom presenting
- [ ] **Speaker notes panel** — toggle overlay with talking points per tab, hidden from audience view
- [ ] **Progress indicator** — step counter ("Tab 3 of 7") and a visual breadcrumb bar

### 🧪 Demo Depth
- [ ] **Spectre Variant 2 demo** — Branch Target Injection, separate from Variant 1 (Bounds Check Bypass)
- [ ] **Meltdown comparison tab** — side-by-side with Spectre to clarify the difference (kernel vs. speculation)
- [ ] **Real hardware counter feed** — hook into the Performance Observer API for actual CPU event counts where browser permits
- [ ] **Multi-byte live leak animation** — show each byte of "SPECTRE" leaking one character at a time with a typewriter effect and cache heatmap updating per byte

### 🤖 AI/ML Depth
- [ ] **Live LSTM chart** — real-time line graph of anomaly score over time as the simulation runs
- [ ] **Confusion matrix widget** — show TP/FP/TN/FN rates interactively for different threshold settings
- [ ] **Model comparison table** — benchmark LSTM vs. Random Forest vs. CNN on synthetic HPC datasets
- [ ] **Code gadget scanner** — paste a JavaScript/C snippet and have it highlight potential Spectre gadget patterns (regex + AST heuristics)

### 🎮 Gamification
- [ ] **Quiz mode** — after each demo, a multiple-choice question locks the next tab until answered correctly
- [ ] **"Can you evade the AI?" challenge** — let users tweak attack parameters (scan speed, noise level) and try to stay below the LSTM detection threshold
- [ ] **Leaderboard** — score based on how quickly/accurately users identify the leaked byte

### 🖥️ Technical
- [ ] **WebAssembly version** — port the timing demos to WASM for more deterministic nanosecond measurements
- [ ] **Export report button** — generate a PDF summary of what was demonstrated (CVE details, mitigations applied, AI/ML approach)
- [ ] **Keyboard shortcuts** — `1`–`7` to jump tabs, `Space` to trigger next demo action
- [ ] **Colour-blind mode** — swap red/green palette for accessible blue/orange

---

## ⚠️ Disclaimer

This project is for **educational and research purposes only**. The demos simulate Spectre behaviour in a browser sandbox; they do not perform actual memory exfiltration. Real Spectre exploits require native code execution, fine-grained timer access, and system-specific tuning. All mitigations described are already deployed in modern operating systems, CPUs, and browsers.

---

## 📚 References

- Kocher et al., *Spectre Attacks: Exploiting Speculative Execution* (2018) — https://spectreattack.com
- CVE-2017-5753 — https://nvd.nist.gov/vuln/detail/CVE-2017-5753
- Google Project Zero — https://googleprojectzero.blogspot.com/2018/01/reading-privileged-memory-with-side.html
- Intel Retpoline whitepaper — https://www.intel.com/content/www/us/en/developer/articles/technical/software-security-guidance/technical-documentation/retpoline-a-branch-target-injection-mitigation.html
- Chen et al., *Detecting Spectre Attacks with Hardware Performance Counters* — IEEE S&P 2019

---
*Anil Kumar Das - G25AIT2009 \n*
*Made for Cybersecurity Demonstration — Educational Use Only*
