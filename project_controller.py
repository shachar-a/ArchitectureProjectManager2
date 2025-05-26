# File: project_controller.py
"""
Controller layer for the Project Management System.
Handles business logic and coordinates between project models and views.
"""

from typing import Dict, Optional
from tkinter import messagebox
from project_model import ProjectModel
from project_view import ProjectListView, ProjectFormView


class ProjectController:
    """Controller for managing project operations."""
    
    def __init__(self, parent_window):
        """
        Initialize the project controller.
        
        Args:
            parent_window: Parent tkinter window
        """
        self.parent_window = parent_window
        
        # Initialize model
        try:
            self.model = ProjectModel()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to initialize project database: {e}")
            return
        
        # Initialize view
        self.list_view = ProjectListView(
            parent=self.parent_window,
            on_add=self.show_add_form,
            on_edit=self.show_edit_form,
            on_delete=self.delete_project,
            on_refresh=self.refresh_projects
        )
        
        # Form view (created on demand)
        self.form_view: Optional[ProjectFormView] = None
        self.current_project_id: Optional[int] = None
        
        # Load initial data
        self.refresh_projects()
    
    def refresh_projects(self) -> None:
        """Refresh the project list from the database."""
        try:
            projects = self.model.get_all_projects()
            self.list_view.update_project_list(projects)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load projects: {e}")
            self.list_view.set_status("Error loading projects")
    
    def show_add_form(self) -> None:
        """Show the form for adding a new project."""
        self.current_project_id = None
        self._show_project_form("Add Project")
    
    def show_edit_form(self, project_id: int) -> None:
        """
        Show the form for editing an existing project.
        
        Args:
            project_id: ID of the project to edit
        """
        # Load project data
        project = self.model.get_project_by_id(project_id)
        if not project:
            messagebox.showerror("Error", "Project not found")
            return
        
        self.current_project_id = project_id
        self._show_project_form("Edit Project", project)
    
    def _show_project_form(self, title: str, project_data: Optional[Dict[str, str]] = None) -> None:
        """
        Show the project form dialog.
        
        Args:
            title: Form window title
            project_data: Optional project data to populate form
        """
        if self.form_view:
            # Close existing form if open
            self.form_view.close()
        
        # Create new form
        self.form_view = ProjectFormView(
            parent=self.parent_window,
            on_save=self.save_project,
            on_cancel=self.cancel_form
        )
        
        # Set window title
        self.form_view.window.title(title)
        
        # Populate form if editing
        if project_data:
            self.form_view.set_form_data(project_data)
    
    def save_project(self, project_data: Dict[str, str]) -> None:
        """
        Save project data (create or update).
        
        Args:
            project_data: Dictionary containing project information
        """
        try:
            if self.current_project_id is None:
                # Create new project
                success, message = self.model.create_project(project_data)
            else:
                # Update existing project
                success, message = self.model.update_project(
                    self.current_project_id, project_data
                )
            
            if success:
                messagebox.showinfo("Success", message)
                self.form_view.close()
                self.form_view = None
                self.refresh_projects()
            else:
                messagebox.showerror("Error", message)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save project: {e}")
    
    def cancel_form(self) -> None:
        """Cancel form operation and close form."""
        if self.form_view:
            self.form_view.close()
            self.form_view = None
    
    def delete_project(self, project_id: int) -> None:
        """
        Delete a project from the database.
        
        Args:
            project_id: ID of the project to delete
        """
        try:
            success, message = self.model.delete_project(project_id)
            
            if success:
                messagebox.showinfo("Success", message)
                self.refresh_projects()
            else:
                messagebox.showerror("Error", message)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete project: {e}")
    
    def hide_view(self) -> None:
        """Hide the project view."""
        # Hide all widgets in the parent window
        for widget in self.parent_window.winfo_children():
            widget.grid_remove()
    
    def show_view(self) -> None:
        """Show the project view."""
        # Show the list view
        self.list_view._create_list_view()
        self.refresh_projects()
