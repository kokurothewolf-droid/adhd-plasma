# Architecture Review: ADHD Plasma for KDE Plasma 6

## Review Purpose
Brief architecture review specifically looking for:
- duplicated KDE functionality
- competing sync layers
- privacy problems
- excessive dependencies
- unnecessary custom backend code
- maintainability risks

After review, proceed to Phase 1 unless a critical blocker exists.

---

## Duplicated KDE Functionality

### Findings: LOW RISK — Good avoidance of duplication

| Area | KDE Already Provides | ADHD Plasma Role | Risk |
|------|----------------------|------------------|------|
| **Calendar UI** | KOrganizer, Kalendar | TODAY/NOW panels show merged/summarized views, not full calendar replacement | ✅ Low — plasmoids aggregate, not replace |
| **Task management** | Akonadi-backed PIM | ADHD-specific metadata + Attention Queue on top of KDE data | ✅ Low — metadata layer only |
| **Notifications** | KDE notification framework | Persistent reminders with custom states (acknowledged/snoozed/blocked) | ✅ Low — KDE notif backbone + ADHD state extension |
| **Global shortcuts** | KWin session shortcuts | Super+Q capture + configurable overrides | ✅ Low — KWin infrastructure + one custom shortcut |
| **Time display** | KDE system clock, panel | Concrete time awareness visualization (1 PM ●████ 3 PM format) | ✅ Low — different visual format, same data source |
| **Sync infrastructure** | CalDAV/Akonadi if configured | Use existing, don't replicate | ✅ Low — explicit "use existing" directive |

**Verdict**: Architecture successfully avoids duplicating KDE functionality. ADHD Plasmoids aggregate and extend, not replace. The only custom layer is the Attention Queue state management, which is ADHD-specific and not covered by KDE out of the box.

---

## Competing Sync Layers

### Findings: LOW RISK — CalDAV-first, no custom engine

| Sync Aspect | Risk | Mitigation |
|-------------|------|------------|
| **Custom sync engine** | ❌ HIGH if implemented | ✅ Architecture explicitly avoids: "Do not run competing synchronization engines if KDE already manages the account" |
| **CalDAV client** | ✅ LOW | Python `caldav` 3.3.1 + `icalendar` 7.3.0 — standard protocol, no custom engine |
| **Akonadi vs direct CalDAV** | ⚠️ MEDIUM | If Akonadi available → use as local cache layer; if not → direct CalDAV. Make optional, not required. |
| **Bidirectional sync** | ✅ LOW | Verified pattern: desktop ↔ CalDAV server ↔ mobile clients. Version vectors for conflict detection. |
| **Conflict handling** | ✅ LOW | "KEEP LOCAL / USE SERVER" prompt pattern from Error UX spec. No silent resolution. |

**Critical check**: The architecture correctly identifies that if the user already has KDE accounts configured (KMail, KOrganizer, etc.), the plasmoids should use those accounts rather than creating a parallel sync pipeline.

**Verdict**: No competing sync layer. CalDAV is the integration layer, not a custom engine. Akonadi is optional fallback.

---

## Privacy Problems

### Findings: LOW RISK — Principles aligned with implementation

| Privacy Aspect | Risk | How Architecture Addresses It |
|---------------|------|------------------------------|
| **Telemetry** | ❌ HIGH in generic apps | ✅ "No telemetry, advertising, tracking SDKs" in principles. Explicitly absent from code. |
| **Account requirement** | ❌ HIGH if mandatory | ✅ "No account, cloud service, or AI should be required" — local-first is default. CalDAV opt-in only. |
| **Data mining** | ❌ HIGH if AI-used | ✅ "AI is optional later" — never required. All core function works without AI. |
| **Cross-service tracking** | ❌ MEDIUM | ✅ Single CalDAV channel for tasks + capture. No aggregate profiling across services. |
| **Location/usage tracking** | ❌ MEDIUM | ✅ No location tracking mentioned in spec. Opt-in only. |
| **Persistent data exposure** | ⚠️ LOW | ✅ SQLite under user home, encrypted if user's filesystem is encrypted. No cloud by default. |

**Verdict**: Privacy architecture is strong. Local-first is the default state. Cloud sync is explicit opt-in via CalDAV configuration. No telemetry or tracking baked in.

---

## Excessive Dependencies

### Findings: LOW RISK — Minimal, well-scoped dependency graph

| Dependency | Category | Status | Alternative if missing |
|------------|----------|--------|----------------------|
| **Kirigami 2** | QML UI | ✅ Available (Plasma 6) | Could fall back to QtQuick.Controls 2 directly |
| **KDE Frameworks 6** | System integration | ✅ Available | Minimal subset needed: coreaddons, gui, widgets, notifications |
| **Qt 6** | Base graphics | ✅ Available (Plasma 6 requires it) | N/A — platform requirement |
| **Python caldav/icalendar** | Sync | ✅ Installable | Could use Command-line nextcloud client as fallback |
| **SQLite** | Local storage | ✅ Built into Python/Qt | Could use JSON files if SQLite unavailable |
| **KWin session shorts** | Global shortcuts | ✅ Confirmed | Could use KDE global shortcuts API directly |
| **Natural-language date parsing** | Capture | ⚠️ Needs research | Python `dateutil` available; custom parser as fallback |

