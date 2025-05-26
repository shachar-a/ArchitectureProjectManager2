# Architecture Project Manager

A desktop application built with Python, Tkinter, and SQLite for managing both contacts and projects using the Model-View-Controller (MVC) architecture pattern.

## Features

### Contact Management
- **CRUD Operations**: Create, Read, Update, and Delete contacts
- **Contact Information**: Store name, phone, email, and address
- **Data Validation**: Input validation with error messages
- **Hebrew Language Support**: GUI labels in Hebrew

### Project Management
- **Project CRUD**: Create, Read, Update, and Delete projects
- **Project Details**: Customer name, location, start/end dates, status, and state
- **Project States**: Planning, In Progress, Completed, On Hold, Cancelled
- **Active Status Tracking**: Boolean flag for project activity

### Unified Interface
- **Navigation**: Switch between Contact and Project management views
- **Consistent UI**: Matching visual style across both modules
- **Modular Design**: Completely separate logic for contacts and projects
- **Persistent Storage**: SQLite database for local data storage

## Architecture

The application follows the MVC design pattern with clean modular separation:

### Contact Module
- **Model** (`models.py`): Contact database operations and data persistence
- **View** (`views.py`): Contact GUI components and layouts
- **Controller** (`controllers.py`): Contact business logic and event handling
- **Schema** (`schema.py`): Contact database schema and validation rules

### Project Module
- **Model** (`project_model.py`): Project database operations and data persistence
- **View** (`project_view.py`): Project GUI components and layouts
- **Controller** (`project_controller.py`): Project business logic and event handling
- **Schema** (`project_schema.py`): Project database schema and validation rules

### Main Application
- **App Controller** (`app_controller.py`): Main navigation and view management
- **Main Entry** (`main.py`): Application entry point

## Database Schema

The application uses SQLite with the following table structures:

### Contacts Table
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

### Projects Table
```sql
CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    location TEXT,
    start_date TEXT,
    end_date TEXT,
    is_active BOOLEAN,
    state TEXT
);
```

## Installation & Setup

### Prerequisites
- Python 3.6 or higher (with tkinter support)
- No additional packages required (uses standard library only)

### Installation Steps

1. **Download/Clone the application files**:
   - `main.py`
   - `app_controller.py`
   - Contact module: `controllers.py`, `views.py`, `models.py`, `schema.py`
   - Project module: `project_controller.py`, `project_view.py`, `project_model.py`, `project_schema.py`

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
- **Navigation Bar**: Switch between "אנשי קשר (Contacts)" and "פרויקטים (Projects)"
- **Active View Indication**: Current view button is disabled
- **Unified Window**: Single window with navigation between modules

### Contact Management
1. **Adding Contacts**: Click "Add Contact" button and fill in the form
2. **Editing Contacts**: Double-click on a contact or select and click "Edit Contact"
3. **Deleting Contacts**: Select a contact and click "Delete Contact"
4. **Required Fields**: First Name and Last Name are mandatory

### Project Management
1. **Adding Projects**: Click "Add Project" button and fill in the form
2. **Editing Projects**: Double-click on a project or select and click "Edit Project"
3. **Deleting Projects**: Select a project and click "Delete Project"
4. **Required Fields**: Customer Name is mandatory
5. **Date Format**: Use YYYY-MM-DD format for start and end dates
6. **Project States**: Select from predefined states (תכנון, בביצוע, הושלם, מושהה, בוטל)
7. **Active Status**: Choose כן (Yes) or לא (No) for project activity

### Data Validation
- Required fields are marked with asterisks (*)
- Email addresses must contain '@' symbol
- Date fields must follow YYYY-MM-DD format
- Form validation occurs on save with clear error messages

## File Structure

