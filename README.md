# SteamTradeHandler 

This repository automates Steam trading processes. It provides methods to log in to Steam, manage encrypted credentials, and handle trade offers. 
This project is designed as a helper for automating Steam trades, including accepting incoming offers with optional filters (e.g., gifts only).

**This is an older project, so the code may be messy and lacks full documentation—but it was a valuable learning experience in automating Steam trading processes.**

## Key Features:
- **Automated Steam Trading**: Fetch, accept, and manage Steam trade offers.
- **Secure Credential Handling**: Encrypt and decrypt Steam credentials for secure account management.
- **Trade Offer Management**: Accept, decline, and process trade offers with support for state checks and filters.
- **Factory Methods**: Create Steam accounts from encrypted data or files.

## File Overview:

### `SteamTradeHandler.py`

  - Logs into Steam using encrypted credentials.
  - Encrypts and decrypts sensitive data (password, API key, secrets).
  - Supports creating accounts from encrypted data or files.  
  - Retrieves incoming and outgoing trade offers as `TradeOffer` objects.


### `TradeOffer.py`
- Represents individual Steam trade offers.
- Provides methods to:
  - Accept or decline trade offers.
  - Identify gifts (offers where no items are given in return).
  - Parse and track offer details (items, trade state, partner info).
