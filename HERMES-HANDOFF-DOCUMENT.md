# Hermes Hand-off Document
## Moving to New Operating System

This document captures all configuration, skills, and settings needed to continue fine-tuning Hermes on a new OS without starting from scratch.

---

## 📦 Core Hermes State (BACKUP)

### **State Database**
- **Path**: `~/.hermes/state.db` (156MB)
- **Backup**: `~/.hermes/state.db.pre-update-emergency-2026-09-26T15-20-37-642Z.bak`
- **Purpose**: All session state, conversation history, task tracking
- **Action**: Copy this file to new OS `~/.hermes/state.db` for instant resume

### **Skills Directory**
- **Path**: `~/.hermes/skills/` (1,375 entries)
- **Key skills loaded**:
  - `software-development` (938KB) - GitHub, code-review, repo-management
  - `autonomous-ai-agents` - AI agent orchestration
  - `devops` - SDLC review, kanban workflow
  - `omarchy` - Desktop customization (Omarchy/Hyprland/Quickshell)
  - `adhd-plasma-development` - KDE Plasma layer
  - `productivity` - Document creation, spreadsheets, presentations

### **Memory Store**
- **Path**: `~/.hermes/memories/` 
- **Contents**: User profile, environment facts, standing conventions
- **Size**: 2,186/2,200 chars (nearly full - see "Memory Management" below)
- **Action**: Copy to new OS for user identity and environment constants

### **Config File**
- **Path**: `~/.hermes/config.yaml` (45KB)
- **Contains**: TTS providers, model preferences, platform settings
- **Critical**: Do NOT overwrite on new OS - merge selectively

### **Usage Log**
- **Path**: `~/.hermes/.usage.json` (42KB)
- **Tracks**: Token usage, model costs, performance metrics
- **Action**: Preserve for budget tracking on new OS

---

## 🔧 Skills to Reinstall/Transfer

### **Essential Skills (must transfer)**

| Skill | Purpose | Location |
|-------|---------|----------|
| `software-development` | GitHub, PRs, code review, repo management | `~/.hermes/skills/software-development/` |
| `omarchy` | Omarchy 4.0.3/Hyprland/Quickshell desktop customization | `~/.hermes/skills/omarchy` → `/usr/share/omarchy/default/agents/skills/omarchy` |
| `adhd-plasma-development` | ADHD Plasma KDE layer build and configuration | `~/.hermes/skills/adhd-plasma-development/` |
| `autonomous-ai-agents` | Spawn/subagent orchestration | `~/.hermes/skills/autonomous-ai-agents/` |
| `productivity` | Docs, spreadsheets, presentations | `~/.hermes/skills/productivity/` |

### **Important Plugin Skills (symlinks)**

| Skill | Target | Notes |
|-------|--------|-------|
| `hyperframes` | `../../.claude/skills/hyperframes` | Core HyperFrames composition |
| `hyperframes-animation` | `../../.claude/skills/hyperframes-animation` | Animation knowledge |
| `hyperframes-audio` | `../../.claude/skills/hyperframes-audio` | Audio in compositions |
| `media-use` | `../../.claude/skills/media-use` | Agent Media OS |
| `figma` | `../../.claude/skills/figma` | Design import |
| `diagnose-crash` | `/usr/share/omarchy/default/agents/skills/diagnose-crash` | Crash analysis |

### **Skills with Supporting Files**

These skills have `.md` references and scripts that need to accompany them:

| Skill | Supporting Files | Critical Files |
|-------|-----------------|----------------|
| `software-development` | `references/auth.md`, `references/pr-workflow.md`, `scripts/git-credential-token.py`, `templates/` | All of the above - essential for GitHub workflows |
| `omarchy` | N/A (system-installed) | System-level only |
| `autonomous-ai-agents` | `scripts/` | Depends on task |
| `adhd-plasma-development` | `SKILL.md` | Frontmatter structure |

---

## 🌐 OS-Specific Considerations

### **Wayland vs X11**
- **Current host**: Wayland (KDE Plasma 6)
- **Issue**: GTK window ignores requested sizes (real surface ~397x461)
- **Workaround**: Use `DISPLAY=:0` + force layout box via app env vars
- **On new OS**: Verify Wayland availability; if X11 only, adjust widget coordinate expectations

### **GTK/Qt Settings**
- **Current**: On Wayland host, GTK window ignores requested sizes
- **Fix**: Force render size via app's own env vars
- **New OS**: Test if same issue occurs; if so, apply same workaround

### **Audio Output**
- **Current**: No audio output device on this host
- **Result**: Every audioplayers/gstreamer playback fails
- **Workaround**: Cache-voice path gated off
- **New OS**: If audio device exists, enable TTS; otherwise keep voice path gated

