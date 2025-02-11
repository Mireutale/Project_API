# dependencies.py
from sqlmodel import Session, create_engine, SQLModel
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
# 모델들을 임포트
from app.models.models import User, Product, Category, ProductImage, Likes, Comment  
from fastapi import UploadFile
# 데이터베이스 URL 설정 (여기서는 SQLite 사용)
db_file_name = "carrot.db"
db_url = f"sqlite:///./{db_file_name}"
# 여러 스레드에서 SQLite 연결을 공유할 수 있도록 설정
db_conn_args = {"check_same_thread": False}
# 데이터베이스 엔진 생성, 데이터베이스와의 실제 연결 관리
db_engine = create_engine(db_url, connect_args=db_conn_args)

# 데이터베이스와의 연결 관리를 Session으로 수행
def get_db_session():
    with Session(db_engine) as session:
        yield session

# 데이터베이스 테이블 생성 함수
def create_db_and_tables():
    SQLModel.metadata.create_all(db_engine)

# JSW
# dependencies.py -> dependencies/io.py, db.py로 모듈화 하면 예쁠 듯듯
# 팀원과 상의 해야할 듯
import os
import uuid
import time
from typing import Optional
from pathlib import Path
UPLOAD_DIR = Path("./uploads")
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif"}

def create_upload_dir():
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

def is_allowed_file(filename: str) -> bool:
    return '.' in filename and filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS

def unique_filename(filename: str) -> str:
    ext = filename.split('.')[-1]
    return f"{int(time.time())}_{uuid.uuid4().hex}.{ext}"

async def save_UploadFile(file: UploadFile) -> Optional[str]:
    if not is_allowed_file(file.filename):
        return None
    
    file_name = unique_filename(file.filename)
    file_path = UPLOAD_DIR / file_name
    if os.path.exists(file_path):
        return None
    
    with open(file_path, "wb") as file_object:
        data = await file.read()
        file_object.write(data)
    return file_name

def delete_file(file_name: str) -> bool:
    file_path = UPLOAD_DIR / file_name
    if not os.path.exists(file_path):
        return False
    os.remove(file_path)
    return True