import json
from fastapi import WebSocket

class WSManager:
    def __init__(self):
        self.rooms: dict[int, set[WebSocket]] = {}  # 채팅방 ID -> 연결된 WebSocket 목록

    async def connect(self, ws: WebSocket, chatroom_id: int, user_id: int):
        """사용자를 특정 채팅방에 연결"""
        await ws.accept()
        if chatroom_id not in self.rooms:
            self.rooms[chatroom_id] = set()
        self.rooms[chatroom_id].add(ws)

        # ✅ JSON 형식으로 입장 메시지 전송
        message = json.dumps({
            "type": "enter",
            "chatroom_id": chatroom_id,
            "user_id": user_id,
            "message": f"사용자 {user_id}가 입장했습니다."
        })
        await self.send_to_room(chatroom_id, message)

    def disconnect(self, ws: WebSocket, chatroom_id: int, user_id: int):
        """사용자가 채팅방에서 나갔을 때"""
        if chatroom_id in self.rooms:
            self.rooms[chatroom_id].discard(ws)
            if not self.rooms[chatroom_id]:  # 방이 비었으면 삭제
                del self.rooms[chatroom_id]

    async def send_to_room(self, chatroom_id: int, message: str):
        """같은 채팅방에 있는 사용자들에게 메시지 전송"""
        if chatroom_id in self.rooms:
            for ws in self.rooms[chatroom_id]:
                await ws.send_json(message)

ws_manager = WSManager()
