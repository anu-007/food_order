from google.adk.sessions import DatabaseSessionService, Session

class CustomSessionService(DatabaseSessionService):
    def __init__(self, db_url: str = "sqlite:///./my_agent_data.db"):
        super().__init__(db_url)
    
    async def filter_events(self, app: str, user: str, sess: str) -> Session:
        """
        Post-process session events to remove internal tool calls.
        
        Args:
            app: Application name
            user: User ID 
            sess: Session ID
            
        Returns:
            Session with filtered events
        """

        # Get current session from database
        current_session = await self.get_session(
            app_name=app,
            user_id=user,
            session_id=sess
        )
        
        if not current_session:
            raise ValueError(f"No session found for {app}/{user}/{sess}")

        filtered_events = []
        print('=======current_session.events before==========',len(current_session.events))
        
        # Filter events without modifying DB
        for event in current_session.events:
            if event.author == 'user':
                filtered_events.append(event)
            
            if hasattr(event, 'is_final_response') and event.is_final_response():
                filtered_events.append(event)
                continue

        # Update only the filtered session's events
        current_session.events = filtered_events
        print('========filtered_session.events after=========', len(current_session.events))
        
        return current_session

async def get_session(app_name: str, user_id: str, session_id: str):
    try:
        session_service = CustomSessionService()
        session = await session_service.get_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id
        )
        return session
    except Exception as e:
        print(f"An error occurred: {e}")