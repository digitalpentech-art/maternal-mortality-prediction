from pydantic import BaseModel, Field

class PatientDataSchema(BaseModel):
    Age: int = Field(..., gt=0)
    Marital_Status: int
    Education: int
    Occupation: int
    Income: int
    Location: int
    Gravida: int = Field(..., ge=0)
    Para: int = Field(..., ge=0)
    Miscarriage_Stillbirth: int = Field(..., ge=0)
    ANCV: int = Field(..., ge=0)
    Delivery_Mode: int
    Complications: int
    PreEC: int
    HFT: int
    ECA: int
    SM: int