```
architecture_project_manager/
├── main.py                  # Application entry point
├── app_controller.py        # Main navigation controller
│
├── Contact Module:
│   ├── controllers.py       # Contact controller (business logic)
│   ├── views.py            # Contact views (GUI components)
│   ├── models.py           # Contact model (database operations)
│   └── schema.py           # Contact schema definitions
│
├── Project Module:
│   ├── project_controller.py # Project controller (business logic)
│   ├── project_view.py      # Project views (GUI components)
│   ├── project_model.py     # Project model (database operations)
│   └── project_schema.py    # Project schema definitions
│
├── requirements.txt         # Dependencies (none - uses stdlib)
├── README.md               # This documentation
└── contacts.db            # SQLite database (created automatically)
```

## Technical Details

### Design Patterns Used
- **Model-View-Controller (MVC)**: Clean separation of concerns for both modules
- **Observer Pattern**: Event-driven GUI interactions
- **Factory Pattern**: Centralized schema and validation
- **Modular Architecture**: Complete separation between contact and project logic

### Key Technologies
- **Python 3.6+**: Core programming language
- **Tkinter**: GUI framework (included with Python)
- **SQLite3**: Embedded database (included with Python)
- **typing**: Type hints for better code documentation

### Navigation Implementation
- **Single Window**: One main window with dynamic content switching
- **View Management**: Controllers are created/destroyed as needed
- **Form Isolation**: Forms from one module are closed when switching views
- **State Preservation**: Each module maintains its own state independently

### Best Practices Implemented
- **PEP 8**: Python coding standards compliance
- **Type hints**: Enhanced code readability and IDE support
- **Docstrings**: Comprehensive documentation
- **Error handling**: Robust exception management
- **Input validation**: Data integrity and security
- **Modular design**: Easy maintenance and extensibility
- **Separation of concerns**: No mixing of contact and project logic

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

4. **Navigation issues**:
   - If views don't switch properly, restart the application
   - Check console for any error messages

### Debug Mode
To run with additional debugging information:
```bash
python -u main.py
```

## Development

### Adding New Modules
To add a new management module (e.g., Tasks):

1. **Create module files**:
   - `task_schema.py`: Define database schema and validation
   - `task_model.py`: Implement database operations
   - `task_view.py`: Create GUI components
   - `task_controller.py`: Handle business logic

2. **Update app_controller.py**:
   - Add navigation button
   - Implement show_tasks() method
   - Import task controller

3. **Follow existing patterns**: Use contact/project modules as templates

### Extending Existing Modules

To add new fields to contacts or projects:

1. **Update respective schema file**:
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

2. **Database will auto-update** on next run
3. **GUI forms automatically adapt** to new schema definitions

### Customizing the GUI
Modify styling in view files:
```python
# In view initialization
style = ttk.Style()
style.configure('Custom.TButton', foreground='blue')
```

## Testing

### Manual Testing Checklist

#### Contact Module
- [ ] Create new contact with all fields
- [ ] Create contact with only required fields
- [ ] Edit existing contact
- [ ] Delete contact with confirmation
- [ ] Form validation (empty required fields)
- [ ] Email validation

#### Project Module
- [ ] Create new project with all fields
- [ ] Create project with only required fields
- [ ] Edit existing project
- [ ] Delete project with confirmation
- [ ] Date format validation
- [ ] State selection functionality
- [ ] Active status toggle

#### Navigation
- [ ] Switch from contacts to projects
- [ ] Switch from projects to contacts
- [ ] Form closure when switching views
- [ ] Button state updates
- [ ] Data persistence across view switches

#### General
- [ ] Database persistence across restarts
- [ ] GUI responsiveness and resizing
- [ ] Error handling and user feedback

## Contributing

1. Follow PEP 8 coding standards
2. Add type hints to all functions
3. Include docstrings for all classes and methods
4. Maintain separation between contact and project logic
5. Test changes manually before submitting
6. Update documentation for new features

## License

This project is provided as-is for educational and personal use.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the code comments and docstrings
3. Test with a minimal example to isolate problems

---

**Version**: 3.1  
**Python Compatibility**: 3.6+  
**GUI Framework**: Tkinter  
**Database**: SQLite3  
**Architecture**: MVC with Navigation
