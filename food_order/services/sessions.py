from google.adk.sessions import InMemorySessionService
from google.adk.sessions import Session

class CustomSessionService(InMemorySessionService):
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
        filtered_events = []
        current_session = await self.get_session(
            app_name=app,
            user_id=user,
            session_id=sess
        )

        print('=======current_session.events before==========', len(current_session.events))
        print("========= after print =============")
        for event in current_session.events:
            # Keep user events
            if event.author == 'user':
                filtered_events.append(event)
                continue
            
            # Keep final response events
            if hasattr(event, 'is_final_response') and event.is_final_response():
                filtered_events.append(event)
                continue

        current_session.events = filtered_events
        print('========current_session.events after=========', len(current_session.events))
        print("========= after finish =============")
        return current_session

async def get_session(app_name: str, user_id: str, session_id: str):
    try:
        session_service = CustomSessionService()
        await session_service.create_session(
            app_name = app_name, user_id = user_id, session_id = session_id
        )
        return session_service
    except Exception as e:
        print(f"An error occurred: {e}")