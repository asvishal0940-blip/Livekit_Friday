# Telnyx Phone Calling Setup Guide

## ✅ What's Changed

You've switched from **Twilio** to **Telnyx** for phone calling.

**Benefits:**
- ✓ No trial restrictions
- ✓ Can call any valid international phone number
- ✓ No verification requirements
- ✓ Better international coverage
- ✓ Pay-as-you-go pricing

---

## 🔧 Your Telnyx Configuration

Your credentials are already set up in `.env`:

```
TELNYX_API_KEY=KEY01A04C5C66D1DC774D48EA1FFF68E378_2ZQPaQDDnKixCn5eS0Hd8l
TELNYX_PHONE_NUMBER=+14092322515
```

---

## ⚠️ Important Setup Steps

Before making calls, you **must** complete these steps:

### Step 1: Create a Telnyx Connection

1. Go to https://portal.telnyx.com/
2. Sign in with your account
3. Navigate to **Connections** → **Voice**
4. Click **Create Connection**
5. Fill in:
   - **Connection Name**: `Friday Agent`
   - **Type**: `Outbound Call Control`
6. Save the connection
7. You'll need the **Connection ID** later

### Step 2: Configure Your Phone Number

1. Go to **Phone Numbers** in your Telnyx dashboard
2. Click on your phone number: `+14092322515`
3. Find the **Voice Settings** section
4. Select the connection you created above
5. Make sure **Outbound Calling** is enabled
6. Save the settings

### Step 3: Update Code with Connection ID (Optional)

If you have a specific connection ID, update [tools.py](tools.py):

Find this line:
```python
connection_id=None,  # Uses default connection
```

Replace with:
```python
connection_id="your-connection-id",  # Your Telnyx connection
```

---

## 📱 Test a Call

Once configured, try calling:

**Test 1: Call yourself**
```
User: "Call Myself"
Friday calls: +14092322515 (your Telnyx number)
```

**Test 2: Call a contact**
```
User: "Call Dad"
Friday calls: +919942320940 (from contacts.py)
Result: Call should connect
```

---

## 🧪 Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| "No Telnyx connection configured" | No connection in Telnyx account | Create a Voice connection in dashboard |
| "API Key authentication failed" | Wrong API key | Check TELNYX_API_KEY in .env |
| "Invalid phone number" | Phone number format is wrong | Use international format: +country-code... |
| Call doesn't connect | Phone number doesn't have voice enabled | Enable voice calling in Telnyx dashboard |

---

## 💰 Pricing

Telnyx pricing is **pay-as-you-go**:

- Inbound calls: Usually included
- Outbound calls: ~$0.0125 per minute (varies by destination)
- Outbound SMS: ~$0.0075 per message

View your usage at: https://portal.telnyx.com/billing

---

## 🔐 Security

Your API key is sensitive:
- ✓ Never share it publicly
- ✓ Never commit it to GitHub
- ✓ Keep it in `.env` (which is in `.gitignore`)

---

## ✨ Next Steps

1. ✓ Credentials configured (.env is set up)
2. → Create a Telnyx Voice Connection (dashboard)
3. → Configure your phone number
4. → Test calling

Once you complete steps 2-3, calling will work!

---

## Quick Links

- **Telnyx Dashboard**: https://portal.telnyx.com/
- **Telnyx Docs**: https://developers.telnyx.com/docs
- **API Reference**: https://developers.telnyx.com/docs/api/v2/overview
- **Pricing**: https://telnyx.com/pricing

---

## Need Help?

Check your agent logs for specific error messages. Each error will tell you exactly what to fix!

Common commands to test:
- "Call Dad"
- "Call Dharsan"
- "Call a friend"

Enjoy! 🎉
