from google.adk.sessions import InMemorySessionService

def get_session(app_name: str, user_id: str, session_id: str):
    try:
        session_service = InMemorySessionService()
        session_service.create_session(
            app_name = app_name, user_id = user_id, session_id = session_id
        )
        return session_service
    except Exception as e:
        print(f"An error occurred: {e}")