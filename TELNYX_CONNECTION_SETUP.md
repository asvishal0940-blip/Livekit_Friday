# Telnyx Connection Setup - Step by Step

## 🎯 What You Need to Do

Telnyx requires a **Call Control App** with a valid webhook URL to make phone calls.

Don't worry - we'll set this up in 5 minutes!

---

## Step 1: Create a Call Control App in Telnyx Dashboard

1. Go to https://portal.telnyx.com/
2. Sign in with your account
3. In the left sidebar, find **"Call Control"** → **"Applications"**
4. Click **"Create a new application"**

---

## Step 2: Configure the Call Control App

Fill in the following:

### **Application Name**
```
Friday Voice Agent
```

### **Connection Type**
Select: **"Call Control (REST API)"**

### **Webhook URL** (Important!)
For testing, use this temporary URL:
```
https://webhook.site/unique-id
```

**To get a unique webhook URL:**
- Go to https://webhook.site/
- Copy your unique URL (looks like: `https://webhook.site/12345678-1234-1234-1234-123456789abc`)
- Paste it in the Telnyx application form

### **Webhook Events** (Enable all of these)
Check all the boxes:
- ☑ Call initiated
- ☑ Call answered
- ☑ Call hangup
- ☑ Call machine detection
- ☑ Digit pressed

### **Outbound Voice Profile**
- Select: Any available voice profile (or create a new one)

### **Save the Application**

---

## Step 3: Get Your Connection ID

1. After saving, you'll see your new application
2. Look for the **Connection ID** field (starts with `tc_` or similar)
3. **Copy this ID** - you'll need it in the next step

Example Connection ID:
```
tc_1234567890abcdef
```

---

## Step 4: Add Connection ID to Your Project

Update your `.env` file:

```
TELNYX_API_KEY=KEY01A04C5C66D1DC774D48EA1FFF68E378_2ZQPaQDDnKixCn5eS0Hd8l
TELNYX_PHONE_NUMBER=+14092322515
TELNYX_CONNECTION_ID=tc_your_connection_id_here
```

Replace `tc_your_connection_id_here` with your actual Connection ID.

---

## Step 5: Update Code to Use Connection ID

Update [tools.py](tools.py) line ~155:

Find this:
```python
"connection_id": None,  # Uses default or first connection
```

Change to:
```python
"connection_id": os.getenv("TELNYX_CONNECTION_ID"),
```

---

## 🧪 Test the Connection

Once you've completed the steps above, try calling:

```
User: "Call Mom"
Friday: "Calling Mom now..."
✓ Call should go through!
```

---

## ❓ Need a Webhook?

If you don't want to use webhook.site, here are alternatives:

### Option 1: Use webhook.site (Easiest - No setup needed)
- Go to https://webhook.site/
- Get a free temporary URL
- Use it in Telnyx (valid for 48 hours)

### Option 2: Use ngrok (For production testing)
1. Install ngrok: https://ngrok.com/
2. Run: `ngrok http 8080`
3. Copy the ngrok URL (e.g., `https://abc123.ngrok.io`)
4. Use that in Telnyx

### Option 3: Set up a real server
- Deploy a webhook receiver to receive call events
- Configure it in Telnyx

For now, **webhook.site is the easiest** for testing!

---

## 📋 Checklist

- [ ] Create Call Control App in Telnyx
- [ ] Configure webhook URL (use webhook.site)
- [ ] Enable webhook events
- [ ] Copy Connection ID
- [ ] Add to .env file: `TELNYX_CONNECTION_ID=tc_...`
- [ ] Update [tools.py](tools.py) to use the Connection ID
- [ ] Test: "Call Mom"

---

## Troubleshooting

| Error | Solution |
|-------|----------|
| "connection_id is invalid" | Check you copied the Connection ID correctly |
| "webhook URL is invalid" | Use https://webhook.site/ for a valid URL |
| "Call Control App not found" | Make sure the app is saved and Connection ID matches |

---

## Next Steps

1. ✓ Create Call Control App
2. ✓ Get Connection ID
3. → Add to .env
4. → Update code
5. → Test calling

Once done, let me know the Connection ID and I'll update your .env and code! 🚀
