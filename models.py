# File: models.py
"""
Model layer for the Contact Management System.
Handles all database operations and data persistence.
"""

import sqlite3
import os
from typing import List, Dict, Optional, Tuple
from schema import ContactSchema


class ContactModel:
    """Model class for managing contact data in SQLite database."""
    
    def __init__(self, db_path: str = "contacts.db"):
        """
        Initialize the contact model with database connection.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self) -> None:
        """Initialize database and create contacts table if it doesn't exist."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(ContactSchema.get_create_table_sql())
                conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"Database initialization failed: {e}")
    
    def create_contact(self, contact_data: Dict[str, str]) -> Tuple[bool, str]:
        """
        Create a new contact in the database.
        
        Args:
            contact_data: Dictionary containing contact information
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        # Validate data
        validation_errors = ContactSchema.validate_contact_data(contact_data)
        if validation_errors:
            return False, "; ".join(validation_errors)
        
        try:
            # Prepare data for insertion (exclude id)
            fields = [field for field in ContactSchema.DISPLAY_ORDER]
            values = [contact_data.get(field, '').strip() for field in fields]
            
            placeholders = ", ".join(["?"] * len(fields))
            field_names = ", ".join(fields)
            
            sql = f"INSERT INTO {ContactSchema.TABLE_NAME} ({field_names}) VALUES ({placeholders})"
            
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(sql, values)
                conn.commit()
                
            return True, "Contact created successfully"
            
        except sqlite3.Error as e:
            return False, f"Database error: {e}"
    
    def get_all_contacts(self) -> List[Dict[str, str]]:
        """
        Retrieve all contacts from the database.
        
        Returns:
            List of contact dictionaries
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row  # Enable column access by name
                cursor = conn.execute(f"SELECT * FROM {ContactSchema.TABLE_NAME} ORDER BY last_name, first_name")
                
                contacts = []
                for row in cursor:
                    contact = {}
                    for column in ContactSchema.COLUMNS.keys():
                        contact[column] = str(row[column]) if row[column] is not None else ""
                    contacts.append(contact)
                
                return contacts
                
        except sqlite3.Error as e:
            print(f"Error retrieving contacts: {e}")
            return []
    
    def get_contact_by_id(self, contact_id: int) -> Optional[Dict[str, str]]:
        """
        Retrieve a specific contact by ID.
        
        Args:
            contact_id: The ID of the contact to retrieve
            
        Returns:
            Contact dictionary or None if not found
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute(
                    f"SELECT * FROM {ContactSchema.TABLE_NAME} WHERE id = ?", 
                    (contact_id,)
                )
                
                row = cursor.fetchone()
                if row:
                    contact = {}
                    for column in ContactSchema.COLUMNS.keys():
                        contact[column] = str(row[column]) if row[column] is not None else ""
                    return contact
                
                return None
                
        except sqlite3.Error as e:
            print(f"Error retrieving contact: {e}")
            return None
    
    def update_contact(self, contact_id: int, contact_data: Dict[str, str]) -> Tuple[bool, str]:
        """
        Update an existing contact.
        
        Args:
            contact_id: ID of the contact to update
            contact_data: Dictionary containing updated contact information
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        # Validate data
        validation_errors = ContactSchema.validate_contact_data(contact_data)
        if validation_errors:
            return False, "; ".join(validation_errors)
        
        try:
            # Prepare update statement
            fields = ContactSchema.DISPLAY_ORDER
            set_clause = ", ".join([f"{field} = ?" for field in fields])
            values = [contact_data.get(field, '').strip() for field in fields]
            values.append(contact_id)  # Add ID for WHERE clause
            
            sql = f"UPDATE {ContactSchema.TABLE_NAME} SET {set_clause} WHERE id = ?"
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(sql, values)
                conn.commit()
                
                if cursor.rowcount == 0:
                    return False, "Contact not found"
                
                return True, "Contact updated successfully"
                
        except sqlite3.Error as e:
            return False, f"Database error: {e}"
    
    def delete_contact(self, contact_id: int) -> Tuple[bool, str]:
        """
        Delete a contact from the database.
        
        Args:
            contact_id: ID of the contact to delete
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    f"DELETE FROM {ContactSchema.TABLE_NAME} WHERE id = ?", 
                    (contact_id,)
                )
                conn.commit()
                
                if cursor.rowcount == 0:
                    return False, "Contact not found"
                
                return True, "Contact deleted successfully"
                
        except sqlite3.Error as e:
            return False, f"Database error: {e}"
