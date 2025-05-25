# File: views.py
"""
View layer for the Contact Management System.
Contains all GUI components built with Tkinter.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List, Callable, Optional
from schema import ContactSchema


class ContactFormView:
    """Form view for creating and editing contacts."""
    
    def __init__(self, parent: tk.Tk, on_save: Callable, on_cancel: Callable):
        """
        Initialize the contact form view.
        
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
        self.window.title("Contact Form")
        self.window.geometry("400x300")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()
        
        # Center the window
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.window.winfo_screenheight() // 2) - (300 // 2)
        self.window.geometry(f"400x300+{x}+{y}")
        
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
        for field in ContactSchema.DISPLAY_ORDER:
            label = ContactSchema.FIELD_LABELS[field]
            
            # Add asterisk for required fields
            if field in ContactSchema.REQUIRED_FIELDS:
                label += " *"
            
            # Label
            ttk.Label(main_frame, text=label).grid(
                row=row, column=1, sticky=tk.W, pady=5
            )
            
            # Entry widget
            if field == 'address':
                # Multi-line text for address
                entry = tk.Text(main_frame, height=3, width=30)
                entry.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=5)
            else:
                # Single-line entry
                entry = ttk.Entry(main_frame, width=30)
                entry.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=5)
            
            self.entries[field] = entry
            row += 1
        
        # Required fields note
        ttk.Label(main_frame, text="* Required fields", 
                 font=("TkDefaultFont", 8)).grid(
            row=row, column=0, columnspan=2, sticky=tk.W, pady=(10, 5)
        )
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=row+1, column=0, columnspan=2, pady=20)
        
        # Save button
        ttk.Button(button_frame, text="Save", 
                  command=self._handle_save).pack(side=tk.LEFT, padx=5)
        
        # Cancel button
        ttk.Button(button_frame, text="Cancel", 
                  command=self._handle_cancel).pack(side=tk.LEFT, padx=5)
        
        # Set focus to first field
        self.entries['first_name'].focus()
    
    def _handle_save(self) -> None:
        """Handle save button click."""
        contact_data = self.get_form_data()
        self.on_save(contact_data)
    
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
            if field == 'address':
                # Get text from Text widget
                data[field] = entry.get("1.0", tk.END).strip()
            else:
                # Get text from Entry widget
                data[field] = entry.get().strip()
        
        return data
    
    def set_form_data(self, contact_data: Dict[str, str]) -> None:
        """
        Populate form fields with contact data.
        
        Args:
            contact_data: Dictionary containing contact information
        """
        for field, entry in self.entries.items():
            value = contact_data.get(field, '')
            
            if field == 'address':
                # Set text in Text widget
                entry.delete("1.0", tk.END)
                entry.insert("1.0", value)
            else:
                # Set text in Entry widget
                entry.delete(0, tk.END)
                entry.insert(0, value)
    
    def close(self) -> None:
        """Close the form window."""
        self.window.destroy()


class ContactListView:
    """List view for displaying contacts in a table format."""
    
    def __init__(self, parent: tk.Tk, on_add: Callable, on_edit: Callable, 
                 on_delete: Callable, on_refresh: Callable):
        """
        Initialize the contact list view.
        
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
        title_label = ttk.Label(main_frame, text="אנשי קשר", 
                               font=("TkDefaultFont", 16, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Treeview frame with scrollbars
        tree_frame = ttk.Frame(main_frame)
        tree_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        # Create treeview
        columns = list(ContactSchema.COLUMNS.keys())
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
        
        # Configure columns
        for col in columns:
            self.tree.heading(col, text=ContactSchema.FIELD_LABELS.get(col, col.title()))
            self.tree.column(col, width=ContactSchema.COLUMN_WIDTHS.get(col, 100))
        
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
        ttk.Button(button_frame, text="Add Contact", 
                  command=self.on_add).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Edit Contact", 
                  command=self._handle_edit).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Contact", 
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
            messagebox.showwarning("No Selection", "Please select a contact to edit.")
            return
        
        # Get contact ID from selected item
        item = selected_item[0]
        contact_id = self.tree.item(item)['values'][0]  # ID is first column
        self.on_edit(int(contact_id))
    
    def _handle_delete(self) -> None:
        """Handle delete button click."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a contact to delete.")
            return
        
        # Get contact info for confirmation
        item = selected_item[0]
        values = self.tree.item(item)['values']
        contact_id = values[0]
        name = f"{values[1]} {values[2]}"  # first_name + last_name
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", 
                              f"Are you sure you want to delete '{name}'?"):
            self.on_delete(int(contact_id))
    
    def update_contact_list(self, contacts: List[Dict[str, str]]) -> None:
        """
        Update the treeview with new contact data.
        
        Args:
            contacts: List of contact dictionaries
        """
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add new items
        for contact in contacts:
            values = [contact.get(col, '') for col in ContactSchema.COLUMNS.keys()]
            self.tree.insert('', tk.END, values=values)
        
        # Update status
        count = len(contacts)
        self.status_var.set(f"{count} contact{'s' if count != 1 else ''} loaded")
    
    def set_status(self, message: str) -> None:
        """
        Set status bar message.
        
        Args:
            message: Status message to display
        """
        self.status_var.set(message)


class MainView:
    """Main application view that manages the overall window."""
    
    def __init__(self, title: str = "Contact Management System"):
        """
        Initialize the main application window.
        
        Args:
            title: Window title
        """
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.root.winfo_screenheight() // 2) - (600 // 2)
        self.root.geometry(f"800x600+{x}+{y}")
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')  # Use a modern theme
    
    def run(self) -> None:
        """Start the main event loop."""
        self.root.mainloop()
    
    def get_root(self) -> tk.Tk:
        """Get the root window."""
        return self.root
