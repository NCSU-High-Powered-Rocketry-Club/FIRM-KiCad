# FIRM — Filtered Inertial Rotational Module

This repository contains the KiCad project files for the Filtered Inertial Rotational Module (FIRM). FIRM is a high-performance inertial sensing and rotation sensing module developed for flight instrumentation and payload monitoring. The repository includes schematic symbols, PCB footprints, 3D models, and all board files necessary to review, edit and manufacture the module.

---

## Quick Start — open the project

1. Install KiCad (see [Install & Setup](#install--setup-kicad) below).
2. Clone the repository:
```bash
git clone https://github.com/NCSU-High-Powered-Rocketry-Club/FIRM-KiCad.git
```

---

## Install & Setup

First, install KiCad from [kicad.org](https://kicad.org/download/). We recommend using the latest stable release of KiCad for new designs.

### After installation
- Open the `FIRM.kicad_pro` project. KiCad will use the `sym-lib-table` and `fp-lib-table` files included here if you open the board/schematic from this checkout.
- If KiCad shows missing library warnings, update the Project Library Tables or use the library manager to add the project's `sym-lib-table` and `fp-lib-table`.

---

## Repository structure

Root-level description (key files/folders):

- `FIRM.kicad_sch` — schematic
- `FIRM.kicad_pcb` — PCB layout
- `FIRM.kicad_pro` — KiCad project file that links schematics, board and library tables
- `sym-lib-table` — project symbol library table that makes project-local symbols available to Eeschema
- `fp-lib-table` — project footprint library table that makes project-local footprints available
- `3dmodels/` — 3D STEP/WRL models used with footprints
- `symbols/` — human-editable symbol libraries (e.g., `connectors.kicad_sym`, `sensors.kicad_sym`)
- `footprints/` — footprint libraries as `.pretty` directories
- `FIRM_Interestlaunch/` — FIRM variant which was milled in the Makerspace.

---

## Library handling

We keep the component libraries inside the HPRC-KiCad-Library so that components can be reused across different HPRC projects.

Make sure to follow the "Setup" instructions [here](
https://github.com/NCSU-High-Powered-Rocketry-Club/HPRC-KiCad-Library)

---

## Good Practices & Design Rules

- Keep schematic symbols generic and footprints specific: do not hardcode assembly-side changes into symbols.
- Look at the existing schematic to see how we do things and try to be consistent.
- Save new libraries to the project-local tables (not global) to keep designs reproducible.
- Keep PCB footprints accurate — use accurate courtyard, 3D models, and update packaging information.
- Validate with DRC (PCB Editor > Inspect > Design Rules Checker) and ERC (Eeschema > Tools > ERC) before committing changes.
- When collaborating, include notes about part sources (Mouser/Digikey vendor links), footprints used, and any custom pad or thickness changes.

---

## Release & Manufacturing Checklist

Before requesting fab or assembling a board, run this checklist:
1. Run ERC (Eeschema > Tools > ERC) and fix all warnings.
2. Run DRC in PCB Editor and resolve all errors.
3. Create a BOM and confirm manufacturer part numbers and footprints match.
4. Generate Gerbers and drill files (Plot + Generate Drill Files) and inspect them in GerbView.
5. Check 3D model alignment in PCB Editor (View > 3D Viewer) to ensure components fit.
6. Tag or branch the repo in Git to preserve the release snapshot.

---

## Git Collaboration and Merge Process

KiCad collaboration using git is difficult due to the KiCad file format. For example, moving a few symbols in a schematic will cause many lines to be edited, which greatly increases the chances of merge conflicts.
1. Create an issue for your feature if there isn't one already.
2. Create a branch including your name and the issue number ex: name-fix-XX or name-add-XX
    - It is best practice to suffix your branch name with a very short description/wordrelated to your change
3. Implement your change on your branch
4. Create a pull request (PR) for your change. Make sure to include images of the schematic or pcb design as well as reasons behind design decision. Request reviews from the issue creator or relevant contributors. You should need one approval to merge.
5. Merge your change into main. You will probably have to and should be able to force merge into main. 
    - However, if someone made change in between the time your branched from main and need to merge, you will have to do an unconvential merge process. 
    - You need a clean branch off the new main for this; this clean branch can either be a new branch you create, or your feature branch with all your changes reverted with main force merged into it. Then, access your changes and copy (ctrl-c copy) your symbols/components.
    - Now, open your clean branch to paste and position your changes. Commit this and update your PR or create a new one linking to your old one, and try to merge your changes as soon as possible.

## License

See `LICENSE` at the repo root for licensing details.

---
