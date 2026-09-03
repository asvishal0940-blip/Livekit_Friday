# Contact list for Friday Agent
# Phone numbers in international format with country code +91 for India

CONTACTS = {
    # Family
    "Mom": {
        "phone": "+917092406749",
        "name": "Shanthi.S",
        "relation": "Mother",
        "priority": "high",
    },
    "Dad": {
        "phone": "+919942320940",
        "name": "SAN.Selvaraaja",
        "relation": "Father",
        "priority": "high",
    },
    "Dharsan": {
        "phone": "+917305184666",
        "name": "Dharsan.S.S",
        "relation": "Brother",
        "priority": "high",
    },
    
    # Friends & Colleagues
    "Arun": {
        "phone": "+919876543213",
        "name": "Arun",
        "relation": "Friend",
        "priority": "medium",
    },
    "Priya": {
        "phone": "+919876543214",
        "name": "Priya",
        "relation": "Colleague",
        "priority": "medium",
    },
    
    # Important Contacts
    "School": {
        "phone": "+919876543215",
        "name": "Equitas Gurukul School",
        "relation": "School",
        "priority": "high",
    },
}

# Quick lookup by phone number
PHONE_TO_CONTACT = {v["phone"]: k for k, v in CONTACTS.items()}


def get_contact_name(phone_number: str) -> str:
    """Get contact name by phone number."""
    return PHONE_TO_CONTACT.get(phone_number, "Unknown")


def get_contact_details(name: str) -> dict:
    """Get full contact details by name."""
    return CONTACTS.get(name, {})


def list_contacts(priority: str = None) -> list:
    """List all contacts, optionally filtered by priority."""
    if priority:
        return [name for name, data in CONTACTS.items() if data.get("priority") == priority]
    return list(CONTACTS.keys())


def add_contact(name: str, phone: str, relation: str = "Contact", priority: str = "medium"):
    """Add a new contact."""
    CONTACTS[name] = {
        "phone": phone,
        "name": name,
        "relation": relation,
        "priority": priority,
    }
    PHONE_TO_CONTACT[phone] = name
