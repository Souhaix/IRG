# Setup — Variables d'environnement requises

Copier `.env.example` → `.env` et remplir toutes les valeurs ci-dessous.

---

## Google Ads

| Variable | Description |
|---|---|
| `GOOGLE_ADS_DEVELOPER_TOKEN` | Developer token du compte MCC (Outils → Centre API) |
| `GOOGLE_ADS_CLIENT_ID` | OAuth2 Client ID (Google Cloud Console → Credentials) |
| `GOOGLE_ADS_CLIENT_SECRET` | OAuth2 Client Secret |
| `GOOGLE_ADS_REFRESH_TOKEN` | OAuth2 Refresh Token (généré via `generate_refresh_token.py` du SDK) |
| `GOOGLE_ADS_LOGIN_CUSTOMER_ID` | Customer ID du MCC, sans tirets (ex: `1234567890`) |
| `GOOGLE_ADS_VOSKER_CA_EN` | Customer ID — Vosker - CA-EN |
| `GOOGLE_ADS_VOSKER_QUEBEC` | Customer ID — Vosker - Québec |
| `GOOGLE_ADS_VOSKER_PRODUCTS` | Customer ID — Vosker Products |
| `GOOGLE_ADS_SPYPOINT_MAIN` | Customer ID — SPYPOINT Google Ads |
| `GOOGLE_ADS_SPYPOINT_QUEBEC` | Customer ID — Spypoint - Québec |
| `GOOGLE_ADS_SPYPOINT_CA_EN` | Customer ID — Spypoint - CA-EN |

**Permissions :** Le developer token doit avoir accès en lecture à tous ces customer IDs via le MCC.

---

## Meta (Facebook) Ads

| Variable | Description |
|---|---|
| `FACEBOOK_ACCESS_TOKEN` | System User Token long-lived avec permission `ads_read` sur les 4 comptes |
| `FACEBOOK_VOSKER_MAIN` | Ad Account ID — Vosker (format `act_XXXXXXXXX`) |
| `FACEBOOK_VOSKER_QUEBEC` | Ad Account ID — Vosker - Québec |
| `FACEBOOK_SPYPOINT_MAIN` | Ad Account ID — SPYPOINT |
| `FACEBOOK_SPYPOINT_QUEBEC` | Ad Account ID — Spypoint - Québec |

**Permissions :** System User → Business Settings → Assign Assets → `ads_read` sur chaque compte.

---

## Microsoft (Bing) Ads

| Variable | Description |
|---|---|
| `MICROSOFT_ADS_CLIENT_ID` | Azure AD App Registration Client ID |
| `MICROSOFT_ADS_CLIENT_SECRET` | Azure AD App Secret |
| `MICROSOFT_ADS_REFRESH_TOKEN` | OAuth2 Refresh Token (scope `msads.manage`) |
| `MICROSOFT_ADS_DEVELOPER_TOKEN` | Developer Token (Microsoft Advertising → Outils) |
| `MICROSOFT_ADS_VOSKER` | Account ID — Vosker Security |
| `MICROSOFT_ADS_SPYPOINT` | Account ID — SPYPOINT |

**Permissions :** Azure AD App → API Permissions → `https://ads.microsoft.com/msads.manage`.

---

## TikTok Ads

| Variable | Description |
|---|---|
| `TIKTOK_ACCESS_TOKEN` | Long-lived Access Token avec scope Reporting |
| `TIKTOK_VOSKER_ADVERTISER_ID` | Advertiser ID — Vosker |

**Permissions :** App TikTok Marketing API → scope Ad Account Management (read) ou Reporting.

---

## SharePoint / Microsoft Graph

| Variable | Description |
|---|---|
| `SHAREPOINT_TENANT_ID` | Azure AD Tenant ID |
| `SHAREPOINT_CLIENT_ID` | Azure AD App Client ID (peut être la même app ou une dédiée) |
| `SHAREPOINT_CLIENT_SECRET` | Azure AD App Secret |
| `SHAREPOINT_SITE_NAME` | Nom du site SharePoint (tel qu'il apparaît dans l'URL) |
| `SHAREPOINT_DRIVE_ID` | ID du Document Library (optionnel si un seul drive) |
| `SHAREPOINT_FILE_PATH` | Chemin complet du fichier Excel dans le drive |

**Permissions :** `Sites.ReadWrite.All` (application permission) + admin consent.

---

## Excel Mapping

Copier `excel_mapping.template.json` → `excel_mapping.json` et remplir :
- noms exacts des onglets
- libellés exacts des lignes
- emplacement et format des dates
- colonne des libellés
