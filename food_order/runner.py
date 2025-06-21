from google.adk.runners import Runner
from google.adk.sessions import Session
from google.adk.artifacts import InMemoryArtifactService
from .agent import root_agent

def get_runner(app_name: str, session: Session, artifact: InMemoryArtifactService):
    return Runner(
        agent = root_agent,
        app_name = app_name,
        session_service = session,
        artifact_service = artifact
    )
