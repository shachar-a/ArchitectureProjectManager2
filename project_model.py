# File: project_model.py
"""
Model layer for the Project Management System.
Handles all database operations and data persistence for projects.
"""

import sqlite3
import os
from typing import List, Dict, Optional, Tuple
from project_schema import ProjectSchema


class ProjectModel:
    """Model class for managing project data in SQLite database."""
    
    def __init__(self, db_path: str = "contacts.db"):
        """
        Initialize the project model with database connection.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self) -> None:
        """Initialize database and create projects table if it doesn't exist."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(ProjectSchema.get_create_table_sql())
                conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"Database initialization failed: {e}")
    
    def create_project(self, project_data: Dict[str, str]) -> Tuple[bool, str]:
        """
        Create a new project in the database.
        
        Args:
            project_data: Dictionary containing project information
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        # Validate data
        validation_errors = ProjectSchema.validate_project_data(project_data)
        if validation_errors:
            return False, "; ".join(validation_errors)
        
        try:
            # Prepare data for insertion (exclude id)
            fields = [field for field in ProjectSchema.DISPLAY_ORDER]
            values = []
            
            for field in fields:
                value = project_data.get(field, '').strip()
                # Convert boolean field
                if field == 'is_active':
                    value = 1 if value.lower() in ['true', '1', 'yes', 'כן'] else 0
                values.append(value)
            
            placeholders = ", ".join(["?"] * len(fields))
            field_names = ", ".join(fields)
            
            sql = f"INSERT INTO {ProjectSchema.TABLE_NAME} ({field_names}) VALUES ({placeholders})"
            
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(sql, values)
                conn.commit()
                
            return True, "Project created successfully"
            
        except sqlite3.Error as e:
            return False, f"Database error: {e}"
    
    def get_all_projects(self) -> List[Dict[str, str]]:
        """
        Retrieve all projects from the database.
        
        Returns:
            List of project dictionaries
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row  # Enable column access by name
                cursor = conn.execute(f"SELECT * FROM {ProjectSchema.TABLE_NAME} ORDER BY customer_name")
                
                projects = []
                for row in cursor:
                    project = {}
                    for column in ProjectSchema.COLUMNS.keys():
                        value = row[column]
                        # Convert boolean field for display
                        if column == 'is_active':
                            value = 'כן' if value else 'לא'
                        project[column] = str(value) if value is not None else ""
                    projects.append(project)
                
                return projects
                
        except sqlite3.Error as e:
            print(f"Error retrieving projects: {e}")
            return []
    
    def get_project_by_id(self, project_id: int) -> Optional[Dict[str, str]]:
        """
        Retrieve a specific project by ID.
        
        Args:
            project_id: The ID of the project to retrieve
            
        Returns:
            Project dictionary or None if not found
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute(
                    f"SELECT * FROM {ProjectSchema.TABLE_NAME} WHERE id = ?", 
                    (project_id,)
                )
                
                row = cursor.fetchone()
                if row:
                    project = {}
                    for column in ProjectSchema.COLUMNS.keys():
                        value = row[column]
                        # Convert boolean field for editing
                        if column == 'is_active':
                            value = 'כן' if value else 'לא'
                        project[column] = str(value) if value is not None else ""
                    return project
                
                return None
                
        except sqlite3.Error as e:
            print(f"Error retrieving project: {e}")
            return None
    
    def update_project(self, project_id: int, project_data: Dict[str, str]) -> Tuple[bool, str]:
        """
        Update an existing project.
        
        Args:
            project_id: ID of the project to update
            project_data: Dictionary containing updated project information
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        # Validate data
        validation_errors = ProjectSchema.validate_project_data(project_data)
        if validation_errors:
            return False, "; ".join(validation_errors)
        
        try:
            # Prepare update statement
            fields = ProjectSchema.DISPLAY_ORDER
            set_clause = ", ".join([f"{field} = ?" for field in fields])
            values = []
            
            for field in fields:
                value = project_data.get(field, '').strip()
                # Convert boolean field
                if field == 'is_active':
                    value = 1 if value.lower() in ['true', '1', 'yes', 'כן'] else 0
                values.append(value)
            
            values.append(project_id)  # Add ID for WHERE clause
            
            sql = f"UPDATE {ProjectSchema.TABLE_NAME} SET {set_clause} WHERE id = ?"
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(sql, values)
                conn.commit()
                
                if cursor.rowcount == 0:
                    return False, "Project not found"
                
                return True, "Project updated successfully"
                
        except sqlite3.Error as e:
            return False, f"Database error: {e}"
    
    def delete_project(self, project_id: int) -> Tuple[bool, str]:
        """
        Delete a project from the database.
        
        Args:
            project_id: ID of the project to delete
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    f"DELETE FROM {ProjectSchema.TABLE_NAME} WHERE id = ?", 
                    (project_id,)
                )
                conn.commit()
                
                if cursor.rowcount == 0:
                    return False, "Project not found"
                
                return True, "Project deleted successfully"
                
        except sqlite3.Error as e:
            return False, f"Database error: {e}"
