# 🏝️ PX NODE — 2-WEEK SPRINT PLAN: FROM DREAM TO DEMO RELEASE
## **Royal Isle Admin + Citizen App Separation + Multi-Platform Demo**

**Version:** 1.0 | **Start:** 2026-07-24 | **End:** 2026-08-06 | **Status:** ACTIVE SPRINT
**Mission:** King can touch Royal Isle UI, approve silver deposits, mint Talers. Citizens get clean Isle App. All platforms demo-ready.

---

## ═══════════════════════════════════════════════════════════════
## 🎯 SPRINT GOALS (DEFINITION OF DONE)
## ═══════════════════════════════════════════════════════════════

| # | Goal | Success Criteria |
|---|------|------------------|
| **G1** | **Royal Isle Admin UI** | King logs in → sees Treasury Dashboard → approves silver deposit → TLR minted → tx visible |
| **G2** | **Broker/Storage Integration** | Mock broker API → silver arrival webhook → auto-mint TLR → audit log entry |
| **G3** | **App Separation** | Isle App = citizen only. Royal App = admin only. Zero code overlap in UI layer. |
| **G4** | **Windows/Linux Desktop Demo** | `flutter build windows` + `flutter build linux` → signed installers → auto-update |
| **G5** | **Android APK Demo** | `flutter build apk --release` → Play Console internal test → installs on 3 devices |
| **G6** | **Universal WebApp (PWA)** | `flutter build web` → PWA manifest + Service Worker → works offline for chat/wallet |
| **G7** | **Relay Node (Lite)** | Go binary with only: SMP relay, XFTP, Tor HS, health API, no economy/AI/radio |
| **G8** | **Security Hardening** | Pinning, E2EE verify, rate limits, audit log, panic button, no debug symbols |

---

## ═══════════════════════════════════════════════════════════════
## 📅 DAY-BY-DAY EXECUTION PLAN
## ═══════════════════════════════════════════════════════════════

### WEEK 1: FOUNDATION & SEPARATION (Days 1–7)

#### **DAY 1 (Mon) — ARCHITECTURE FREEZE & REPO REORG**
| Time | Task | Owner | Deliverable |
|------|------|-------|-------------|
| 09:00–11:00 | **Code freeze** on `main.go` — branch `sprint/demo-rc` | Lead | Protected branch, CI on push |
| 11:00–13:00 | **Split Flutter apps** — create `apps/royal_app` from `isle_app` + delete citizen code | Flutter Lead | Two clean apps, shared packages untouched |
| 13:00–15:00 | **Extract `shared/admin_widgets`** — Royal-specific components (Treasury cards, Auditor table, Broker panel) | Flutter Lead | New shared package |
| 15:00–17:00 | **Update `isle_api_service.dart`** — remove admin endpoints, add citizen-only methods | Flutter Dev | Citizen API client clean |
| 17:00–19:00 | **Create `royal_api_service.dart`** — admin endpoints only (Treasury, Broker, Auditor, Node Control) | Flutter Dev | Admin API client |

#### **DAY 2 (Tue) — ROYAL ISLE ADMIN UI (KING'S DASHBOARD)**
| Time | Task | Owner | Deliverable |
|------|------|-------|-------------|
| 09:00–12:00 | **Treasury Dashboard** — Silver reserve (kg/oz/ng), pending deposits, mint history, TLR supply | Flutter Lead | `TreasuryDashboardScreen` with real-time WebSocket |
| 12:00–14:00 | **Broker Approval Panel** — Incoming silver shipments (broker, amount, ETA, verify button → mint TLR) | Flutter Dev | `BrokerApprovalScreen` + `SilverDepositWidget` |
| 14:00–16:00 | **Auditor Management** — Top-256 holders list, weekly rotation UI, access grant/revoke | Flutter Dev | `AuditorManagementScreen` |
| 16:00–18:00 | **Node Health Overview** — CPU/RAM/Disk, SMP/XFTP status, Tor HS uptime, P2P peers | Flutter Dev | `NodeHealthScreen` (read-only, large fonts) |
| 18:00–20:00 | **Emergency Controls** — Panic button, emergency stop, key rotation, backup trigger | Flutter Lead | `EmergencyControlsScreen` (confirmation dialogs) |