### **Memory Constraints**
- **Current**: i3-7100T, 4 threads, 7.6GiB RAM
- **Swap + zram**: Near full
- **Perf rule**: Report measured DELTA against disabled baseline, never absolute RSS
- **New OS**: Profile before claiming any perf figure; report delta against baseline

### **Network**
- **Current**: Wifi: RTL8822BU 11ac (5GHz, ~130 Mbit/s)
- **Dead**: RTL8723be (2.4GHz, 0.27 Mbit/s, WPA2 auth fails)
- **New OS**: Verify USB wifi adapter compatibility; if using built-in, expect issues

---

## 📁 Files to Transfer

### **Critical Configuration Files**

| File | Path | Purpose |
|------|------|---------|
| `config.yaml` | `~/.hermes/config.yaml` | Hermes global config (TTS, models, paths) |
| `auth.json` | `~/.hermes/auth.json` | Authentication state |
| `channel_directory.json` | `~/.hermes/channel_directory.json` | Channel mappings |
| `.env` | `~/.hermes/.env` | Environment variables |
| `install_id` | `~/.hermes/install_id` | Unique install identifier |

### **Skills and Memories**

| Item | Path | Action |
|------|------|--------|
| `.skills_prompt_snapshot.json` | `~/.hermes/.skills_prompt_snapshot.json` (97KB) | Backup before OS move |
| `ledger.jsonl` | `~/.hermes/.curator_ledger.jsonl` | Skills curation ledger |
| `usage.json` | `~/.hermes/.usage.json` (42KB) | Token usage tracking |
| `state.db` | `~/.hermes/state.db` (156MB) | Full session resume - COPY FIRST |
| `memories/` | `~/.hermes/memories/` | User profile + environment facts |

### **Project-Specific Files**

| File | Path | Description |
|------|------|-------------|
| `adhd-plasma/` | `~/Projects/adhd-plasma/` | KDE Plasma 6 executive-function layer |
| `kindcue-flutter/` | `~/Projects/kindcue-flutter/` | Tablet-first AAC app for neurodivergent children |
| `kokuro-desktop/` | `~/Projects/kokuro-desktop/` | Omarchy/Hyprland/Quickshell customization |
| `google-oauth2/` | `~/.config/google-oauth2/` | Google API tokens (calendar, tasks) |

---

## 🔄 Migration Procedure

### **Step 1: Backup Current State**

```bash
# 1. Copy state database (most important)
cp ~/.hermes/state.db ~/state.db.backup

# 2. Copy skills directory
cp -r ~/.hermes/skills/ ~/skills.backup

# 3. Copy memories
cp -r ~/.hermes/memories/ ~/memories.backup

# 4. Copy config
cp ~/.hermes/config.yaml ~/config.yaml.backup

# 5. Copy usage log
cp ~/.hermes/.usage.json ~/usage.json.backup
```

### **Step 2: Install on New OS**

```bash
# Create Hermes directory structure
mkdir -p ~/.hermes/{skills,memories,cache,scratch,logs,state-snapshots}

# 1. Restore state database (enables instant resume)
cp ~/state.db.backup ~/.hermes/state.db

# 2. Restore skills
cp -r ~/skills.backup/.hermes/skills/ ~/.hermes/skills/

# 3. Restore memories
cp -r ~/memories.backup/.hermes/memories/ ~/.hermes/memories/

# 4. Restore config
cp ~/config.yaml.backup ~/.hermes/config.yaml

# 5. Restore usage tracking
cp ~/usage.json.backup ~/.hermes/.usage.json
```

### **Step 3: Verify Installation**

```bash
# Check skills load
hermes skill_view name='software-development'

# Check state persists
head -5 ~/.hermes/state.db 2>/dev/null && echo "State DB accessible"

# Check config loaded
grep -c "tts.provider" ~/.hermes/config.yaml && echo "Config has TTS settings"

# Test basic operation
echo "Hermes handoff verification complete"
```

### **Step 4: Project-Specific Migration**

#### **ADHD Plasma**
```bash
# Copy project files
cp -r ~/Projects/adhd-plasma/ ~/new-os/Projects/

# Ensure Google API tokens accessible
# (OAuth tokens are user-specific, not OS-specific)
# Just copy the config and data model files

# Rebuild if needed (using transferred skills)
hermes skill_view name='adhd-plasma-development'
```

#### **Kindcue Flutter**
```bash
# Copy project
cp -r ~/Projects/kindcue-flutter/ ~/new-os/Projects/

# Note: $10/mo AI ceiling, model=deepseek-flash
# Perf floor: Fire HD 8 12th gen (3-4GB, Fire OS, no Play)

# Restore binding context
# Reference: ~/Downloads/kindcue-flutter-skill vN.md (updated each milestone)
```

#### **Omarchy/Hyprland/Quickshell**
```bash
# Config is in ~/.config/omarchy/ and ~/.config/hypr/
# Copy these directories if keeping same WM setup

# Key customizations:
# - ~/.config/omarchy/plugins/kokuro.dashboard
# - ~/.config/omarchy/themes/kokuro
# - ~/.kokuro-backups/
# - ~/Projects/kokuro-desktop (tag: baseline-before-kokuro)
```

