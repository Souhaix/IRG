# Daily Budget Pacing Automation (Local Playwright + TypeScript)

This project runs **locally** with Playwright and persistent browser profiles, collects yesterday spend from TikTok Ads, Google Ads, Facebook Ads, and Microsoft Ads, computes brand totals (Vosker and SpyPoint), and optionally writes final values to an Excel-for-Web file on SharePoint.

## Key design goals

- Local-only runtime (no cloud workflow dependency).
- Persistent browser profile/session reuse.
- Modular per-platform collectors.
- Strict uncertainty handling (stop instead of guess).
- Controlled retry policy:
  - Google Ads: max 1 refresh/account
  - Microsoft Ads: max 1 reconnect flow
  - Facebook Ads: one primary + one fallback path
- Write to SharePoint **only after all values are collected successfully**.
- Dry-run mode for safe testing.
- Structured logging + error artifacts.

## Project structure

```text
.
├── src
│   ├── config
│   │   ├── accounts.ts
│   │   └── env.ts
│   ├── platforms
│   │   ├── common.ts
│   │   ├── facebookAds.ts
│   │   ├── googleAds.ts
│   │   ├── microsoftAds.ts
│   │   └── tiktok.ts
│   ├── sharepoint
│   │   └── writer.ts
│   ├── types
│   │   └── index.ts
│   ├── utils
│   │   ├── browser.ts
│   │   ├── date.ts
│   │   ├── errors.ts
│   │   ├── logger.ts
│   │   └── normalize.ts
│   ├── index.ts
│   └── testSelectors.ts
├── logs/
├── screenshots/
├── .env.example
├── package.json
├── tsconfig.json
└── README.md
```

## Setup

1. Install Node.js 20+.
2. Install dependencies:

```bash
npm install
npx playwright install
```

3. Copy env template:

```bash
cp .env.example .env
```

4. Edit `.env` values:
- `BROWSER_PROFILE_PATH`: local persistent profile folder.
- `HEADLESS`: set to `false` for first-time auth.
- `SHAREPOINT_URL`: your final SharePoint Excel URL.
- Optional `TARGET_DATE_OVERRIDE=YYYY-MM-DD` for manual testing.

## Commands

- **Dry run (collect + compute only):**

```bash
npm run dry
```

- **Write mode (collect + compute + SharePoint write at end):**

```bash
npm run run
```

- **Selector checks (platform helper):**

```bash
npm run test:selectors
```

## Runtime behavior

### Date handling

- Target date is always **local yesterday** (`new Date() - 1 day`) unless override is set.
- URL dates are ignored.
- Each platform module attempts to enforce/verify date in the UI.

### Platform collection

- TikTok: reads cost from `Total of X campaigns` row.
- Google Ads: enforces yesterday, reads `Cost`, allows one refresh/account.
- Facebook Ads: avoids unreliable campaign total; tries account summary primary then one fallback report route.
- Microsoft Ads: reads `Vosker Security` and `SPYPOINT` values from overview; allows one reconnect.

### SharePoint write

- Runs only in write mode and only after all reads succeeded.
- Finds sheet tabs:
  - `VK [MON] [YEAR] Budget Pacing`
  - `SP [MON] [YEAR] Budget Pacing`
- Finds date column by configured date row:
  - VK row 13
  - SP row 11
- Writes only required mapped rows, with row+label verification.
- Waits for autosave confirmation before exit.

## Error handling and artifacts

On unrecoverable failure, the workflow:
1. Captures full-page screenshot in `screenshots/`.
2. Stores structured error JSON in `logs/error-YYYY-MM-DD.json`.
3. Includes current URL + module/action context.
4. Exits non-zero.

## How to refresh selectors when UIs change

1. Run `npm run test:selectors` while logged in.
2. Inspect which selectors fail (`visible: false`).
3. Update selectors in the corresponding platform module:
   - `src/platforms/tiktok.ts`
   - `src/platforms/googleAds.ts`
   - `src/platforms/facebookAds.ts`
   - `src/platforms/microsoftAds.ts`
4. Re-run selector tests.
5. Validate with `npm run dry` before `npm run run`.

## Notes

- Europe accounts are not configured and therefore ignored.
- Currency labels are preserved in logs while SharePoint writes plain numeric values.
- First run should be non-headless to manually complete login and persist sessions.