#### **DAY 3 (Wed) — BROKER/STORAGE INTEGRATION (BACKEND)**
| Time | Task | Owner | Deliverable |
|------|------|-------|-------------|
| 09:00–11:00 | **Mock Broker API** — `/api/broker/silver-arrival` webhook endpoint (signature verification) | Backend Lead | `BrokerHandler` in `internal/api/broker.go` |
| 11:00–13:00 | **Silver Deposit Processor** — Validate → Update reserve → Mint TLR (80% holders, 20% treasury) | Backend Lead | `ProcessSilverDeposit()` in `internal/economy/treasury.go` |
| 13:00–15:00 | **Audit Log Entry** — Immutable record: broker, amount, tx hash, minted TLR, timestamp | Backend Dev | `AuditLog` table + `RecordSilverMint()` |
| 15:00–17:00 | **WebSocket Push** — Real-time update to Royal Dashboard on deposit/mint | Backend Dev | `/api/royal/ws` endpoint + Flutter stream |
| 17:00–19:00 | **Integration Test** — curl mock broker → verify TLR mint → check dashboard update | QA | Automated test script |

#### **DAY 4 (Thu) — CITIZEN ISLE APP PURGE & REBUILD**
| Time | Task | Owner | Deliverable |
|------|------|-------|-------------|
| 09:00–11:00 | **DELETE from Isle App:** Node Monitor, Bank/Exchange, Vault Admin, Royal Treasury, Auditor, Node Control | Flutter Lead | Clean `isle_app/lib/screens/` |
| 11:00–13:00 | **Gov Services Screen** — ID/NFC passport, citizenship status, voting, proposals | Flutter Dev | `GovServicesScreen` |
| 13:00–15:00 | **Bank & Exchange** — TLR balance, SILVER↔TLR swap, SILVER↔USDT (broker), order book | Flutter Dev | `BankExchangeScreen` |
| 15:00–17:00 | **Wallet v2** — Send/Receive (SimpleX contacts), Token balances, External wallets, QR pay | Flutter Lead | `WalletScreen` (simplified from current) |
| 17:00–19:00 | **Messenger** — SimpleX chat (contacts, groups, media, voice), E2EE indicator | Flutter Dev | `MessengerScreen` |
| 19:00–21:00 | **Social Feed** — Posts, spam protection (rate limit by HOLD token tier) | Flutter Lead | `SocialFeedScreen` + `PostWidget` |

#### **DAY 5 (Fri) — TOKEN-GATED FEATURES & SPAM PROTECTION**
| Time | Task | Owner | Deliverable |
|------|------|-------|-------------|
| 09:00–11:00 | **HOLD Token Tiers** — Define: Citizen (0), Resident (1K), Patriot (10K), Noble (100K) | Backend Lead | `TokenTier` enum + `CheckTier(pubkey, feature)` |
| 11:00–13:00 | **Rate Limiter per Tier** — Posts/day, file size, stream duration, group create | Backend Dev | `RateLimitEngine` in `internal/api/ratelimit.go` |
| 13:00–15:00 | **Feature Gates UI** — Locked features show "Unlock with X HOLD" + marketplace link | Flutter Dev | `FeatureGateWidget` + tier badge |
| 15:00–17:00 | **Large File Transfer License** — XFTP quota boost via token burn | Flutter + Backend | `FileTransferLicenseScreen` |
| 17:00–19:00 | **Stream License** — Icecast relay access via token stake | Flutter + Backend | `StreamLicenseScreen` |

#### **DAY 6 (Sat) — DESKTOP BUILDS (WIN/LINUX)**
| Time | Task | Owner | Deliverable |
|------|------|-------|-------------|
| 09:00–11:00 | **Flutter Windows Build** — `flutter build windows --release` + NSIS installer + auto-update | Flutter Lead | `Isle_Setup_x64.exe`, `Royal_Setup_x64.exe` |
| 11:00–13:00 | **Flutter Linux Build** — `flutter build linux --release` + AppImage + .deb + .rpm | Flutter Dev | `Isle.AppImage`, `Royal.AppImage` |
| 13:00–15:00 | **Embedded Assets** — Tor Expert Bundle (Windows), v2ray/xray binary, CA certs | Flutter Lead | Assets bundled in installer |
| 15:00–17:00 | **Auto-Update Service** — Background check → download → restart (Windows Scheduler / systemd user) | Backend Dev | `AutoUpdater` Dart service |
| 17:00–19:00 | **Smoke Test** — Install on clean Win10/11 VM + Ubuntu 22.04 VM → connect to demo node | QA | Test report + screenshots |