---

## ⚠️ Known Issues & Workarounds (Carry These Forward)

### **1. GTK on Wayland Size Ignorance**
- **Symptom**: Requested window sizes ignored (real surface ~397x461)
- **Workaround**: `DISPLAY=:0` + force layout box via app's env vars
- **File to reference**: `~/.hermes/memories/gtk-wayland-workaround.md` (if created)

### **2. No Audio Output Device**
- **Symptom**: Audioplayers/gstreamer playback fails (two plugin errors, slow)
- **Workaround**: Cache-voice path gated off long harness runs
- **File to reference**: `~/.hermes/memories/audio-workaround.md`

### **3. Wifi RTL8723be Dead (0.27 Mbit/s)**
- **Symptom**: WPA2 auth fails (client TX fault, proven dead)
- **Live link**: USB RTL8822BU 11ac (5GHz, ~130 Mbit/s)
- **Action**: On new OS, verify wifi hardware; if using built-in RTL8723be, expect issues
- **File to reference**: `~/.hermes/memories/network-wifi-workaround.md`

### **4. wttr.in Expired TLS**
- **Symptom**: `wttr.in` unreachable (expired TLS cert)
- **Workaround**: Use `open-meteo` (`api.open-meteo.com`) instead
- **File to reference**: `~/.hermes/memories/weather-workaround.md`

### **5. Screensaver Blocks Grim Captures**
- **Symptom**: Idle screensaver (kokuro.video-screensaver) covers whole screen
- **Action**: Check `omarchy-shell video-screensaver status` and stop before grim captures
- **File to reference**: `~/.hermes/memories/screener-workaround.md`

### **6. Memory Tight (7.6GiB RAM, swap+zram near full)**
- **Rule**: Report measured DELTA against disabled baseline, never absolute RSS
- **Action**: Profile before claiming any perf figure
- **File to reference**: `~/.hermes/memories/perf-rules.md`

---

## 📋 Quick Reference Commands (New OS)

```bash
# Verify Hermes is loaded
hermes skill_view name='software-development' 2>&1 | head -5

# Check state is accessible
ls -la ~/.hermes/state.db && echo "State DB present"

# Check skills are installed
ls ~/.hermes/skills/ | head -10

# Verify config
grep "model:" ~/.hermes/config.yaml

# Check memories
cat ~/.hermes/memories/user.md 2>/dev/null || echo "No user.md yet"

# GitHub auth (if needed)
gh auth status

# ADHD Plasma status
ls ~/Projects/adhd-plasma/ 2>/dev/null && echo "ADHD Plasma project present"
```

---

## 🆘 If Things Go Wrong

### **State DB Missing/Corrupt**
1. Restore from `~/state.db.backup`
2. Check `.hermes/state.db.pre-update-emergency-2026-09-26T15-20-37-642Z.bak`
3. Re-run Hermes with `--reset` if needed (loses session history)

### **Skills Not Loading**
1. Verify `~/.hermes/skills/` has expected directories
2. Run `hermes skill_view name='<skill-name>'` to confirm
3. Check `~/.hermes/.skills_prompt_snapshot.json` for loaded skills

### **Config Mismatches**
1. Merge `~/config.yaml.backup` with new OS defaults
2. Critical fields: `tts.provider`, `model`, `provider`
3. Do NOT remove `memories/` entries intentionally

### **Project Files Not Found**
1. Verify project paths: `~/Projects/<project-name>/`
2. Check git remotes are still valid
3. For ADHD Plasma: ensure `caldav_backend.py` and widgets are intact

---

## ✅ Migration Checklist

- [ ] `~/.hermes/state.db` copied (156MB - most critical)
- [ ] `~/.hermes/skills/` transferred (all skill directories)
- [ ] `~/.hermes/memories/` transferred (user profile + environment)
- [ ] `~/.hermes/config.yaml` transferred/merged
- [ ] `~/.hermes/.usage.json` transferred (budget tracking)
- [ ] `~/.hermes/.skills_prompt_snapshot.json` backed up
- [ ] Projects: `~/Projects/adhd-plasma/` copied
- [ ] Projects: `~/Projects/kindcue-flutter/` copied
- [ ] Projects: `~/Projects/kokuro-desktop/` copied
- [ ] Google API tokens accessible (`~/.config/google-oauth2/token.json`)
- [ ] Wifi adapter verified (RTL8723be dead, RTL8822BU recommended)
- [ ] Wayland/GTK workaround noted (if applicable)
- [ ] Audio setup verified (or voice path gated)
- [ ] `gh auth status` valid (or git credential helper configured)

Handoff complete. On new OS, copy these files and run the verification commands to resume fine-tuning where you left off.