**Dependency count**: ~7 core dependencies, all either:
- Built into Plasma 6 (Kirigami, Qt, KWin)
- Installable pip packages (caldav, icalendar, dateutil)
- SQLite built-in

No optional dependencies that break the build. No Electron. No custom C++ backend required for MVP.

**Verdict**: Dependency graph is minimal and well-justified. No excessive or unnecessary dependencies.

---

## Unnecessary Custom Backend Code

### Findings: LOW RISK — Intentional minimalism

| Potential Custom Backend | Status | Reason |
|-------------------------|--------|--------|
| **Custom CalDAV sync engine** | ❌ Avoided | Architecture: "Use existing KDE infrastructure and open standards" |
| **Custom task database** | ❌ Avoided | Uses CalDAV as source of truth; SQLite only as local cache |
| **Custom natural-language parser** | ⚠️ Possible minimal custom | Start with Python `dateutil`, add custom only for edge cases |
| **Custom notification system** | ❌ Avoided | Leverages KDE notification framework + custom state metadata |
| **Custom sync conflict resolver** | ⚠️ Minimal needed | Version-vector based, 2-option prompt (KEEP LOCAL / USE SERVER) |
| **Custom capture backend** | ❌ Avoided | KWin global shortcut → QML dialog → CalDAV add item — no custom server |
| **Custom AI backend** | ❌ Explicitly avoided | "AI is optional later" — never required for core function |

**Custom code necessity**: Only what's truly ADHD-specific and not in KDE:
- Attention Queue state machine (pending/acknowledged/snoozed/completed/rescheduled/blocked)
- "Closing ≠ completion" contract enforcement
- Super+Q capture workflow
- Time awareness visualization format
- NL date parsing for capture field

Everything else is KDE infrastructure, CalDAV standard, or Python stdlib.

**Verdict**: Custom backend code is purposeful and minimal. Nothing unnecessary. Architecture successfully reuses existing KDE/CalDAV infrastructure.

---

## Maintainability Risks

### Findings: MEDIUM RISK — Manageable with good patterns

| Risk Area | Severity | Mitigation Strategy |
|-----------|----------|---------------------|
| **Plasma 6 API changes** | ⚠️ MEDIUM | Pin to Plasma 6.7.x LTS; follow KDE deprecation policy; abstract QML imports |
| **CalDAV server API variations** | ⚠️ MEDIUM | Target Nextcloud Tasks as primary; implement standard CalDAV; test against multiple servers |
| **Kirigami API changes** | ⚠️ LOW | Kirigami has stable major versions; import from official repos |
| **KWin shortcut changes** | ⚠️ LOW | KWin shortcut API stable; configurable default (Super+Q) |
| **SQLite schema evolution** | ⚠️ LOW | Version-migrate schema; backward-compatible additions |
| **Attention state sync between machines** | ⚠️ MEDIUM | CalDAV handles this; ADHD-specific metadata in `metadata` field; document sync behavior |
| **Configuration migration on version update** | ⚠️ MEDIUM | Provide migration script in packaging; default configs for new installs |
| **QML version compatibility** | ⚠️ LOW | Kirigami qmltypes; test on fresh Plasma 6 installs |

**Most significant risk**: Attention state synchronization between multiple ADHD Plasma machines. The architecture documents this as "Research how ADHD-specific state should synchronize between multiple ADHD Plasma machines" — this is tracked as an open question, not assumed.

**Secondary risk**: CalDAV server variations. Mitigated by targeting Nextcloud Tasks first, implementing standard protocol, testing against at least one other CalDAV server before broad deployment.

**Verdict**: Maintainability risks are identified and documented. No show-stopping risks. Mitigations are concrete (pinning, testing, versioned schemas). Proceed to Phase 1 with these risks noted.

---

## Summary: Critical Blockers?

| Blocker | Status | Action |
|---------|--------|--------|
| Duplicated KDE functionality | ✅ None | Proceed |
| Competing sync layer | ✅ None | Proceed |
| Privacy problems | ✅ None (principles aligned) | Proceed |
| Excessive dependencies | ✅ None | Proceed |
| Unnecessary custom backend | ✅ None | Proceed |
| Maintainability risks | ⚠️ Documented, manageable | Proceed with mitigations |

**No critical blockers exist**. The architecture review confirms the design is sound, principles are honored, and the path to Phase 1 is clear.

## Recommendation: Proceed to Phase 1

Build TODAY, NOW, ATTENTION and CAPTURE using fake/local data.

**Open items to track during Phase 1**:
1. Akonadi availability verification in actual Plasma session
2. Natural-language date parsing implementation (dateutil vs custom)
3. Attention state sync strategy between multiple machines
4. CalDAV server compatibility testing (beyond Nextcloud)