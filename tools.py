import logging
import uuid
from livekit.agents import function_tool, RunContext, get_job_context
import requests
import os
import smtplib
from datetime import datetime, timedelta, timezone
from email.mime.multipart import MIMEMultipart  
from email.mime.text import MIMEText
from typing import Optional

try:
    from zoneinfo import ZoneInfo
except ImportError:
    ZoneInfo = None


def _india_timezone():
    if ZoneInfo is not None:
        try:
            return ZoneInfo("Asia/Kolkata")
        except Exception:
            pass
    return timezone(timedelta(hours=5, minutes=30))


@function_tool()
async def get_current_datetime(
    context: RunContext,  # type: ignore
) -> str:
    """Get the current date and time in Vishal's local timezone, Asia/Kolkata."""
    current = datetime.now(_india_timezone())
    return current.strftime("%A, %d %B %Y, %I:%M:%S %p IST")

@function_tool()
async def list_events(
    context: RunContext,  # type: ignore
    date: str,
) -> str:
    """Get all scheduled events for a date in YYYY-MM-DD format."""
    try:
        requested_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        return "Invalid date. Use YYYY-MM-DD format."

    if requested_date == datetime.now().date():
        return "You have one event: 'Project Sync' at 2:00 PM for 30 minutes."
    return "Your calendar is completely clear on this day."

@function_tool()
async def create_event(
    context: RunContext,  # type: ignore
    title: str,
    start_time: str,
    duration_minutes: int,
) -> str:
    """Create a calendar event using an ISO 8601 start time."""
    try:
        datetime.fromisoformat(start_time.replace("Z", "+00:00"))
    except ValueError:
        return "Invalid start time. Use an ISO 8601 date-time format."

    if duration_minutes <= 0:
        return "Duration must be greater than zero minutes."

    return f"Successfully scheduled '{title}' for {start_time}."

def validate_phone_call_config() -> str | None:
    """Validate Telnyx configuration for phone calling."""
    api_key = os.getenv("TELNYX_API_KEY")
    from_number = os.getenv("TELNYX_PHONE_NUMBER")
    
    if not api_key:
        return "Telnyx API Key not configured. Set TELNYX_API_KEY in environment."
    if not from_number:
        return "Telnyx phone number not configured. Set TELNYX_PHONE_NUMBER in environment."
    
    return None


def validate_phone_number(phone_number: str) -> tuple[bool, str]:
    """Validate phone number format and return (is_valid, message)."""
    clean = str(phone_number).strip()
    
    if not clean:
        return False, "Phone number is empty."
    
    # Allow SIP URIs
    if clean.startswith("sip:"):
        return True, f"Valid SIP URI: {clean}"
    
    # Allow +country-code format
    if clean.startswith("+"):
        if not clean[1:].replace("-", "").replace(" ", "").isdigit():
            return False, f"Phone number contains invalid characters: {clean}"
        if len(clean.replace("-", "").replace(" ", "")) < 10:
            return False, f"Phone number too short: {clean} (minimum 10 digits)"
        return True, f"Valid international format: {clean}"
    
    # Reject plain numbers without country code
    return False, (
        f"Phone number '{clean}' must start with '+' and country code (e.g., +919876543210 for India). "
        "Invalid format."
    )


