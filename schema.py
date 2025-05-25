# File: schema.py
"""
Centralized schema definitions for the Contact Management System.
This module defines the database schema and validation rules to ensure
consistency across models and views.
"""

class ContactSchema:
    """Central schema definition for contact data structure."""
    
    # Database table schema
    TABLE_NAME = "contacts"
    
    # Column definitions
    COLUMNS = {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'first_name': 'TEXT NOT NULL',
        'last_name': 'TEXT NOT NULL', 
        'phone': 'TEXT',
        'email': 'TEXT',
        'address': 'TEXT'
    }
    # Field order for display
    COLUMNS_DISPLAY_ORDER = {
        'address': 'TEXT',
        'email': 'TEXT',
        'phone': 'TEXT',
        'last_name': 'TEXT NOT NULL', 
        'first_name': 'TEXT NOT NULL',
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT'
    }

    # Field labels for GUI
    FIELD_LABELS = {
        'first_name': 'שם פרטי',
        'last_name': 'שם משפחה',
        'phone': 'טלפון',
        'email': 'כתובת אימייל',
        'address': 'כתובת'
    }
    
    # Required fields
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    # Field order for display
    DISPLAY_ORDER = ['first_name', 'last_name', 'phone', 'email', 'address']
    
    # Column widths for treeview
    COLUMN_WIDTHS = {
        'id': 50,
        'first_name': 120,
        'last_name': 120,
        'phone': 120,
        'email': 200,
        'address': 200
    }

    @classmethod
    def get_create_table_sql(cls):
        """Generate CREATE TABLE SQL statement."""
        columns = [f"{col} {definition}" for col, definition in cls.COLUMNS.items()]
        return f"CREATE TABLE IF NOT EXISTS {cls.TABLE_NAME} ({', '.join(columns)})"
    
    @classmethod
    def validate_contact_data(cls, data):
        """Validate contact data according to schema rules."""
        errors = []
        
        # Check required fields
        for field in cls.REQUIRED_FIELDS:
            if not data.get(field, '').strip():
                errors.append(f"{cls.FIELD_LABELS[field]} is required")
        
        # Basic email validation
        email = data.get('email', '').strip()
        if email and '@' not in email:
            errors.append("Email address must contain '@' symbol")
            
        return errors
