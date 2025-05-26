# File: project_schema.py
"""
Centralized schema definitions for the Project Management System.
This module defines the database schema and validation rules for projects
to ensure consistency across models and views.
"""

class ProjectSchema:
    """Central schema definition for project data structure."""
    
    # Database table schema
    TABLE_NAME = "projects"
    
    # Column definitions
    COLUMNS = {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'customer_name': 'TEXT NOT NULL',
        'location': 'TEXT',
        'start_date': 'TEXT',
        'end_date': 'TEXT',
        'is_active': 'BOOLEAN',
        'state': 'TEXT'
    }

    # Field labels for GUI (Hebrew)
    FIELD_LABELS = {
        'customer_name': 'שם לקוח',
        'location': 'מיקום',
        'start_date': 'תאריך התחלה',
        'end_date': 'תאריך סיום',
        'is_active': 'פעיל',
        'state': 'מצב'
    }
    
    # Required fields
    REQUIRED_FIELDS = ['customer_name']
    
    # Field order for display
    DISPLAY_ORDER = ['customer_name', 'location', 'start_date', 'end_date', 'is_active', 'state']
    
    # Column widths for treeview
    COLUMN_WIDTHS = {
        'id': 50,
        'customer_name': 150,
        'location': 120,
        'start_date': 100,
        'end_date': 100,
        'is_active': 80,
        'state': 100
    }

    # State options
    STATE_OPTIONS = ['תכנון', 'בביצוע', 'הושלם', 'מושהה', 'בוטל']

    @classmethod
    def get_create_table_sql(cls):
        """Generate CREATE TABLE SQL statement."""
        columns = [f"{col} {definition}" for col, definition in cls.COLUMNS.items()]
        return f"CREATE TABLE IF NOT EXISTS {cls.TABLE_NAME} ({', '.join(columns)})"
    
    @classmethod
    def validate_project_data(cls, data):
        """Validate project data according to schema rules."""
        errors = []
        
        # Check required fields
        for field in cls.REQUIRED_FIELDS:
            if not data.get(field, '').strip():
                errors.append(f"{cls.FIELD_LABELS[field]} is required")
        
        # Validate date format (basic validation)
        for date_field in ['start_date', 'end_date']:
            date_value = data.get(date_field, '').strip()
            if date_value:
                # Basic date format validation (YYYY-MM-DD)
                try:
                    if len(date_value) == 10 and date_value.count('-') == 2:
                        year, month, day = date_value.split('-')
                        if not (year.isdigit() and month.isdigit() and day.isdigit()):
                            errors.append(f"{cls.FIELD_LABELS[date_field]} must be in YYYY-MM-DD format")
                    elif date_value:
                        errors.append(f"{cls.FIELD_LABELS[date_field]} must be in YYYY-MM-DD format")
                except:
                    errors.append(f"{cls.FIELD_LABELS[date_field]} must be in YYYY-MM-DD format")
            
        return errors
