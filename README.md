# File: README.md
"""
# Contact Management System

A desktop contact management application built with Python using the Model-View-Controller (MVC) architecture pattern.

## Features

- **CRUD Operations**: Create, Read, Update, and Delete contacts
- **Persistent Storage**: SQLite database for local data storage
- **User-Friendly GUI**: Clean Tkinter interface with form validation
- **Modular Architecture**: Clean separation of concerns using MVC pattern
- **Data Validation**: Input validation with error messages
- **Responsive Design**: Resizable windows with proper layout management

## Architecture

The application follows the MVC design pattern with clean modular separation:

### Models (`models.py`)
- `ContactModel`: Handles all database operations and data persistence
- SQLite database with ACID compliance
- Centralized data validation

### Views (`views.py`)
- `MainView`: Main application window
- `ContactListView`: Table view for displaying contacts
- `ContactFormView`: Form dialog for creating/editing contacts
- Clean Tkinter GUI with modern styling

### Controllers (`controllers.py`)
- `ContactController`: Coordinates between models and views
- Handles business logic and user interactions
- Event-driven architecture

### Schema (`schema.py`)
- `ContactSchema`: Centralized schema definitions
- Database table structure
- Field validation rules
- GUI field configurations

## Database Schema

The application uses SQLite with the following table structure:

```sql
CREATE TABLE contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    phone TEXT,
    email TEXT,
    address TEXT
);
```

## Installation & Setup

### Prerequisites
- Python 3.6 or higher (with tkinter support)
- No additional packages required (uses standard library only)

### Installation Steps

1. **Download/Clone the application files**:
   - `main.py`
   - `controllers.py`
   - `views.py`
   - `models.py`
   - `schema.py`

2. **Ensure Python has tkinter support**:
   ```bash
   python -c "import tkinter; print('Tkinter is available')"
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

## Usage

### Starting the Application
```bash
python main.py
```

### Main Interface
- View all contacts in a sortable table
- Use buttons to Add, Edit, Delete, or Refresh contacts
- Double-click a contact row to edit
- Status bar shows current operation status

### Adding Contacts
1. Click "Add Contact" button
2. Fill in the required fields (First Name, Last Name)
3. Optionally add Phone, Email, and Address
4. Click "Save" to create the contact

### Editing Contacts
1. Select a contact from the list
2. Click "Edit Contact" or double-click the row
3. Modify the information in the form
4. Click "Save" to update the contact

### Deleting Contacts
1. Select a contact from the list
2. Click "Delete Contact"
3. Confirm the deletion in the dialog box

### Data Validation
- First Name and Last Name are required fields
- Email addresses must contain '@' symbol
- Form validation occurs on save with clear error messages

## File Structure

```
contact_management_system/
├── main.py              # Application entry point
├── controllers.py       # Controller layer (business logic)
├── views.py            # View layer (GUI components)
├── models.py           # Model layer (database operations)
├── schema.py           # Centralized schema definitions
├── requirements.txt    # Dependencies (none - uses stdlib)
├── README.md          # This documentation
└── contacts.db        # SQLite database (created automatically)
```

## Technical Details

### Design Patterns Used
- **Model-View-Controller (MVC)**: Clean separation of concerns
- **Observer Pattern**: Event-driven GUI interactions
- **Factory Pattern**: Centralized schema and validation

### Key Technologies
- **Python 3.6+**: Core programming language
- **Tkinter**: GUI framework (included with Python)
- **SQLite3**: Embedded database (included with Python)
- **typing**: Type hints for better code documentation

### Best Practices Implemented
- **PEP 8**: Python coding standards compliance
- **Type hints**: Enhanced code readability and IDE support
- **Docstrings**: Comprehensive documentation
- **Error handling**: Robust exception management
- **Input validation**: Data integrity and security
- **Modular design**: Easy maintenance and extensibility

## Troubleshooting

### Common Issues

1. **"No module named 'tkinter'"**:
   - Install tkinter: `sudo apt-get install python3-tk` (Ubuntu/Debian)
   - Or use: `brew install python-tk` (macOS with Homebrew)

2. **Database permission errors**:
   - Ensure write permissions in the application directory
   - The database file `contacts.db` is created automatically

3. **Window doesn't appear**:
   - Check if running in a headless environment
   - Tkinter requires a display server (X11, Wayland, etc.)

### Debug Mode
To run with additional debugging information:
```bash
python -u main.py
```

## Development

### Extending the Application

To add new fields to contacts:

1. **Update schema.py**:
   ```python
   COLUMNS = {
       # ... existing columns ...
       'new_field': 'TEXT'
   }
   
   FIELD_LABELS = {
       # ... existing labels ...
       'new_field': 'New Field Label'
   }
   
   DISPLAY_ORDER = [..., 'new_field']
   ```

2. **Database will auto-update** on next run (SQLite handles missing columns gracefully)

3. **GUI forms automatically adapt** to new schema definitions

### Adding Validation Rules
Update the `validate_contact_data` method in `schema.py`:
```python
@classmethod
def validate_contact_data(cls, data):
    errors = []
    # Add custom validation logic
    return errors
```

### Customizing the GUI
Modify styling in `views.py`:
```python
# In MainView.__init__()
style = ttk.Style()
style.configure('Custom.TButton', foreground='blue')
```

## Testing

### Manual Testing Checklist
- [ ] Create new contact with all fields
- [ ] Create contact with only required fields
- [ ] Edit existing contact
- [ ] Delete contact with confirmation
- [ ] Form validation (empty required fields)
- [ ] Email validation
- [ ] Database persistence across restarts
- [ ] GUI responsiveness and resizing

### Unit Testing Framework
For automated testing, consider adding:
```python
import unittest
from models import ContactModel

class TestContactModel(unittest.TestCase):
    def setUp(self):
        self.model = ContactModel(':memory:')  # In-memory DB for testing
    
    def test_create_contact(self):
        # Test implementation
        pass
```

## Contributing

1. Follow PEP 8 coding standards
2. Add type hints to all functions
3. Include docstrings for all classes and methods
4. Test changes manually before submitting
5. Update documentation for new features

## License

This project is provided as-is for educational and personal use.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the code comments and docstrings
3. Test with a minimal example to isolate problems

---

**Version**: 1.0  
**Python Compatibility**: 3.6+  
**GUI Framework**: Tkinter  
**Database**: SQLite3
"""