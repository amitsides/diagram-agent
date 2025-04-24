
from .models import CloudProviderOntology 
from google.genai.types import GenerateContentConfig, Part, EmbedContentConfig
import json

class DiagramAgent():
    def __init__(self, query):
        self.query = query
        self.client = genai.Client(api_key='GEMINI_API_KEY')
        self.diagramOntology = json.loads(f = open("aws.json", "r"))
        self.architectureOntology = self.query_to_pydantic_ontology(query)

    def query_to_pydantic_ontology(self, query):
      response = self.client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=[
              text
            ],
            config=GenerateContentConfig(
              system_instruction=self.UserArchitectureIntention(query),
              temperature=0,
              response_mime_type=JSON_MIME_TYPE,
              response_schema=CloudProviderOntology,
            ),
        )
      return json.loads(response.text)

    def UserArchitectureIntention(self, query):
        return self.query_to_pydantic_ontology('given the user query {query} return a CloudProviderOntology which is the user intention for his cloud infrastructure architecture sugges the best possible architecture')
    
    def json_to_diagram():
        