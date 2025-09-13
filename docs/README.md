# Cross-Reference Matrix – SilentStacks / TDT Evidence Base

| Document                | Primary Role                         | Supports…                           | How It Supports                                                   |
|-------------------------|--------------------------------------|-------------------------------------|-------------------------------------------------------------------|
| **P0/CF Logs**          | Raw evidence of failures             | Findings, Framework, Step-G, Sims   | Provides ground truth (290 P0, 4 CF, 1 RF). Concrete failure cases.|
| **[token-blindness.md](token-blindness.md)**| Quantitative findings (thresholds, phases, stats) | Framework, Step-G, Sims | Defines 4-phase trajectory (catastrophic → equilibrium). Supplies measured thresholds (65/75/85/90/95).|
| **[ptdtm-vs-blindness.md](ptdtm-vs-blindness.md)** | Taxonomy / classification (context, size, resource, safety) | Findings, Step-G                    | Classifies “Token Blindness” as Resource Blindness subset (PTDTM). Benchmarks match measured fabrication & confusion.|
| **[Step-G Phenomenon.md](Step-G%20Phenomenon.md)** | Mechanism of failure (self-contradiction, safety gate bypass) | Framework, Findings                 | Shows **Safety Blindness in action**. Explains *why thresholds are ignored* despite explicit safeguards.|
| **TDT Simulations (1000-session)** | Long-run trajectory modeling | Findings, Framework                 | Confirms plateau (~78–82% TDT). Maps phases onto blindness levels.|
| **[Bridge Table (Phases ↔ Blindness)](bridge-table.md)** | Integration layer            | Framework, Findings, Sims           | Directly ties empirical phases to taxonomy categories + benchmarks.|

