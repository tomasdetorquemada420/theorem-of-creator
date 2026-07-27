# HERMES AGENT INSTRUCTION — PX Node / Royal ParanoidX Transport Node

> **Архив:** `px-node-project.zip` → распакован в `C:\PXNode\`
> **Агент-получатель:** Hermes (Deepseek V4, как и я)
> **Дата архива:** 2026-07-23

---

## 1. ЧТО ЭТО ЗА ПРОЕКТ

**PX Node** (он же **Royal ParanoidX Transport Node**) — суверенный сетевой демон для **Saint Mary Liberty Island ("The Isle", stmaria.org)**. Это backend-сервер, который объединяет:

- **SimpleX Chat** — защищённый p2p-мессенджер (через bridge)
- **Tor Onion-сервисы** — xftp, smp, dashboard
- **V2Ray/Xray VPN** — транспортный слой
- **Экономика** — Silver Standard (токенизированное серебро), RWA, аукционы
- **Royal Banking** — банкноты, холодные кошельки, стейкинг
- **ParanoidX** — мониторинг всех транспортных слоёв
- **POS-терминалы** — приём платежей в SILVER
- **Радио** — стриминг через Icecast
- **AI-агенты** — Telegram-боты, администрирование

### Ключевые концепты

| Термин | Описание |
|--------|----------|
| **Royal Node** | Базовая реализация ноды для stmaria.org |
| **PX Node** | Основной бренд (ParanoidX Transport Node) |
| **Silver Standard** | Токенизированное серебро (backed by physical Ag) |
| **SILVER** | Торгуемый токен на TON (jetton) |
| **Isle** | Фронтенд (Flutter-приложение) |
| **KiloParanoidX** | Автономный монитор транспортных слоёв |
| **Island Bot** | Telegram-бот для автоматизации ноды |

---

## 2. СТРУКТУРА ПРОЕКТА (C:\PXNode\)

```
C:\PXNode\
├── cmd/
│   └── simplex-node/          # Главный entry point (main.go, app.html)
│       └── main.go            # 3447 строк — роутинг, инициализация
├── internal/
│   ├── api/                   # HTTP-хендлеры (все API endpoints)
│   │   ├── admin.go           # Админ-панель, live dashboard
│   │   ├── nodeinfo.go        # /api/admin/info, /api/version
│   │   ├── chat.go            # SimpleX Chat bridge
│   │   ├── radio.go           # Радио-стриминг
│   │   ├── pos.go             # POS-терминалы
│   │   ├── economy.go         # Silver Standard экономика
│   │   ├── token_wallet.go    # **Токен-кошелёк (5 endpoints)**
│   │   ├── external_wallet.go # **Внешние кошельки (5 endpoints)**
│   │   ├── paranoidx.go       # ParanoidX monitoring
│   │   ├── metrics_prom.go    # Prometheus метрики
│   │   └── docs.go            # API документация
│   ├── store/                 # SQLite хранилища
│   │   ├── token_store.go     # **Токены + топ-10 seed**
│   │   ├── extwallet_store.go # **Внешние кошельки**
│   │   ├── store.go           # Базовое хранилище
│   │   └── queries/           # Скомпилированные SQL-запросы
│   ├── economy/               # Экономическая логика
│   ├── middleware/             # HTTP middleware
│   ├── bridge/                # SimpleX bridge
│   └── ...                    # Другие пакеты
├── apps/
│   ├── isle_app/              # **Flutter-клиент Isle**
│   ├── royal_app/             # **Flutter-клиент Royal**
│   ├── life_elements_game/    # **Flutter игра Life Elements**
│   └── shared/                # **Dart shared packages**
│       ├── api_client/        # HTTP-клиент для API
│       └── models/            # Общие модели данных
├── docker/
│   ├── docker-compose.yml     # Docker Compose стек
│   ├── dashboard.html         # **SPA-дашборд (обновлён: PX Node)**
│   └── ...
├── KiloParanoidX/             # Автономный монитор слоёв
├── scripts/                   # Bash/Python скрипты
├── systemd/                   # systemd unit-файлы
├── docs/                      # Документация, whitepaper
├── node-monitor.py            # **Системный трей-монитор (обновлён)**
├── HERMES.md                  # Этот файл
└── go.mod / go.sum            # Go modules
```

---

## 3. ТЕКУЩЕЕ СОСТОЯНИЕ (на момент архивации)

### 3.1. Статус сборки

- **Go backend:** `go build ./...` — OK
- **Go vet:** `go vet ./...` — OK
- **Go tests:** 38/39 pass (1 pre-existing failure: `TestChatSendHandlerValidation` — expected 400 for empty body, got 200)
- **Flutter:** требуется `flutter pub get` + `flutter build apk` / `flutter build windows`
- **Python монитор:** `node-monitor.py` — работает (PID жив)

### 3.2. Что уже сделано (сессия 2026-07-23)

#### Этап A — Восстановление после потери данных
1. Проект был на USB FAT32 — нет symlink/execute perms
2. USB отключился во время долгой операции → потеря данных HDD
3. Восстановлено из backup-тарбола (`simplex-node-backup-torquemada-*.tar.gz`)
4. Все изменения сессии повторно накатаны на restored backup
5. Git init + USB backup remote

#### Этап B — Очистка диска
- Освобождено ~10 GB: Go build cache (1.1G), Gradle cache (5.5G), pub cache (0.65G), npm (0.4G), temp (0.5G)
- Сайд-проекты (Xbridge, MatrixX, simplex-fork, isle-duplicate) перенесены на USB

#### Этап C — Wallet Evolution (10 новых endpoint + Flutter UI)
1. **`internal/store/token_store.go`** — TokenStore + Top-10 seed data
2. **`internal/store/extwallet_store.go`** — ExternalWalletStore
3. **`internal/api/token_wallet.go`** — 5 handlers: List tokens, Get token, Create token balance, Update token, Delete token
4. **`internal/api/external_wallet.go`** — 5 handlers: List wallets, Get wallet, Create wallet, Update wallet, Delete wallet
5. **`cmd/simplex-node/main.go`**:
   - Строка ~1500: store init (TokenStore, ExternalWalletStore)
   - Строка ~1936: 10 новых routes
6. **Flutter shared (`apps/shared/`):**
   - `api_client/lib/src/token_client.dart` — Token HTTP-клиент
   - `api_client/lib/src/external_wallet_client.dart` — ExternalWallet HTTP-клиент
   - `models/lib/src/token.dart` — Token + TokenBalance модели
   - `models/lib/src/external_wallet.dart` — ExternalWallet модель
   - Barrel exports обновлены
7. **Flutter Isle (`apps/isle_app/`):**
   - `lib/services/isle_api_service.dart` — новые методы (getTokens, getWallets, etc.)
   - `lib/screens/wallet_screen.dart` — переписан: Balance + Transfer + Holdings + Silver + **Token Balances** + **External Wallets** (expandable cards)
8. **`scripts/backup-to-usb.sh`** — скрипт бекапа на USB

#### Этап D — Node Monitor v2 (Log Manager)
1. **Цветовая схема логов:**
   - CRITICAL/FATAL → `#ff2222` red
   - ERROR/FAIL → `#ff4444` red
   - WARNING → `#ffaa00` yellow
   - INFO/NOTICE → `#cccccc` white
   - DEBUG/TRACE → `#4488ff` blue
   - REQUEST (GET/POST/...) → `#44aaaa` cyan
   - SERVICE (START/STOP/CONNECT) → `#44cc44` green
