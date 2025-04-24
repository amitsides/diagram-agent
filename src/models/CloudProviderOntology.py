from pydantic import BaseModel, Field
from typing import List, Optional

class ServiceComponent(BaseModel):
    generic_type: str = Field(..., description="Generic classification of the service component")
    description: str = Field(..., min_length=10, max_length=200)
    examples_in_code: List[str] = Field(..., min_items=1)

class CloudProviderOntology(BaseModel):
    aws_network: Optional[List[ServiceComponent]] = Field(
        None, alias="aws.network", description="Network-related services"
    )
    aws_compute: Optional[List[ServiceComponent]] = Field(
        None, alias="aws.compute", description="Compute resources and services"
    )
    aws_database: Optional[List[ServiceComponent]] = Field(
        None, alias="aws.database", description="Database services and storage solutions"
    )
    aws_integration: Optional[List[ServiceComponent]] = Field(
        None, alias="aws.integration", description="Integration and messaging services"
    )
    aws_analytics: Optional[List[ServiceComponent]] = Field(
        None, alias="aws.analytics", description="Data processing and analytics tools"
    )
    aws_management: Optional[List[ServiceComponent]] = Field(
        None, alias="aws.management", description="Monitoring and management services"
    )