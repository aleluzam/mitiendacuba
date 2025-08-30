from app.database import db
from pydantic import BaseModel, Field, ConfigDict

class SectionTable(db.Model):
    __tablename__ = "sections"
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    img = db.Column(db.String(300))
    description = db.Column(db.String(500))
    
    def get_name(self):
        return f"{self.name}"
    
class SectionCreate(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    
    name: str = Field( min_length=5, max_length=100)
    img: str = Field(max_length=300)
    description: str = Field(min_length=15, max_length=500)
    
class SectionPublic(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    
    name: str = Field( min_length=5, max_length=100)
    img: str = Field(max_length=300)
    id: int
    
class SectionUpdate(BaseModel):
    name: str | None = Field(None, min_length=5, max_length=100)
    img: str | None = Field(None, max_length=300)
    description: str | None = Field(None, min_length=15, max_length=500)

    
    
    
    
    