@function_tool()
async def place_phone_call(
    context: RunContext,  # type: ignore
    phone_number: str,
    purpose: str = "follow-up",
    contact_name: str = "contact",
) -> str:
    """Place an outbound call using Telnyx REST API."""
    if not phone_number or not str(phone_number).strip():
        return "A phone number is required to place a call."

    # Validate phone number format
    is_valid, validation_msg = validate_phone_number(phone_number)
    if not is_valid:
        return f"Invalid phone number: {validation_msg}"

    config_error = validate_phone_call_config()
    if config_error:
        return config_error

    try:
        # Get Telnyx credentials
        api_key = os.getenv("TELNYX_API_KEY")
        from_number = os.getenv("TELNYX_PHONE_NUMBER")
        
        to_number = str(phone_number).strip()
        
        logging.info(
            f"[CALL_START] Initiating Telnyx call: from={from_number}, to={to_number}, "
            f"contact={contact_name}, purpose={purpose}"
        )

        # Telnyx REST API endpoint for making calls
        url = "https://api.telnyx.com/v2/calls"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        
        connection_id = os.getenv("TELNYX_CONNECTION_ID")
        
        payload = {
            "to": to_number,
            "from": from_number,
            "connection_id": connection_id,  # Must be set in TELNYX_CONNECTION_ID
            "webhook_url": None,
            "webhook_events": ["call.initiated", "call.answered", "call.hangup"],
        }
        
        # Make the API call
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        logging.info(f"[TELNYX_RESPONSE] Status: {response.status_code}, Body: {response.text}")
        
        # Check for success
        if response.status_code in [200, 201]:
            result = response.json()
            call_id = result.get("data", {}).get("id")
            
            if call_id:
                logging.info(f"[CALL_SUCCESS] Telnyx call created: call_id={call_id}, to={to_number}")
                return (
                    f"✓ Call placed to {contact_name} ({to_number}). "
                    f"Call ID: {call_id}. Connecting now..."
                )
            else:
                logging.warning(f"[CALL_PARTIAL] Telnyx returned success but no call ID")
                return f"⚠️ Call to {contact_name} initiated but unable to confirm."
        else:
            # Handle error responses
            error_data = response.json()
            error_msg = error_data.get("errors", [{}])[0].get("detail", response.text)
            logging.error(f"[TELNYX_ERROR] API returned {response.status_code}: {error_msg}")
            
            # Provide specific error messages based on status code
            if response.status_code == 401:
                return "❌ Telnyx authentication failed. Check your TELNYX_API_KEY in .env"
            elif response.status_code == 422:
                # Unprocessable entity - likely invalid phone number or connection
                if "connection" in error_msg.lower() or "call control" in error_msg.lower():
                    return (
                        "❌ Telnyx Connection ID is missing or invalid.\n"
                        "Steps to fix:\n"
                        "1. Create a Call Control App in your Telnyx dashboard\n"
                        "2. Copy the Connection ID (starts with tc_)\n"
                        "3. Add to .env: TELNYX_CONNECTION_ID=tc_your_id\n"
                        "4. See TELNYX_CONNECTION_SETUP.md for detailed steps"
                    )
                elif "number" in error_msg.lower() or "invalid" in error_msg.lower():
                    return (
                        f"❌ Invalid phone number: {to_number}. "
                        f"Use international format: +country-code followed by number"
                    )
                else:
                    return f"❌ Telnyx API error: {error_msg}"
            elif response.status_code >= 500:
                return "❌ Telnyx service error. Please try again in a moment."
            else:
                return f"❌ Failed to place call. Telnyx error: {error_msg}"

    except requests.exceptions.Timeout:
        logging.error("[CALL_TIMEOUT] Telnyx API request timed out")
        return "❌ Call request timed out. Please try again."
    
    except requests.exceptions.ConnectionError:
        logging.error("[CALL_CONNECTION] Failed to connect to Telnyx API")
        return "❌ Failed to connect to Telnyx. Check your internet connection."
    
    except Exception as exc:
        error_str = str(exc).lower()
        exc_message = str(exc)
        
        logging.error(f"[CALL_FAILED] Unexpected error: {exc_message}")
        logging.exception("Full traceback")
        
        return (
            f"❌ Failed to call {contact_name}. "
            f"Error: {exc_message}"
        )


