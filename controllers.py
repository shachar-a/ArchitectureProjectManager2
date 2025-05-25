# File: controllers.py
"""
Controller layer for the Contact Management System.
Handles business logic and coordinates between models and views.
"""

from typing import Dict, Optional
from tkinter import messagebox
from models import ContactModel
from views import MainView, ContactListView, ContactFormView


class ContactController:
    """Main controller for managing contact operations."""
    
    def __init__(self):
        """Initialize the contact controller."""
        # Initialize model
        try:
            self.model = ContactModel()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to initialize database: {e}")
            return
        
        # Initialize views
        self.main_view = MainView()
        self.list_view = ContactListView(
            parent=self.main_view.get_root(),
            on_add=self.show_add_form,
            on_edit=self.show_edit_form,
            on_delete=self.delete_contact,
            on_refresh=self.refresh_contacts
        )
        
        # Form view (created on demand)
        self.form_view: Optional[ContactFormView] = None
        self.current_contact_id: Optional[int] = None
        
        # Load initial data
        self.refresh_contacts()
    
    def run(self) -> None:
        """Start the application."""
        self.main_view.run()
    
    def refresh_contacts(self) -> None:
        """Refresh the contact list from the database."""
        try:
            contacts = self.model.get_all_contacts()
            self.list_view.update_contact_list(contacts)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load contacts: {e}")
            self.list_view.set_status("Error loading contacts")
    
    def show_add_form(self) -> None:
        """Show the form for adding a new contact."""
        self.current_contact_id = None
        self._show_contact_form("Add Contact")
    
    def show_edit_form(self, contact_id: int) -> None:
        """
        Show the form for editing an existing contact.
        
        Args:
            contact_id: ID of the contact to edit
        """
        # Load contact data
        contact = self.model.get_contact_by_id(contact_id)
        if not contact:
            messagebox.showerror("Error", "Contact not found")
            return
        
        self.current_contact_id = contact_id
        self._show_contact_form("Edit Contact", contact)
    
    def _show_contact_form(self, title: str, contact_data: Optional[Dict[str, str]] = None) -> None:
        """
        Show the contact form dialog.
        
        Args:
            title: Form window title
            contact_data: Optional contact data to populate form
        """
        if self.form_view:
            # Close existing form if open
            self.form_view.close()
        
        # Create new form
        self.form_view = ContactFormView(
            parent=self.main_view.get_root(),
            on_save=self.save_contact,
            on_cancel=self.cancel_form
        )
        
        # Set window title
        self.form_view.window.title(title)
        
        # Populate form if editing
        if contact_data:
            self.form_view.set_form_data(contact_data)
    
    def save_contact(self, contact_data: Dict[str, str]) -> None:
        """
        Save contact data (create or update).
        
        Args:
            contact_data: Dictionary containing contact information
        """
        try:
            if self.current_contact_id is None:
                # Create new contact
                success, message = self.model.create_contact(contact_data)
            else:
                # Update existing contact
                success, message = self.model.update_contact(
                    self.current_contact_id, contact_data
                )
            
            if success:
                messagebox.showinfo("Success", message)
                self.form_view.close()
                self.form_view = None
                self.refresh_contacts()
            else:
                messagebox.showerror("Error", message)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save contact: {e}")
    
    def cancel_form(self) -> None:
        """Cancel form operation and close form."""
        if self.form_view:
            self.form_view.close()
            self.form_view = None
    
    def delete_contact(self, contact_id: int) -> None:
        """
        Delete a contact from the database.
        
        Args:
            contact_id: ID of the contact to delete
        """
        try:
            success, message = self.model.delete_contact(contact_id)
            
            if success:
                messagebox.showinfo("Success", message)
                self.refresh_contacts()
            else:
                messagebox.showerror("Error", message)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete contact: {e}")
