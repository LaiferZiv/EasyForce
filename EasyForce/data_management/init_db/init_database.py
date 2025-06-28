from EasyForce.data_management.init_db.init_entities import init_entities
from EasyForce.data_management.init_db.init_relationships import init_relationships
from EasyForce.data_management.init_db.init_triggers import init_triggers

def initialize_database():
    """Initialize the database and create all necessary tables."""
    if not init_entities():
        return False
    if not init_relationships():
        return False
    if not init_triggers():
        return False
    return True