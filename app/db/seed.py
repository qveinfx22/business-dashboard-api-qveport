from app.core.config import settings
from app.core.security import get_password_hash
from app.db.session import SessionLocal
from app.models.user import User


def seed_admin_user() -> None:
    with SessionLocal() as db:
        existing_user = db.query(User).filter(User.email == settings.admin_email).first()
        if existing_user:
            return

        admin = User(
            email=settings.admin_email,
            full_name="Admin User",
            hashed_password=get_password_hash(settings.admin_password),
            is_admin=True,
        )
        db.add(admin)
        db.commit()
