# Day 1: ARCHITECTURE FREEZE & REPO REORG
## Branch: sprint/demo-rc
## Target: Clean separation Isle App (citizen) ↔ Royal App (admin)

---

## 1. GIT BRANCH & FREEZE
```bash
cd /c/PXNode
git checkout -b sprint/demo-rc
git push -u origin sprint/demo-rc
# Protect branch: Settings → Branches → Add rule: sprint/demo-rc (require PR, status checks)
```

---

## 2. ISLE APP — PURGE ADMIN SCREENS
### Files to DELETE from `/c/PXNode/apps/isle_app/lib/screens/`:
- ❌ `royal_screen.dart` (13 KB) — sub-node registry → belongs to Royal App
- ❌ `paranoidx_screen.dart` (19 KB) — ParanoidX monitoring → Royal App
- ❌ `market_screen.dart` (19 KB) — Exchange/Buyback/Auction → Royal App (Treasury) or separate Bank screen
- ❌ `vault_screen.dart` (16 KB) — Admin vault mgmt → Royal App (DC Cloud)
- ❌ `pos_screen.dart` (8.7 KB) — POS admin → Royal App (or keep minimal citizen POS pay)

### Files to KEEP (Citizen only):
- ✅ `wallet_screen.dart` (20 KB) — citizen wallet
- ✅ `simplex_chat_screen.dart` (161 KB) — messenger
- ✅ `radio_screen.dart` (9.7 KB) — radio listener
- ✅ `dashboard_screen.dart` (13 KB) — citizen dashboard
- ✅ `welcome_screen.dart` (45 KB) — onboarding
- ✅ `market_screen.dart` → REPLACE with `bank_exchange_screen.dart` (citizen Bank & Exchange)

### NEW FILES to CREATE in Isle App:
- 🆕 `bank_exchange_screen.dart` — TLR/SILVER/USDT swap, order book (citizen view)
- 🆕 `gov_services_screen.dart` — ID/NFC, citizenship, voting
- 🆕 `social_feed_screen.dart` — posts with HOLD-tier spam protection

---

## 3. ROYAL APP — ADD MISSING CRITICAL SCREENS
### Current screens (8):
1. Dashboard ✅
2. AI Office ✅
3. Treasury ✅ (has mint/burn/oracle/deflation/dividend)
4. Communications ✅
5. DC Cloud ✅
6. Governance ✅
5. System ✅
8. Settings ✅