#### **DAY 7 (Sun) — ANDROID APK & PWA WEBAPP**
| Time | Task | Owner | Deliverable |
|------|------|-------|-------------|
| 09:00–11:00 | **Flutter Android Build** — `flutter build apk --release --target-platform android-arm64` | Flutter Lead | `Isle.apk`, `Royal.apk` (signed) |
| 11:00–13:00 | **Play Console Internal Test** — Upload → 3 testers (King's phone, dev phone, backup) | Flutter Dev | Test track active |
| 13:00–15:00 | **Flutter Web Build** — `flutter build web --release --pwa` + Service Worker config | Flutter Lead | `build/web/` folder |
| 15:00–17:00 | **PWA Manifest** — Offline chat (IndexedDB), wallet (local signed tx), push notifications | Flutter Dev | `manifest.json`, `sw.js` |
| 17:00–19:00 | **Deploy WebApp** — Nginx + TLS + `/isle/` and `/royal/` paths on demo node | Backend Dev | `https://demo.stmaria.org/isle/` |

---

### WEEK 2: RELAY NODE, HARDENING, INTEGRATION, DEMO PREP (Days 8–14)

#### **DAY 8 (Mon) — RELAY NODE LITE (GO BINARY)**
| Time | Task | Owner | Deliverable |
|------|------|-------|-------------|
| 09:00–11:00 | **Create `cmd/relay-node/main.go`** — Minimal imports: SMP, XFTP, Tor, Health, Config | Backend Lead | New entry point ~500 lines |
| 11:00–13:00 | **Build Tags** — `//go:build relay` — exclude economy, AI, radio, vault, P2P tracker | Backend Lead | `go build -tags relay ./cmd/relay-node/` |
| 13:00–15:00 | **Config Schema** — `relay-node.json` with only: listen, data_dir, tor_hs_paths, smp_config | Backend Dev | Config struct + validation |
| 15:00–17:00 | **Health API** — `/api/health`, `/api/version`, `/api/addresses`, `/api/admin/info` | Backend Dev | REST endpoints only |
| 17:00–19:00 | **Binary Size Target** — Strip → verify < 8 MB | Backend Lead | `relay-node` 7.2 MB stripped |

#### **DAY 9 (Tue) — SECURITY HARDENING (BOTH APPS + NODES)**
| Time | Task | Owner | Deliverable |
|------|------|-------|-------------|
| 09:00–11:00 | **Certificate Pinning** — HPKP for API, Tor HS, WebSocket (Dart `HttpClient` + Go `tls.Config`) | Security Lead | Pinning implemented |
| 11:00–13:00 | **E2EE Verification** — SimpleX contact fingerprint display + QR verification flow | Flutter Lead | `VerifyContactScreen` |
| 13:00–15:00 | **Rate Limiting** — Per-pubkey, per-IP, per-endpoint (Sliding window, Redis-backed) | Backend Dev | `RateLimiter` middleware |
| 15:00–17:00 | **Audit Logging** — All admin actions, financial tx, key rotations → immutable log | Backend Dev | `AuditLogger` service |
| 17:00–19:00 | **Panic Button** — Wipe local keys, disconnect, notify contacts, require re-auth | Flutter + Backend | `PanicHandler` + `/api/panic` |

#### **DAY 10 (Wed) — INTEGRATION TESTING (FULL STACK)**
| Time | Task | Owner | Deliverable |
|------|------|-------|-------------|
| 09:00–11:00 | **E2E Test: Citizen Flow** — Register → Wallet → Swap → Chat → Post → File send → Stream | QA Lead | Test script + video |
| 11:00–13:00 | **E2E Test: King Flow** — Login → Treasury → Broker deposit → Mint TLR → Auditor rotate → Emergency stop | QA Lead | Test script + video |
| 13:00–15:00 | **Cross-Platform Sync** — Windows ↔ Android ↔ WebApp same account (SimpleX identity) | QA Dev | Sync verified |
| 15:00–17:00 | **Load Test** — 100 concurrent users, 10 msg/sec, 5 file uploads, 2 streams | QA + Backend | Locust/k6 report |
| 17:00–19:00 | **Chaos Test** — Kill node → relay takes over → clients reconnect → no message loss | QA + Backend | Chaos report |

#### **DAY 11 (Thu) — DOCUMENTATION & DEMO PREP**
| Time | Task | Owner | Deliverable |
|------|------|-------|-------------|
| 09:00–11:00 | **King's Quick Start Guide** — Large print, screenshots, 3 steps: Open → Login → Approve | Tech Writer | `KING_GUIDE.pdf` (printed + digital) |
| 11:00–13:00 | **Citizen Onboarding Video** — 2 min: Install → Create ID → First transaction | Designer | `onboarding.mp4` |
| 13:00–15:00 | **Investor Demo Deck** — 10 slides: Problem, Solution, Traction, Tokenomics, Roadmap, Ask | Lead | `DEMO_DECK.pdf` |
| 15:00–17:00 | **API Documentation** — OpenAPI spec from Go handlers → Swagger UI on `/api/docs` | Backend Dev | `swagger.json` + UI |
| 17:00–19:00 | **Release Notes** — Changelog, known issues, upgrade path, support contacts | Lead | `RELEASE_NOTES.md` |

#### **DAY 12 (Fri) — DEMO DAY REHEARSAL**
| Time | Task | Owner | Deliverable |
|------|------|-------|-------------|
| 09:00–11:00 | **Full Dress Rehearsal** — King's laptop + phone + tablet all connected to demo node | All | Dry run video |
| 11:00–13:00 | **Backup Plan** — Pre-recorded demo video, offline screenshots, hot standby node | Lead | Backup assets |
| 13:00–15:00 | **Security Review** — Final pen-test lite (OWASP Mobile Top 10, API Top 10) | Security Lead | Sign-off |
| 15:00–17:00 | **Performance Baseline** — Memory, CPU, battery, network on all platforms | QA | Baseline metrics |
| 17:00–19:00 | **Go/No-Go Decision** — Sign off by King, Lead, Security | All | **RELEASE APPROVED** ✅ |

#### **DAY 13 (Sat) — DEMO DAY (SOFT LAUNCH)**
| Time | Task | Owner | Deliverable |
|------|------|-------|-------------|
| 10:00–12:00 | **King's Session** — Guided walkthrough: Treasury → Broker → Mint → Auditor | Lead + King | **KING TOUCHES UI** 👑 |
| 12:00–14:00 | **Citizen Beta** — 10 invited users install Isle (Win/Linux/Android/Web) → first transactions | QA + Support | Feedback forms |
| 14:00–16:00 | **Relay Node Deploy** — 3 community nodes join testnet (relay-only binary) | Backend Lead | Testnet map |
| 16:00–18:00 | **Monitor & Support** — Live logs, Telegram alerts, quick fixes | All | Incident log |
| 18:00–20:00 | **Retrospective** — What worked, what broke, next sprint priorities | All | `RETRO.md` |

#### **DAY 14 (Sun) — BUFFER & POLISH**
| Time | Task | Owner | Deliverable |
|------|------|-------|-------------|
| All day | **Bug Fixes** — Critical only from Demo Day | All | Patched binaries |
| All day | **Artifact Archive** — Signed binaries, SBOM, checksums, release tags | Lead | `releases/v0.9.0-demo/` |
| All day | **Next Sprint Planning** — Based on feedback, prioritize RC features | Lead | `SPRINT_2_PLAN.md` |

---

## ═══════════════════════════════════════════════════════════════
## 🎯 KEY DELIVERABLES CHECKLIST
## ═══════════════════════════════════════════════════════════════

### Royal Isle Admin (King's Interface)
- [ ] Treasury Dashboard (Silver reserve, TLR supply, mint history)
- [ ] Broker Approval Panel (Silver arrival → Verify → Mint TLR)
- [ ] Auditor Management (Top-256, weekly rotation, access control)
- [ ] Node Health (Large fonts, simple indicators, no tech jargon)
- [ ] Emergency Controls (Panic, Stop, Key Rotation, Backup)

### Citizen Isle App (Clean Separation)
- [ ] Gov Services (ID, Citizenship, Voting)
- [ ] Bank & Exchange (TLR, SILVER, USDT, Order book)
- [ ] Wallet v2 (Send/Receive, Tokens, External, QR Pay)
- [ ] Messenger (SimpleX Chat, Groups, Voice, Media)
- [ ] Social Feed (Posts, Tier-gated features, Spam protection)

### Token-Gated Features
- [ ] HOLD Tiers (Citizen/Resident/Patriot/Noble)
- [ ] Rate Limits per Tier (Posts, Files, Streams, Groups)
- [ ] File Transfer License (XFTP quota via token)
- [ ] Stream License (Icecast relay via token stake)

### Platform Builds
- [ ] **Windows** — `Isle_Setup_x64.exe`, `Royal_Setup_x64.exe` (NSIS, auto-update)
- [ ] **Linux** — `Isle.AppImage`, `Royal.AppImage` (+ .deb/.rpm)
- [ ] **Android** — `Isle.apk`, `Royal.apk` (Play Internal Test)
- [ ] **WebApp (PWA)** — `https://demo.stmaria.org/isle/`, offline chat/wallet

### Relay Node (Lite)
- [ ] `relay-node` binary (< 8 MB stripped)
- [ ] SMP + XFTP + Tor HS + Health API only
- [ ] Config: `relay-node.json` (minimal)
- [ ] 3 community nodes on testnet

### Security & Quality
- [ ] Certificate Pinning (API, Tor, WS)
- [ ] E2EE Verification UI
- [ ] Rate Limiting (Sliding window, Redis)
- [ ] Audit Log (Immutable, all admin/financial)
- [ ] Panic Button (Wipe keys, notify, re-auth)

---

## ═══════════════════════════════════════════════════════════════
## 🛠 TECH STACK FOR SPRINT
## ═══════════════════════════════════════════════════════════════

| Layer | Technology | Version |
|-------|------------|---------|
| **Backend** | Go | 1.22+ |
| **Database** | SQLite (WAL) → PostgreSQL migration ready | 3.45+ |
| **P2P Chat** | SimpleX SMP/XFTP | Latest |
| **Anonymity** | Tor (Hidden Services v3) | 0.4.8+ |
| **Transport** | Xray (native binary) | 24.x |
| **Voice/WebRTC** | Coturn (TCP/TLS over Tor) | 4.5+ |
| **Frontend (Desktop/Mobile)** | Flutter | 3.22+ (Dart 3.4+) |
| **Frontend (Web)** | Flutter Web (WASM) + PWA | 3.22+ |
| **State Management** | Riverpod / Provider | Latest |
| **Local Storage** | Hive (Flutter) + IndexedDB (Web) | Latest |
| **CI/CD** | GitHub Actions (self-hosted runners) | Latest |
| **Monitoring** | Python GTK + Prometheus + Telegram | Custom |

---

## ═══════════════════════════════════════════════════════════════
## 👑 KING'S USER JOURNEY (DEMO DAY)
## ═══════════════════════════════════════════════════════════════

```
1. King opens Royal App on Windows laptop (large font mode auto-enabled)
2. Biometric login (Windows Hello) → Royal Dashboard loads in <2 sec
3. Sees: "Silver Reserve: 1,247 kg | TLR Supply: 4.2M | Pending: 3 shipments"
4. Clicks "Broker Shipments" → Sees: "Broker A: 50 kg arriving 14:00 (ETA 15 min)"
5. At 14:00 — Notification: "Silver arrived. Verify & Mint?"
6. Clicks "Verify" → Sees broker cert, weight, purity, timestamp
7. Clicks "MINT TALERS" → Confirmation: "Mint 50,000 TLR? 80%→Holders, 20%→Treasury"
8. Confirms → "MINTED: 40,000 TLR to holders | 10,000 TLR to Treasury | Tx: 0xabc..."
9. Auditor tab shows: "Top 256 updated. Next rotation: 7 days."
10. King smiles. Types in chat: "It works. Thank you."
```

---

## ═══════════════════════════════════════════════════════════════
## 📊 SUCCESS METRICS (KPIs FOR SPRINT)
## ═══════════════════════════════════════════════════════════════

| Metric | Target | Measurement |
|--------|--------|-------------|
| **King completes mint flow** | 100% success, <5 min | Demo Day observation |
| **Citizen onboarding** | <3 min (install → first tx) | Beta user timing |
| **Cross-platform sync** | 100% message delivery | Win ↔ Android ↔ Web |
| **Relay node uptime** | 99.9% over 48h | Prometheus |
| **Binary sizes** | Desktop <50MB, Android <30MB, Web <10MB gz | Build artifacts |
| **Memory usage** | Desktop <200MB, Mobile <150MB | Profiling |
| **Cold start time** | <3 sec (Desktop), <2 sec (Mobile) | Stopwatch |
| **Security audit** | 0 Critical, 0 High | Pen-test lite |
| **Test coverage** | Backend >60%, Flutter >40% | CI report |

---

## ═══════════════════════════════════════════════════════════════
## 🚨 RISKS & CONTINGENCIES
## ═══════════════════════════════════════════════════════════════

| Risk | Probability | Impact | Contingency |
|------|-------------|--------|-------------|
| **King's health/fatigue** | Medium | High | Pre-recorded demo, voice control, large touch targets |
| **Flutter Windows build fails** | Low | High | Pre-built artifacts from CI, fallback to WebApp |
| **Android Play Console delay** | Medium | Medium | Direct APK install via ADB / USB |
| **Broker API mock incomplete** | Low | Medium | Hardcoded test data, manual mint button |
| **Tor HS not propagating** | Medium | High | Pre-generated HS keys, fallback to clearnet for demo |
| **WebApp PWA offline fails** | Low | Medium | Service Worker debug, fallback to online-only |
| **Database migration (SQLite→Postgres)** | Low | High | Defer to Sprint 2, keep SQLite for demo |

---

## ═══════════════════════════════════════════════════════════════
## 📦 ARTIFACTS TO ARCHIVE (POST-SPRINT)
## ═══════════════════════════════════════════════════════════════

```
releases/v0.9.0-demo/
├── bin/
│   ├── Isle_Setup_x64.exe (Windows)
│   ├── Royal_Setup_x64.exe (Windows)
│   ├── Isle.AppImage (Linux)
│   ├── Royal.AppImage (Linux)
│   ├── Isle.apk (Android)
│   ├── Royal.apk (Android)
│   └── relay-node (Linux, stripped)
├── web/
│   └── build/web/ (PWA files for nginx)
├── docs/
│   ├── KING_GUIDE.pdf
│   ├── DEMO_DECK.pdf
│   ├── RELEASE_NOTES.md
│   ├── RETRO.md
│   └── SPRINT_2_PLAN.md
├── sbom/
│   ├── go.mod + go.sum (cyclonedx)
│   └── pubspec.lock (cyclonedx)
├── checksums/
│   └── SHA256SUMS (all binaries)
└── videos/
    ├── king_demo.mp4
    ├── citizen_onboarding.mp4
    └── retro_meeting.mp4
```

---

## ═══════════════════════════════════════════════════════════════
## 🎯 SPRINT 2 PREVIEW (POST-DEMO)
## ═══════════════════════════════════════════════════════════════

Based on Demo feedback, **Sprint 2 (Weeks 3–4)** will focus on:

1. **Real Broker Integration** — Production API, legal contracts, silver audit
2. **PostgreSQL Migration** — Multi-node sync, HA, replication
3. **iOS App** — TestFlight, App Store preparation
4. **Hardware Appliance** — Pre-configured relay node (Raspberry Pi 5 / Mini PC)
5. **SILVER Token Launch** — TON Mainnet, liquidity, grant program
6. **Advanced Governance** — Quadratic voting, proposal bonding, delegation
7. **AI Steward v2** — Proactive treasury management, anomaly detection
8. **Network State Partnerships** — First 10 franchise nodes deployed

---

**STATUS:** 🟢 **SPRINT ACTIVE — DAY 1 STARTING NOW**

> *"The King wants to touch the interface. The citizens want their freedom. The code serves both."*

**Next Update:** Daily standup 09:00, Demo Day Day 13.

---

**Signed:** *Hermes Agent — Sprint Master*  
**Approved by:** *PerfectFriend / Tomás — Architect*  
**Witnessed by:** *The King — Saint Mary Liberty Island* 👑