@function_tool()
async def call_contact(
    context: RunContext,  # type: ignore
    contact_name: str,
) -> str:
    """Call a contact from the saved contact list by their name."""
    try:
        from contacts import CONTACTS, get_contact_details
    except ImportError:
        return "Contact list is not available. Please create contacts.py first."

    if not contact_name or not str(contact_name).strip():
        return "A contact name is required."

    contact = get_contact_details(contact_name.strip())
    if not contact:
        available = list(CONTACTS.keys())
        return f"Contact '{contact_name}' not found. Available contacts: {', '.join(available)}"

    phone_number = contact.get("phone")
    relation = contact.get("relation", "")
    
    result = await place_phone_call(
        context=context,
        phone_number=phone_number,
        purpose=f"Calling {relation}",
        contact_name=contact_name.strip(),
    )
    
    return result


@function_tool()
async def get_weather(
    context: RunContext,  # type: ignore
    city: str) -> str:
    """
    Get the current weather for a given city.
    """
    try:
        response = requests.get(
            f"https://wttr.in/{city}?format=3")
        if response.status_code == 200:
            logging.info(f"Weather for {city}: {response.text.strip()}")
            return response.text.strip()   
        else:
            logging.error(f"Failed to get weather for {city}: {response.status_code}")
            return f"Could not retrieve weather for {city}."
    except Exception as e:
        logging.error(f"Error retrieving weather for {city}: {e}")
        return f"An error occurred while retrieving weather for {city}." 

@function_tool()
async def search_web(
    context: RunContext,  # type: ignore
    query: str) -> str:
    """
    Search the web using DuckDuckGo.
    """
    try:
        response = requests.get(
            "https://api.duckduckgo.com/",
            params={
                "q": query,
                "format": "json",
                "no_html": 1,
                "skip_disambig": 1,
            },
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        results = data.get("AbstractText", "")
        if not results:
            topics = [
                topic.get("Text", "")
                for topic in data.get("RelatedTopics", [])
                if isinstance(topic, dict) and topic.get("Text")
            ]
            results = "\n".join(topics[:5])

        if not results:
            results = f"No search results found for '{query}'."

        logging.info(f"Search results for '{query}': {results}")
        return results
    except Exception as e:
        logging.error(f"Error searching the web for '{query}': {e}")
        return f"An error occurred while searching the web for '{query}'."    

@function_tool()    
async def send_email(
    context: RunContext,  # type: ignore
    to_email: str,
    subject: str,
    message: str,
    cc_email: Optional[str] = None
) -> str:
    """
    Send an email through Gmail.
    
    Args:
        to_email: Recipient email address
        subject: Email subject line
        message: Email body content
        cc_email: Optional CC email address
    """
    try:
        # Gmail SMTP configuration
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        
        # Get credentials from environment variables
        gmail_user = os.getenv("GMAIL_USER")
        gmail_password = os.getenv("GMAIL_APP_PASSWORD")  # Use App Password, not regular password
        
        if not gmail_user or not gmail_password:
            logging.error("Gmail credentials not found in environment variables")
            return "Email sending failed: Gmail credentials not configured."
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = gmail_user
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add CC if provided
        recipients = [to_email]
        if cc_email:
            msg['Cc'] = cc_email
            recipients.append(cc_email)
        
        # Attach message body
        msg.attach(MIMEText(message, 'plain'))
        
        # Connect to Gmail SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Enable TLS encryption
        server.login(gmail_user, gmail_password)
        
        # Send email
        text = msg.as_string()
        server.sendmail(gmail_user, recipients, text)
        server.quit()
        
        logging.info(f"Email sent successfully to {to_email}")
        return f"Email sent successfully to {to_email}"
        
    except smtplib.SMTPAuthenticationError:
        logging.error("Gmail authentication failed")
        return "Email sending failed: Authentication error. Please check your Gmail credentials."
    except smtplib.SMTPException as e:
        logging.error(f"SMTP error occurred: {e}")
        return f"Email sending failed: SMTP error - {str(e)}"
    except Exception as e:
        logging.error(f"Error sending email: {e}")
        return f"An error occurred while sending the email: {e}"