### NEW SCREENS to CREATE (Priority HIGH):
| Screen | Purpose | API Endpoints |
|--------|---------|---------------|
| **BrokerApprovalScreen** | Silver arrival → Verify → Mint TLR | `/api/broker/silver-arrival`, `/api/royal/mint`, `/api/royal/dividend` |
| **AuditorManagementScreen** | Top-256 holders, weekly rotation, access control | `/api/royal/audit/log`, `/api/royal/nodes/reputation`, `/api/royal/alerts` |
| **NodeHealthScreen** | Large fonts, simple indicators (King's view) | `/api/admin/metrics/system`, `/api/admin/docker`, `/api/paranoidx/status` |
| **EmergencyControlsScreen** | Panic, Stop, Key Rotation, Backup | `/api/royal/emergency-stop`, `/api/panic`, `/api/admin/backup` |

### Navigation Update (main.dart):
Add to `_screens` list and `NavigationRail` destinations:
```dart
// New imports
import 'screens/broker_approval_screen.dart';
import 'screens/auditor_management_screen.dart';
import 'screens/node_health_screen.dart';
import 'screens/emergency_controls_screen.dart';

// In _screens (reorder for King's workflow):
final List<Widget> _screens = [
  const DashboardScreen(),           // 0 - Overview
  const BrokerApprovalScreen(),      // 1 - Silver → TLR (DAILY WORK)
  const TreasuryScreen(),            // 2 - Reserve, Mint, Burn, Dividends
  const AuditorManagementScreen(),   // 3 - Weekly rotation
  const NodeHealthScreen(),          // 4 - Health (large fonts)
  const EmergencyControlsScreen(),   // 5 - Panic, Stop
  const AIOfficeScreen(),            // 6
  const CommunicationsScreen(),      // 7
  const DCCloudScreen(),             // 8
  const GovernanceScreen(),          // 9
  const SystemScreen(),              // 10
  const SettingsScreen(),            // 11
];

// NavigationRail destinations (add 4 new):
NavigationRailDestination(icon: Icon(Icons.verified), label: Text('Broker')),
NavigationRailDestination(icon: Icon(Icons.people), label: Text('Auditors')),
NavigationRailDestination(icon: Icon(Icons.monitor_heart), label: Text('Health')),
NavigationRailDestination(icon: Icon(Icons.warning), label: Text('Emergency')),
```

---

## 4. SHARED PACKAGE — NEW ADMIN WIDGETS
Create `/c/PXNode/apps/shared/admin_widgets/`:
```
apps/shared/admin_widgets/
├── pubspec.yaml
├── lib/
│   ├── admin_widgets.dart
│   ├── silver_deposit_card.dart      // Broker shipment card with Verify/Mint
│   ├── auditor_row.dart              // Auditor list item with rotate/grant/revoke
│   ├── health_indicator.dart         // Large font status (King-friendly)
│   ├── emergency_button.dart         // Panic button with confirmations
│   ├── tier_badge.dart               // HOLD tier display
│   └── audit_log_entry.dart          // Immutable audit log display
```

---

## 5. BACKEND — BROKER ENDPOINT (if not exists)
Check `/c/PXNode/internal/api/broker.go`:
```go
// POST /api/broker/silver-arrival
// Verify broker signature → Update reserve → Mint SILVER → Trigger TLR dividends
func BrokerSilverArrivalHandler(w http.ResponseWriter, r *http.Request) {
    // 1. Verify broker pubkey (whitelist)
    // 2. Validate warehouse receipt hash
    // 3. Update silver_reserve_ng.txt
    // 4. Mint SILVER (1:1 ng)
    // 5. Trigger TLR dividend distribution (80% holders, 20% treasury)
    // 6. Emit audit log entry
    // 7. Push WebSocket to Royal Dashboard (/api/royal/events)
}
```

---

## 6. API ENDPOINTS NEEDED FOR ROYAL APP
Verify these exist in `main.go` (from royal_api_service.dart):
- ✅ `/api/royal/reserve` (GET/POST)
- ✅ `/api/royal/mint` (POST)
- ✅ `/api/royal/burn` (POST)
- ✅ `/api/royal/oracle` (GET/POST)
- ✅ `/api/royal/deflation` (GET/POST)
- ✅ `/api/royal/dividend` (POST)
- ✅ `/api/royal/banknotes` (GET/POST)
- ✅ `/api/royal/audit-log` (GET)
- ✅ `/api/royal/emergency-stop` (GET/POST)
- ✅ `/api/royal/events` (SSE)
- ✅ `/api/broker/silver-arrival` (POST) — **NEED TO ADD**
- ✅ `/api/royal/nodes/reputation` (GET) — for auditor list
- ✅ `/api/admin/metrics/system` (GET) — for NodeHealthScreen

---

## 7. DAY 1 EXECUTION ORDER
| Time | Task | Owner |
|------|------|-------|
| 09:00 | Git branch + protect | Lead |
| 09:30 | Delete 5 admin screens from Isle App | Flutter Lead |
| 10:30 | Create Royal App missing 4 screens (stubs) | Flutter Lead |
| 12:00 | Update Royal App navigation (main.dart) | Flutter Lead |
| 13:00 | Create shared/admin_widgets package | Flutter Dev |
| 14:00 | Add broker.go endpoint (if missing) | Backend Lead |
| 15:00 | Wire BrokerApprovalScreen to API | Flutter + Backend |
| 16:00 | Wire AuditorManagementScreen to API | Flutter + Backend |
| 17:00 | Test Royal App builds (Windows/Linux) | QA |
| 18:00 | Commit & Push | All |

---

## 8. FILES TO MODIFY TODAY
```
/c/PXNode/
├── apps/isle_app/lib/screens/
│   ├── DELETE: royal_screen.dart, paranoidx_screen.dart, market_screen.dart, vault_screen.dart, pos_screen.dart
│   ├── CREATE: bank_exchange_screen.dart, gov_services_screen.dart, social_feed_screen.dart
│   └── MODIFY: main.dart (remove admin routes), isle_api_service.dart (remove admin methods)
├── apps/royal_app/
│   ├── lib/main.dart (add 4 screens + navigation)
│   ├── lib/screens/
│   │   ├── CREATE: broker_approval_screen.dart
│   │   ├── CREATE: auditor_management_screen.dart
│   │   ├── CREATE: node_health_screen.dart
│   │   ├── CREATE: emergency_controls_screen.dart
│   │   └── MODIFY: treasury_screen.dart (add broker deposit view)
│   └── lib/services/royal_api_service.dart (add broker methods)
├── apps/shared/admin_widgets/ (NEW PACKAGE)
└── internal/api/broker.go (NEW or MODIFY)
```

---

## 9. SUCCESS CRITERIA DAY 1
- [ ] Isle App builds without admin screens
- [ ] Royal App has 12 screens with NavigationRail
- [ ] BrokerApprovalScreen shows mock data → "Verify & Mint" button works
- [ ] AuditorManagementScreen shows mock top-10 → "Rotate" button works
- [ ] Both apps build Windows/Linux without errors
- [ ] Git commits: clean separation

---

**START NOW** — Create branch, delete Isle admin screens, scaffold Royal screens.