2. **12 источников логов:**
   - Файловые (6): dashboard.log, xray.log, monitor.log, island.log, tor-file, vmess.log
   - Docker (6): smp-server, xftp, coturn, v2ray, tor, vpn-isle
3. **Фильтры:** Source dropdown, Level dropdown, Search text, Auto-scroll, Clear
4. **Хронологический unified лог** — все записи сортируются по времени
5. **Защита от крашей:**
   - Все GTK-обработчики обёрнуты в `_safe_call()` / `try/except`
   - `_render_tab_logs()` → `_safe_render_logs()` → `_render_logs_fallback(e)`
   - `_logs_as_text(N)` — текстовый fallback через `_show_dialog()`
   - **Исправлен segmentation fault**: ScrolledWindow был добавлен как child и в VBox, и в Notebook (два родителя)
6. **ANSI-escape коды** — вычищаются из docker output (`strip_ansi`)
7. **Опрос каждые 30 секунд** (LOG_POLL_INTERVAL)

#### Этап E — Ребрендинг
1. **`node-monitor.py`:** заголовок, индикатор, уведомления → "PX Node" / "Royal ParanoidX Transport Node"
2. **`cmd/simplex-node/main.go`:** `"build": "simplex-node-..."` → `"px-node-..."`
3. **`internal/api/nodeinfo.go`:** `Build: "simplex-node-..."` → `"px-node-..."`
4. **`docker/dashboard.html`:** `<title>PX Node • Dashboard</title>`, `<h1>PX Node</h1>`
5. **`~/.local/share/simplex-node/dashboard.html`:** обновлён (копия)
6. **`~/.config/autostart/node-monitor.desktop`:** путь → `/home/tomas/simplex-node/node-monitor.py`
7. **`~/.local/share/applications/node-monitor.desktop`:** обновлён

