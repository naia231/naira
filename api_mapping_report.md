# NasfamPay Security Audit: API & Authorization Mapping

## Overview
Following the static analysis of the frontend JavaScript bundles, we have successfully mapped the core API endpoints interacting with the custom backend hosted on Render (`https://nasfampay-backend.onrender.com`). We identified critical business logic pathways handling the processing and approval of cryptocurrency transactions, as well as administrative operations.

## Discovered API Endpoints

Through targeted analysis of the JS bundles (specifically `TonTransactions-DDDFQ8wk.js`, `SuiTransactions-Zcy4Rl6B.js`, and `adminPanel-SrgemToX.js`), we extracted the following primary API endpoints:

1. **Transaction Processing**
   - `POST /api/processTonTransactions`
   - `POST /api/approveTonTransactions`
   - `POST /api/processSuiTransactions`
   - `POST /api/approveSuiTransactions`

2. **Administrative & Platform State**
   - `POST /api/admin/updateLastSeen`
   - `POST /api/stocks`

## Authorization Model & Security Boundaries

### 1. Inconsistent Authentication Headers
The analysis revealed a potentially critical vulnerability in how authorization is handled across different API endpoints. 

> [!WARNING]
> The transaction processing endpoints (`processTonTransactions`, `approveTonTransactions`, `processSuiTransactions`, `approveSuiTransactions`) **do not append a Firebase Bearer token** to the request headers. 

Instead, they rely solely on:
- `X-Firebase-AppCheck` header (AppCheck Token)
- The `adminId` included in the JSON payload (e.g., `{"adminId": "user_id_here", "transaction": { ... } }`)

In contrast, non-transaction endpoints like `/api/admin/updateLastSeen` and `/api/stocks` properly fetch and transmit the Firebase user token (`Authorization: Bearer <token>`).

**Exploitation Scenario:** If the backend does not enforce backend-side Firebase token validation for transaction processing routes (because the frontend doesn't send it), an attacker who can acquire a valid AppCheck token could potentially execute unauthorized approvals by forging an arbitrary `adminId` and transaction payload.

### 2. Live Probe Results (Endpoint Availability)
To validate the API surface, we conducted automated dynamic probing against the identified routes on the live server:

- **`/api/stocks`**: Returned `{"error":"App Check token missing"}`. This confirms the endpoint is active and validating the AppCheck header as the first line of defense.
- **`/api/admin/updateLastSeen`**: Returned `{"error":"App Check token missing"}`. Confirms activity.
- **`/api/processTonTransactions`** and **`/api/approveTonTransactions`**: Returned a `404 Cannot POST` HTML response from the Express.js server. 

> [!NOTE]
> The `Cannot POST` responses on the transaction endpoints suggest that these routes are either currently disabled/removed on the live backend, have been renamed, or are blocked at a proxy level, despite being actively referenced in the current production frontend code.

## Next Steps

1. **AppCheck Token Acquisition**: Develop a method to retrieve or intercept a valid `X-Firebase-AppCheck` token from a legitimate browser session. This will allow us to bypass the initial WAF/AppCheck barrier and probe deeper into the backend validation logic.
2. **Payload Fuzzing**: Once an AppCheck token is acquired, send forged requests to `/api/stocks` and `/api/admin/updateLastSeen` to determine if the backend correctly validates the Firebase Auth Bearer token and permissions.
3. **Firestore Interaction Analysis**: Expand the search to direct Firestore operations (`addDoc`, `updateDoc`) performed from the client side, which might be bypassing the Render backend entirely for certain transaction state changes.
