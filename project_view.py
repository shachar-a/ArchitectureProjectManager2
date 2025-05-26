# File: project_view.py
"""
View layer for the Project Management System.
Contains all GUI components built with Tkinter for project management.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List, Callable, Optional
from project_schema import ProjectSchema


class ProjectFormView:
    """Form view for creating and editing projects."""
    
    def __init__(self, parent: tk.Tk, on_save: Callable, on_cancel: Callable):
        """
        Initialize the project form view.
        
        Args:
            parent: Parent tkinter window
            on_save: Callback function for save action
            on_cancel: Callback function for cancel action
        """
        self.parent = parent
        self.on_save = on_save
        self.on_cancel = on_cancel
        
        # Create form window
        self.window = tk.Toplevel(parent)
        self.window.title("Project Form")
        self.window.geometry("450x400")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()
        
        # Center the window
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.window.winfo_screenheight() // 2) - (400 // 2)
        self.window.geometry(f"450x400+{x}+{y}")
        
        # Store entry widgets
        self.entries = {}
        
        self._create_form()
    
    def _create_form(self) -> None:
        """Create the form layout with input fields."""
        # Main frame
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Create form fields
        row = 0
        for field in ProjectSchema.DISPLAY_ORDER:
            label = ProjectSchema.FIELD_LABELS[field]
            
            # Add asterisk for required fields
            if field in ProjectSchema.REQUIRED_FIELDS:
                label += " *"
            
            # Label
            ttk.Label(main_frame, text=label).grid(
                row=row, column=2, sticky=tk.W, pady=5
            )
            
            # Entry widget based on field type
            if field == 'is_active':
                # Checkbox for boolean field
                var = tk.StringVar(value='לא')
                entry = ttk.Combobox(main_frame, textvariable=var, 
                                   values=['כן', 'לא'], state='readonly', width=27)
                entry.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
            elif field == 'state':
                # Combobox for state selection
                var = tk.StringVar()
                entry = ttk.Combobox(main_frame, textvariable=var, 
                                   values=ProjectSchema.STATE_OPTIONS, width=27)
                entry.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
            elif field in ['start_date', 'end_date']:
                # Entry with date format hint
                entry = ttk.Entry(main_frame, width=30)
                entry.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
                # Add date format hint
                hint_label = ttk.Label(main_frame, text="(YYYY-MM-DD)", 
                                     font=("TkDefaultFont", 8), foreground="gray")
                hint_label.grid(row=row, column=0, sticky=tk.W, padx=(5, 0))
            else:
                # Regular entry
                entry = ttk.Entry(main_frame, width=30)
                entry.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
            
            self.entries[field] = entry
            row += 1
        
        # Required fields note
        ttk.Label(main_frame, text="שדה חובה *", 
                 font=("TkDefaultFont", 8)).grid(
            row=row, column=2, columnspan=3, sticky=tk.W, pady=(10, 5)
        )
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=row+1, column=0, columnspan=3, pady=20)
        
        # Save button
        ttk.Button(button_frame, text="Save", 
                  command=self._handle_save).pack(side=tk.LEFT, padx=5)
        
        # Cancel button
        ttk.Button(button_frame, text="Cancel", 
                  command=self._handle_cancel).pack(side=tk.LEFT, padx=5)
        
        # Set focus to first field
        self.entries['customer_name'].focus()
    
    def _handle_save(self) -> None:
        """Handle save button click."""
        project_data = self.get_form_data()
        self.on_save(project_data)
    
    def _handle_cancel(self) -> None:
        """Handle cancel button click."""
        self.on_cancel()
    
    def get_form_data(self) -> Dict[str, str]:
        """
        Extract data from form fields.
        
        Returns:
            Dictionary containing form data
        """
        data = {}
        for field, entry in self.entries.items():
            if hasattr(entry, 'get'):
                data[field] = entry.get().strip()
            else:
                # For combobox with textvariable
                data[field] = entry.get().strip()
        
        return data
    
    def set_form_data(self, project_data: Dict[str, str]) -> None:
        """
        Populate form fields with project data.
        
        Args:
            project_data: Dictionary containing project information
        """
        for field, entry in self.entries.items():
            value = project_data.get(field, '')
            
            if hasattr(entry, 'set'):
                # For combobox
                entry.set(value)
            else:
                # For regular entry
                entry.delete(0, tk.END)
                entry.insert(0, value)
    
    def close(self) -> None:
        """Close the form window."""
        self.window.destroy()


class ProjectListView:
    """List view for displaying projects in a table format."""
    
    def __init__(self, parent: tk.Tk, on_add: Callable, on_edit: Callable, 
                 on_delete: Callable, on_refresh: Callable):
        """
        Initialize the project list view.
        
        Args:
            parent: Parent tkinter window
            on_add: Callback function for add action
            on_edit: Callback function for edit action
            on_delete: Callback function for delete action
            on_refresh: Callback function for refresh action
        """
        self.parent = parent
        self.on_add = on_add
        self.on_edit = on_edit
        self.on_delete = on_delete
        self.on_refresh = on_refresh
        
        self._create_list_view()
    
    def _create_list_view(self) -> None:
        """Create the list view layout."""
        # Main frame
        main_frame = ttk.Frame(self.parent, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="ניהול פרויקטים", 
                               font=("TkDefaultFont", 16, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Treeview frame with scrollbars
        tree_frame = ttk.Frame(main_frame)
        tree_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        # Create treeview
        columns = list(ProjectSchema.COLUMNS.keys())
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
        
        # Configure columns
        for col in columns:
            self.tree.heading(col, text=ProjectSchema.FIELD_LABELS.get(col, col.title()))
            self.tree.column(col, width=ProjectSchema.COLUMN_WIDTHS.get(col, 100))
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, 
                                   command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, 
                                   command=self.tree.xview)

        # Update column appearance to present data right to left. Also don't show the ID column in the display.    
        display_columns = [col for col in columns if col != 'id']  # Exclude ID from display
        display_columns.reverse()  # Reverse order for display
        self.tree['displaycolumns'] = display_columns  # Set display columns

        self.tree.configure(yscrollcommand=v_scrollbar.set, 
                           xscrollcommand=h_scrollbar.set)

        # Grid layout for treeview and scrollbars
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, pady=10)
        
        # Buttons
        ttk.Button(button_frame, text="Add Project", 
                  command=self.on_add).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Edit Project", 
                  command=self._handle_edit).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Project", 
                  command=self._handle_delete).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Refresh", 
                  command=self.on_refresh).pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Bind double-click to edit
        self.tree.bind("<Double-1>", lambda e: self._handle_edit())
    
    def _handle_edit(self) -> None:
        """Handle edit button click."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a project to edit.")
            return
        
        # Get project ID from selected item
        item = selected_item[0]
        project_id = self.tree.item(item)['values'][0]  # ID is first column
        self.on_edit(int(project_id))
    
    def _handle_delete(self) -> None:
        """Handle delete button click."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a project to delete.")
            return
        
        # Get project info for confirmation
        item = selected_item[0]
        values = self.tree.item(item)['values']
        project_id = values[0]
        customer_name = values[1]  # customer_name
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", 
                              f"Are you sure you want to delete project for '{customer_name}'?"):
            self.on_delete(int(project_id))
    
    def update_project_list(self, projects: List[Dict[str, str]]) -> None:
        """
        Update the treeview with new project data.
        
        Args:
            projects: List of project dictionaries
        """
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add new items
        for project in projects:
            values = [project.get(col, '') for col in ProjectSchema.COLUMNS.keys()]
            self.tree.insert('', tk.END, values=values)
        
        # Update status
        count = len(projects)
        self.status_var.set(f"{count} project{'s' if count != 1 else ''} loaded")
    
    def set_status(self, message: str) -> None:
        """
        Set status bar message.
        
        Args:
            message: Status message to display
        """
        self.status_var.set(message)