#### Этап F — Обновление бинарника
- Бинарник пересобран: `go build -ldflags="-s -w" -o ~/bin/simplex-node`
- Размер: 20.4 MB → 14.7 MB (stripped)
- `/api/health` → `"build": "px-node-C41-C60"`

---

## 4. КЛЮЧЕВЫЕ ФАЙЛЫ ДЛЯ HERMES

### 4.1. Backend
| Файл | Назначение |
|------|-----------|
| `cmd/simplex-node/main.go` | Главный entry point, все routes, store init |
| `internal/store/token_store.go` | Token Store (CRUD + seed data) |
| `internal/store/extwallet_store.go` | External Wallet Store (CRUD) |
| `internal/api/token_wallet.go` | 5 token API handlers |
| `internal/api/external_wallet.go` | 5 external wallet API handlers |
| `internal/api/admin.go` | Админка, live dashboard (3447 строк в main.go) |
| `internal/api/nodeinfo.go` | Build version, system info |

### 4.2. Flutter
| Файл | Назначение |
|------|-----------|
| `apps/isle_app/lib/screens/wallet_screen.dart` | Wallet UI (5 expandable cards) |
| `apps/isle_app/lib/services/isle_api_service.dart` | API integration service |
| `apps/shared/api_client/lib/src/token_client.dart` | Token HTTP client |
| `apps/shared/api_client/lib/src/external_wallet_client.dart` | External wallet HTTP client |
| `apps/shared/models/lib/src/token.dart` | Token model |
| `apps/shared/models/lib/src/external_wallet.dart` | External wallet model |

### 4.3. Монитор
| Файл | Назначение |
|------|-----------|
| `node-monitor.py` | Системный трей-монитор (1239 строк) |
| `~/bin/node-monitor.py` | Старая копия (не используется) |

### 4.4. Инфраструктура
| Файл | Назначение |
|------|-----------|
| `docker/docker-compose.yml` | Docker стек |
| `docker/dashboard.html` | **SPA Dashboard (обновлён)**
| `scripts/backup-to-usb.sh` | Бекап на USB |
| `systemd/simplex-node.service` | systemd service |
| `install-pack/` | Инсталляционный пакет |

---

## 5. КАК СОБИРАТЬ И ЗАПУСКАТЬ

### 5.1. Backend (Go)
```bash
cd C:\PXNode
go build ./cmd/simplex-node/
# Бинарник: simplex-node.exe (Windows) или simplex-node (Linux)
```

### 5.2. Flutter (Windows клиент)
```bash
cd C:\PXNode\apps\isle_app
flutter pub get
flutter build windows --dart-define=API_URL=http://<node-ip>:8080
```

### 5.3. Flutter (Android APK)
```bash
cd C:\PXNode\apps\isle_app
flutter pub get
flutter build apk --debug --target-platform android-arm64
# требуется NDK 28.2+
```

### 5.4. Docker стек
```bash
cd C:\PXNode\docker
docker compose up -d
# Поднимает: smp-server, xftp, coturn, v2ray, tor
```

### 5.5. Монитор
```bash
python C:\PXNode\node-monitor.py
# Linux-only (GTK + AyatanaAppIndicator)
```

---

## 6. ЧТО ДЕЛАТЬ ДАЛЬШЕ

### Priority High

1. **Windows-клиент** — собрать `flutter build windows` с IsleApp
   - Убедиться что `API_URL=http://<сервер>:8080`
   - Слинковать с `v2ray/xray` для VPN-транспорта
   - Добавить Tor binary (expert bundle) для onion-routing

2. **Audit Dashboard** — реализовать audit-ui с expandable cards:
   - System Health → Disk, RAM, CPU, Uptime
   - Network → Hostname, IP, Onion addresses, API status
   - Services → Docker containers, systemd units
   - Wallet → Balance, transactions, token holdings
   - Economy → Silver spot price, reserve ratio, backing

