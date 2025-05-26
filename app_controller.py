# File: app_controller.py
"""
Main application controller that manages navigation between Contact and Project views.
This controller implements the unified interface with navigation capabilities.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from views import MainView
from controllers import ContactController
from project_controller import ProjectController


class AppController:
    """Main application controller managing navigation between modules."""
    
    def __init__(self):
        """Initialize the main application controller."""
        # Initialize main view
        self.main_view = MainView("Architecture Project Manager")
        self.root = self.main_view.get_root()
        
        # Create main container frame
        self.main_container = ttk.Frame(self.root)
        self.main_container.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for main window
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.main_container.columnconfigure(0, weight=1)
        self.main_container.rowconfigure(0, weight=1)
        
        # Create navigation frame
        self._create_navigation()
        
        # Initialize controllers
        self.contact_controller = None
        self.project_controller = None
        self.current_view = None
        
        # Start with contacts view
        self.show_contacts()
    
    def _create_navigation(self) -> None:
        """Create the navigation bar with tabs/buttons."""
        # Navigation frame at the top
        nav_frame = ttk.Frame(self.root, padding="10")
        nav_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Configure navigation frame
        self.root.rowconfigure(0, weight=0)  # Navigation doesn't expand
        nav_frame.columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(nav_frame, text="Architecture Project Manager", 
                               font=("TkDefaultFont", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Navigation buttons
        button_frame = ttk.Frame(nav_frame)
        button_frame.grid(row=1, column=0, columnspan=2)
        
        # Contacts button
        self.contacts_btn = ttk.Button(button_frame, text="אנשי קשר (Contacts)", 
                                      command=self.show_contacts, width=20)
        self.contacts_btn.pack(side=tk.LEFT, padx=5)
        
        # Projects button
        self.projects_btn = ttk.Button(button_frame, text="פרויקטים (Projects)", 
                                      command=self.show_projects, width=20)
        self.projects_btn.pack(side=tk.LEFT, padx=5)
        
        # Separator
        separator = ttk.Separator(nav_frame, orient='horizontal')
        separator.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
    
    def _clear_main_container(self) -> None:
        """Clear all widgets from the main container."""
        for widget in self.main_container.winfo_children():
            widget.destroy()
    
    def _update_button_states(self, active_view: str) -> None:
        """
        Update button states to show which view is active.
        
        Args:
            active_view: Either 'contacts' or 'projects'
        """
        if active_view == 'contacts':
            self.contacts_btn.configure(state='disabled')
            self.projects_btn.configure(state='normal')
        else:
            self.contacts_btn.configure(state='normal')
            self.projects_btn.configure(state='disabled')
    
    def show_contacts(self) -> None:
        """Show the contacts management view."""
        try:
            # Clear current view
            self._clear_main_container()
            
            # Close any open project forms
            if self.project_controller and self.project_controller.form_view:
                self.project_controller.form_view.close()
                self.project_controller.form_view = None
            
            # Initialize contact controller if needed
            if not self.contact_controller:
                # Create a temporary frame for the contact view
                contact_frame = ttk.Frame(self.main_container)
                contact_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
                contact_frame.columnconfigure(0, weight=1)
                contact_frame.rowconfigure(0, weight=1)
                
                # Initialize contact controller with the frame as parent
                self.contact_controller = ContactController()
                
                # Replace the contact controller's main view with our frame
                self.contact_controller.main_view.root.withdraw()  # Hide original window
                
                # Recreate the contact list view in our frame
                from views import ContactListView
                self.contact_controller.list_view = ContactListView(
                    parent=contact_frame,
                    on_add=self.contact_controller.show_add_form,
                    on_edit=self.contact_controller.show_edit_form,
                    on_delete=self.contact_controller.delete_contact,
                    on_refresh=self.contact_controller.refresh_contacts
                )
                
                # Load initial data
                self.contact_controller.refresh_contacts()
            else:
                # Recreate the contact view in the main container
                contact_frame = ttk.Frame(self.main_container)
                contact_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
                contact_frame.columnconfigure(0, weight=1)
                contact_frame.rowconfigure(0, weight=1)
                
                from views import ContactListView
                self.contact_controller.list_view = ContactListView(
                    parent=contact_frame,
                    on_add=self.contact_controller.show_add_form,
                    on_edit=self.contact_controller.show_edit_form,
                    on_delete=self.contact_controller.delete_contact,
                    on_refresh=self.contact_controller.refresh_contacts
                )
                
                self.contact_controller.refresh_contacts()
            
            self.current_view = 'contacts'
            self._update_button_states('contacts')
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load contacts view: {e}")
    
    def show_projects(self) -> None:
        """Show the projects management view."""
        try:
            # Clear current view
            self._clear_main_container()
            
            # Close any open contact forms
            if self.contact_controller and self.contact_controller.form_view:
                self.contact_controller.form_view.close()
                self.contact_controller.form_view = None
            
            # Create project frame
            project_frame = ttk.Frame(self.main_container)
            project_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            project_frame.columnconfigure(0, weight=1)
            project_frame.rowconfigure(0, weight=1)
            
            # Initialize project controller
            self.project_controller = ProjectController(project_frame)
            
            self.current_view = 'projects'
            self._update_button_states('projects')
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load projects view: {e}")
    
    def run(self) -> None:
        """Start the main application."""
        self.main_view.run()


def main():
    """Main function to start the unified application."""
    try:
        # Create and run the application
        app = AppController()
        app.run()
        
    except KeyboardInterrupt:
        print("\nApplication terminated by user")
        sys.exit(0)
        
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
