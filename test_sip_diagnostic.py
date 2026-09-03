"""
Diagnostic script to test SIP configuration and phone calling setup.
Run this to verify your LiveKit SIP trunk is working.
"""

import os
import asyncio
from dotenv import load_dotenv
from livekit import api

load_dotenv()

def check_env():
    """Check if all required environment variables are set."""
    print("=" * 60)
    print("ENVIRONMENT CONFIGURATION CHECK")
    print("=" * 60)
    
    livekit_url = os.getenv("LIVEKIT_URL")
    livekit_key = os.getenv("LIVEKIT_API_KEY")
    livekit_secret = os.getenv("LIVEKIT_API_SECRET")
    sip_trunk = os.getenv("LIVEKIT_SIP_OUTBOUND_TRUNK") or os.getenv("SIP_OUTBOUND_TRUNK_ID")
    
    print(f"✓ LIVEKIT_URL: {livekit_url}")
    print(f"✓ LIVEKIT_API_KEY: {livekit_key[:10]}..." if livekit_key else "✗ LIVEKIT_API_KEY: NOT SET")
    print(f"✓ LIVEKIT_API_SECRET: {livekit_secret[:10]}..." if livekit_secret else "✗ LIVEKIT_API_SECRET: NOT SET")
    print(f"✓ SIP_OUTBOUND_TRUNK: {sip_trunk}" if sip_trunk else "✗ SIP_OUTBOUND_TRUNK: NOT SET")
    
    if not all([livekit_url, livekit_key, livekit_secret, sip_trunk]):
        print("\n❌ MISSING REQUIRED ENV VARIABLES - Phone calling won't work!")
        return False
    
    print("\n✓ All environment variables are set.")
    return True


def check_phone_numbers():
    """Check phone numbers in contacts."""
    print("\n" + "=" * 60)
    print("CONTACT PHONE NUMBERS CHECK")
    print("=" * 60)
    
    try:
        from contacts import CONTACTS
        
        for name, contact in CONTACTS.items():
            phone = contact.get("phone", "")
            relation = contact.get("relation", "")
            
            # Validate format
            if phone.startswith("+") and phone[1:].replace("-", "").isdigit():
                status = "✓"
            else:
                status = "✗"
            
            print(f"{status} {name:15} | {phone:20} | {relation}")
        
        return True
    except ImportError:
        print("✗ contacts.py not found!")
        return False


def check_sip_trunk_format():
    """Check if SIP trunk ID looks valid."""
    print("\n" + "=" * 60)
    print("SIP TRUNK FORMAT CHECK")
    print("=" * 60)
    
    sip_trunk = os.getenv("LIVEKIT_SIP_OUTBOUND_TRUNK") or os.getenv("SIP_OUTBOUND_TRUNK_ID")
    
    if not sip_trunk:
        print("✗ No SIP trunk configured")
        return False
    
    # LiveKit SIP trunks typically start with ST_
    if sip_trunk.startswith("ST_"):
        print(f"✓ SIP trunk looks valid: {sip_trunk}")
        print("\nSIP Trunk Details:")
        print(f"  - ID: {sip_trunk}")
        print(f"  - Format: LiveKit Standard")
        print("\n⚠️  Important: Your SIP trunk must be configured in your LiveKit dashboard")
        print("    to route calls to actual phone numbers. Without proper routing rules,")
        print("    all calls will timeout.")
        return True
    else:
        print(f"⚠️  SIP trunk doesn't start with ST_: {sip_trunk}")
        print("   This might be a custom SIP provider. Verify it's correct in your config.")
        return True


def main():
    """Run all diagnostics."""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  SIP PHONE CALLING DIAGNOSTIC SCRIPT".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    
    results = []
    
    # Run checks
    results.append(("Environment", check_env()))
    results.append(("Phone Numbers", check_phone_numbers()))
    results.append(("SIP Trunk Format", check_sip_trunk_format()))
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    for check_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {check_name}")
    
    print("\n" + "=" * 60)
    print("NEXT STEPS IF CALLS ARE TIMING OUT (408 error):")
    print("=" * 60)
    print("""
1. Verify the phone numbers are REACHABLE:
   - Test calling the numbers from your personal phone first
   - Check if numbers are active and can receive calls
   
2. Verify SIP Trunk is properly configured:
   - Go to your LiveKit dashboard
   - Check SIP -> Trunks -> ST_b4dvoXocwQcc
   - Verify the trunk has the correct routing rules
   - Make sure the trunk is active/enabled
   
3. Test with a simple destination first:
   - Try calling a test SIP URI instead of a regular phone number
   - Format: sip:+919942320940@your-provider.com
   
4. Check LiveKit logs:
   - Review your LiveKit cloud logs for detailed SIP error messages
   - They may show why the SIP trunk is rejecting the call
   
5. Contact LiveKit support:
   - The 408 timeout suggests the SIP trunk isn't routing properly
   - They can help verify your trunk configuration
""")
    
    print("=" * 60)


if __name__ == "__main__":
    main()
