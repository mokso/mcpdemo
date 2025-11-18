from fastmcp import FastMCP
import os
from datetime import datetime

# Initialize server
port = int(os.environ.get('PORT', 8080))
mcp = FastMCP("Nordic Energy Solutions API", port=port)

# Mock customer database
CUSTOMERS = {
    "C-1001": {
        "customer_number": "C-1001",
        "name": "Matti Virtanen",
        "email": "matti.virtanen@example.fi",
        "phone": "+358 40 123 4567",
        "address": "Mannerheimintie 15, 00100 Helsinki",
        "property_type": "Detached House",
        "property_size": "150 sqm",
        "registered_date": "2024-03-12",
        "total_orders": 3,
        "customer_status": "Active"
    },
    "C-1002": {
        "customer_number": "C-1002",
        "name": "Anna Korhonen",
        "email": "anna.korhonen@example.fi",
        "phone": "+358 50 234 5678",
        "address": "Bulevardi 22, 00120 Helsinki",
        "property_type": "Apartment",
        "property_size": "85 sqm",
        "registered_date": "2024-08-20",
        "total_orders": 1,
        "customer_status": "Active"
    },
    "C-1003": {
        "customer_number": "C-1003",
        "name": "Petri Laaksonen",
        "email": "petri.laaksonen@example.fi",
        "phone": "+358 44 345 6789",
        "address": "Kalevankatu 8, 00180 Helsinki",
        "property_type": "Terraced House",
        "property_size": "120 sqm",
        "registered_date": "2025-01-15",
        "total_orders": 1,
        "customer_status": "New"
    },
    "C-1004": {
        "customer_number": "C-1004",
        "name": "Sari Nieminen",
        "email": "sari.nieminen@example.fi",
        "phone": "+358 45 456 7890",
        "address": "Hämeentie 45, 00500 Helsinki",
        "property_type": "Detached House",
        "property_size": "180 sqm",
        "registered_date": "2023-11-05",
        "total_orders": 5,
        "customer_status": "VIP"
    }
}

# Mock order database
ORDERS = {
    "NES-2025-001": {
        "order_number": "NES-2025-001",
        "customer_number": "C-1001",
        "customer_name": "Matti Virtanen",
        "service": "Energy Audit",
        "service_price": "450 EUR",
        "order_date": "2025-11-10",
        "scheduled_date": "2025-11-15",
        "completion_date": "2025-11-15",
        "status": "Completed",
        "technician": "Jukka Heikkinen",
        "notes": "Thermal imaging completed. Report sent to customer."
    },
    "NES-2025-002": {
        "order_number": "NES-2025-002",
        "customer_number": "C-1002",
        "customer_name": "Anna Korhonen",
        "service": "Solar Panel Installation",
        "service_price": "12,500 EUR",
        "order_date": "2025-11-08",
        "scheduled_date": "2025-11-20",
        "completion_date": None,
        "status": "In Progress",
        "technician": "Mikko Nieminen",
        "notes": "Installation day 1 of 3. Panels mounted on roof."
    },
    "NES-2025-003": {
        "order_number": "NES-2025-003",
        "customer_number": "C-1003",
        "customer_name": "Petri Laaksonen",
        "service": "Heat Pump Consultation",
        "service_price": "0 EUR (Free)",
        "order_date": "2025-11-16",
        "scheduled_date": "2025-11-22",
        "completion_date": None,
        "status": "Scheduled",
        "technician": "Sanna Tuominen",
        "notes": "Initial consultation scheduled. Customer interested in ground source heat pump."
    },
    "NES-2025-004": {
        "order_number": "NES-2025-004",
        "customer_number": "C-1004",
        "customer_name": "Sari Nieminen",
        "service": "Smart Home Setup",
        "service_price": "850 EUR",
        "order_date": "2025-11-12",
        "scheduled_date": "2025-11-19",
        "completion_date": None,
        "status": "Scheduled",
        "technician": "Jukka Heikkinen",
        "notes": "Installing Home Assistant hub and 12 smart devices."
    },
    "NES-2024-156": {
        "order_number": "NES-2024-156",
        "customer_number": "C-1004",
        "customer_name": "Sari Nieminen",
        "service": "Solar Panel Installation",
        "service_price": "15,200 EUR",
        "order_date": "2024-09-01",
        "scheduled_date": "2024-09-15",
        "completion_date": "2024-09-17",
        "status": "Completed",
        "technician": "Mikko Nieminen",
        "notes": "8.5 kW system installed. Customer very satisfied."
    }
}

@mcp.tool()
def get_customer_info(customer_number: str) -> dict:
    """
    Retrieve detailed customer information by customer number.
    
    Args:
        customer_number: The customer ID (e.g., C-1001)
    
    Returns:
        Complete customer profile including contact details, property info, and account status
    """
    customer = CUSTOMERS.get(customer_number.upper())
    
    if not customer:
        return {
            "success": False,
            "message": f"Customer {customer_number} not found in our system. Please verify the customer number."
        }
    
    return {
        "success": True,
        "customer": customer
    }

@mcp.tool()
def get_order_status(order_number: str) -> dict:
    """
    Retrieve current order status and details by order number.
    
    Args:
        order_number: The order ID (e.g., NES-2025-001)
    
    Returns:
        Complete order details including status, dates, assigned technician, and notes
    """
    order = ORDERS.get(order_number.upper())
    
    if not order:
        return {
            "success": False,
            "message": f"Order {order_number} not found. Please check the order number and try again."
        }
    
    # Add human-readable status message
    status_messages = {
        "Scheduled": f"Order is scheduled for {order['scheduled_date']}. Technician {order['technician']} will arrive during the scheduled time slot.",
        "In Progress": f"Work is currently underway. {order['technician']} is handling this installation.",
        "Completed": f"Service completed on {order['completion_date']}. Thank you for choosing Nordic Energy Solutions!"
    }
    
    return {
        "success": True,
        "order": order,
        "status_message": status_messages.get(order['status'], "Status information unavailable")
    }

if __name__ == "__main__":
    mcp.run(transport='sse')