3. **Wallet Evolution Phase II:**
   - Swap Tokens (token A → token B)
   - Wallet connect (Web3-style external wallet linking)
   - Token transfers between users
   - External wallet sync (watch-only mode)

4. **Тесты:**
   - `internal/store/token_store_test.go`
   - `internal/store/extwallet_store_test.go`
   - Flutter widget tests for wallet_screen.dart

### Priority Medium

5. **CI/CD** — GitHub Actions для автоматической сборки:
   - Go build + test
   - Flutter build web/android/windows
   - Docker image build

6. **ParanoidX Layer Monitor** в Flutter:
   - V2Ray health
   - Tor circuit status
   - Bridge status
   - Unified status dashboard

7. **Апдейт `app.html`** — embedded ARGENTUM mini-app:
   - Сейчас это "Liquid Taler on TON"
   - Может быть переиспользован для Royal UI

8. **API Docs auto-generation** — OpenAPI/Swagger из Go-кода

### Priority Low

9. **White-paper перевод** — docs/ на английский, испанский
10. **Island Bot enhancement** — telegram admin bot с командами
11. **Radio streaming** — плейлисты, Icecast управление через API

---

## 7. ЗАМЕТКИ ДЛЯ HERMES

### 7.1. Стиль кода
- Go: стандартный `gofmt`, без комментариев в коде (если не просили)
- Flutter/Dart: `flutter format`, mimick existing patterns
- Python: PEP8, но без докстрингов в monitor

### 7.2. Конвенции именования
- Go файлы: `snake_case.go`
- API handlers: `internal/api/<feature>.go`
- Store: `internal/store/<feature>_store.go`
- Flutter: `snake_case` для файлов, `CamelCase` для классов
- Routes: `/api/<feature>/<action>` (RESTful)

### 7.3. Важные замечания
- `go.sum` и `go.mod` — обновлять после добавления зависимостей
- Flutter `pubspec.lock` — НЕ включать в архив (тяжёлый, генерируется)
- Dashboard.html — не embedded в Go binary, читается с диска
- `node-monitor.py` — PID file блокировка, только один экземпляр
- В проекте есть pre-existing test failure (TestChatSendHandlerValidation)
- Monitor обновлён для Wayland (AyatanaAppIndicator3)

### 7.4. Полезные команды
```bash
# Go
go build ./cmd/simplex-node/     # сборка
go test ./internal/...           # тесты
go vet ./...                     # статический анализ

# Flutter
cd apps/isle_app && flutter pub get && flutter analyze

# Python monitor
python node-monitor.py           # запуск
kill $(cat ~/.local/share/simplex-node/node-monitor.pid)  # остановка

# Docker
cd docker && docker compose logs --tail=50 -f  # логи всех контейнеров
```

### 7.5. Ссылки и API endpoints
- **API Base:** `http://<host>:8080`
- **Health:** `GET /api/health`
- **Version:** `GET /api/version`
- **Dashboard:** `GET /` (читает dashboard.html с диска)
- **Tokens:** `GET/POST/PUT/DELETE /api/tokens`
- **Token Balances:** `GET/POST/PUT/DELETE /api/tokens/:id/balances`
- **External Wallets:** `GET/POST/PUT/DELETE /api/external-wallets`
- **Economy:** `GET /api/economy/oracle`
- **ParanoidX:** `GET /api/paranoidx/status`
- **Docs:** `GET /api/docs`

---

## 8. КОНТАКТЫ И ИСТОРИЯ

- **Проект:** Saint Mary Liberty Island — https://stmaria.org
- **Автор:** PerfectFriend / Tomás
- **Сервер:** torquemada (Linux, Ubuntu 24.04)
- **HDD путь:** `/home/tomas/simplex-node/`
- **USB backup:** `/run/media/tomas/SIMPLEX-USB/Projects/isle/simplex-node` (git remote "usb")
- **GitHub:** `https://github.com/PerfectFriend/simplex-node.git` (токен протух)

### История изменений (git log)
```
44aa571 Add token + external wallet Dart clients, models, and Flutter UI
4fad97a Initial restore from USB backup + token/external wallet evolution
```

### Версия билда
```
px-node-C41-C60
```
(C41-C60 = ~20 циклов разработки, эволюция от C41 до C60)

---

*Конец инструкции для Hermes. Удачи, агент!*
