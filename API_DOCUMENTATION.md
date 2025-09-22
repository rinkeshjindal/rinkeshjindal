# 🏦 Bank API Documentation

This document provides detailed information about the official APIs available for each supported Indian bank and the information needed to access them.

## 📋 **Overview**

The India Bank Checker application integrates with official APIs from four major Indian banks:
- **ICICI Bank** - iMobile API
- **Axis Bank** - Developer Portal API
- **Yes Bank** - Developer Hub API
- **HDFC Bank** - Developer Portal API

---

## 🏦 **1. ICICI Bank API**

### **Official Documentation**
- **Developer Portal:** https://developer.icicibank.com/
- **API Documentation:** https://developer.icicibank.com/docs
- **Base URL:** `https://api.icicibank.com`
- **API Version:** v1

### **Required Credentials**
```json
{
  "api_key": "Your ICICI Bank API Key",
  "client_id": "Your Client ID",
  "client_secret": "Your Client Secret",
  "customer_id": "Your Customer ID",
  "username": "Your Internet Banking Username",
  "password": "Your Internet Banking Password"
}
```

### **Available Endpoints**
| Endpoint | Method | Description | Required Scopes |
|----------|--------|-------------|-----------------|
| `/api/v1/accounts` | GET | Get all accounts | `account.read` |
| `/api/v1/accounts/{accountId}/balance` | GET | Get account balance | `account.read` |
| `/api/v1/accounts/{accountId}/transactions` | GET | Get transactions | `transaction.read` |
| `/api/v1/fixed-deposits` | GET | Get fixed deposits | `fd.read` |
| `/api/v1/loans` | GET | Get loan information | `loan.read` |

### **Authentication Method**
- **Type:** OAuth 2.0 with API Key
- **Flow:** Client Credentials + Resource Owner Password
- **Token Endpoint:** `/oauth/token`

### **Sample API Call**
```bash
curl -X GET "https://api.icicibank.com/api/v1/accounts" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json"
```

---

## 🏦 **2. Axis Bank API**

### **Official Documentation**
- **Developer Portal:** https://developer.axisbank.com/
- **API Documentation:** https://developer.axisbank.com/docs
- **Base URL:** `https://api.axisbank.com`
- **API Version:** v1

### **Required Credentials**
```json
{
  "api_key": "Your Axis Bank API Key",
  "client_id": "Your Client ID",
  "client_secret": "Your Client Secret",
  "merchant_id": "Your Merchant ID",
  "username": "Your Internet Banking Username",
  "password": "Your Internet Banking Password"
}
```

### **Available Endpoints**
| Endpoint | Method | Description | Required Scopes |
|----------|--------|-------------|-----------------|
| `/api/v1/account/balance` | GET | Get account balance | `account.read` |
| `/api/v1/account/statement` | GET | Get account statement | `transaction.read` |
| `/api/v1/fixed-deposits` | GET | Get FD details | `fd.read` |
| `/api/v1/credit-cards` | GET | Get credit card info | `creditcard.read` |

### **Authentication Method**
- **Type:** API Key + OAuth 2.0
- **Flow:** Authorization Code + Client Credentials
- **Token Endpoint:** `/oauth2/token`

### **Sample API Call**
```bash
curl -X GET "https://api.axisbank.com/api/v1/account/balance" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "X-Merchant-ID: YOUR_MERCHANT_ID" \
  -H "Content-Type: application/json"
```

---

## 🏦 **3. Yes Bank API**

### **Official Documentation**
- **Developer Hub:** https://developer.yesbank.in/
- **API Documentation:** https://developer.yesbank.in/docs
- **Base URL:** `https://api.yesbank.in`
- **API Version:** v1

### **Required Credentials**
```json
{
  "api_key": "Your Yes Bank API Key",
  "client_id": "Your Client ID",
  "client_secret": "Your Client Secret",
  "merchant_code": "Your Merchant Code",
  "username": "Your Internet Banking Username",
  "password": "Your Internet Banking Password"
}
```

### **Available Endpoints**
| Endpoint | Method | Description | Required Scopes |
|----------|--------|-------------|-----------------|
| `/api/v1/accounts/balance` | GET | Get account balance | `account.read` |
| `/api/v1/accounts/statement` | GET | Get account statement | `transaction.read` |
| `/api/v1/deposits/fixed` | GET | Get fixed deposits | `fd.read` |
| `/api/v1/loans` | GET | Get loan information | `loan.read` |

### **Authentication Method**
- **Type:** API Key + JWT Token
- **Flow:** Client Credentials + JWT
- **Token Endpoint:** `/oauth2/token`

### **Sample API Call**
```bash
curl -X GET "https://api.yesbank.in/api/v1/accounts/balance" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "X-Merchant-Code: YOUR_MERCHANT_CODE" \
  -H "Content-Type: application/json"
```

---

## 🏦 **4. HDFC Bank API**

### **Official Documentation**
- **Developer Portal:** https://developer.hdfcbank.com/
- **API Documentation:** https://developer.hdfcbank.com/docs
- **Base URL:** `https://api.hdfcbank.com`
- **API Version:** v1

### **Required Credentials**
```json
{
  "api_key": "Your HDFC Bank API Key",
  "client_id": "Your Client ID",
  "client_secret": "Your Client Secret",
  "merchant_id": "Your Merchant ID",
  "username": "Your Internet Banking Username",
  "password": "Your Internet Banking Password"
}
```

### **Available Endpoints**
| Endpoint | Method | Description | Required Scopes |
|----------|--------|-------------|-----------------|
| `/api/v1/account/balance` | GET | Get account balance | `account.read` |
| `/api/v1/account/statement` | GET | Get account statement | `transaction.read` |
| `/api/v1/fixed-deposits` | GET | Get FD details | `fd.read` |
| `/api/v1/credit-cards` | GET | Get credit card info | `creditcard.read` |

### **Authentication Method**
- **Type:** API Key + OAuth 2.0
- **Flow:** Authorization Code + Client Credentials
- **Token Endpoint:** `/oauth2/token`

### **Sample API Call**
```bash
curl -X GET "https://api.hdfcbank.com/api/v1/account/balance" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "X-Merchant-ID: YOUR_MERCHANT_ID" \
  -H "Content-Type: application/json"
```

---

## 🔑 **How to Get API Access**

### **Step 1: Register as a Developer**
1. Visit each bank's developer portal
2. Create a developer account with your business email
3. Complete KYC verification process
4. Submit your business use case and requirements

### **Step 2: Create Application**
1. Create a new application in the developer portal
2. Select required API scopes:
   - `account.read` - Read account information
   - `transaction.read` - Read transaction history
   - `fd.read` - Read fixed deposit information
3. Get your API credentials (API Key, Client ID, Client Secret)

### **Step 3: Sandbox Testing**
1. Use sandbox environment for initial testing
2. Test with sample data provided by the bank
3. Verify API responses and data formats
4. Test authentication flows

### **Step 4: Production Access**
1. Submit application for production approval
2. Complete security review and compliance checks
3. Get production API keys and credentials
4. Update your application with production endpoints

---

## 📊 **API Response Formats**

### **Account Balance Response**
```json
{
  "status": "success",
  "data": {
    "accounts": [
      {
        "account_number": "1234567890",
        "account_type": "Savings",
        "balance": 50000.00,
        "currency": "INR",
        "last_updated": "2024-01-15T10:30:00Z"
      }
    ]
  }
}
```

### **Fixed Deposit Response**
```json
{
  "status": "success",
  "data": {
    "fixed_deposits": [
      {
        "fd_number": "FD123456",
        "principal_amount": 100000.00,
        "interest_rate": 6.5,
        "maturity_date": "2025-01-15",
        "maturity_amount": 106500.00,
        "days_to_maturity": 365
      }
    ]
  }
}
```

---

## ⚠️ **Important Notes**

### **Security Requirements**
- All API calls must use HTTPS
- API keys must be stored securely
- Never expose credentials in client-side code
- Use environment variables for sensitive data

### **Rate Limits**
- Each bank has different rate limits
- Typical limits: 100-1000 requests per hour
- Implement proper rate limiting in your application

### **Compliance**
- Ensure compliance with RBI guidelines
- Follow data protection regulations
- Implement proper audit logging
- Use only for legitimate business purposes

### **Error Handling**
- Implement proper error handling for all API calls
- Handle authentication failures gracefully
- Log all API errors for debugging
- Implement retry logic for transient failures

---

## 🔧 **Configuration Setup**

### **Environment Variables**
Create a `.env` file with your API credentials:

```bash
# ICICI Bank
ICICI_API_KEY=your_icici_api_key
ICICI_CLIENT_ID=your_icici_client_id
ICICI_CLIENT_SECRET=your_icici_client_secret
ICICI_CUSTOMER_ID=your_icici_customer_id

# Axis Bank
AXIS_API_KEY=your_axis_api_key
AXIS_CLIENT_ID=your_axis_client_id
AXIS_CLIENT_SECRET=your_axis_client_secret
AXIS_MERCHANT_ID=your_axis_merchant_id

# Yes Bank
YES_API_KEY=your_yes_api_key
YES_CLIENT_ID=your_yes_client_id
YES_CLIENT_SECRET=your_yes_client_secret
YES_MERCHANT_CODE=your_yes_merchant_code

# HDFC Bank
HDFC_API_KEY=your_hdfc_api_key
HDFC_CLIENT_ID=your_hdfc_client_id
HDFC_CLIENT_SECRET=your_hdfc_client_secret
HDFC_MERCHANT_ID=your_hdfc_merchant_id
```

### **Testing**
Use the sandbox environments provided by each bank for testing before moving to production.

---

## 📞 **Support and Resources**

### **Bank Support Contacts**
- **ICICI Bank:** developer-support@icicibank.com
- **Axis Bank:** api-support@axisbank.com
- **Yes Bank:** developer-support@yesbank.in
- **HDFC Bank:** api-support@hdfcbank.com

### **Additional Resources**
- [RBI API Guidelines](https://www.rbi.org.in/Scripts/BS_ViewMas.aspx?Id=10487)
- [Open Banking Standards](https://www.openbanking.org.uk/)
- [API Security Best Practices](https://owasp.org/www-project-api-security/)