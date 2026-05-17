from starlette.requests import Request
from starlette.responses import RedirectResponse

from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend

from app.core.security import create_access_token, verify_password
from app.db.session import engine, SessionLocal
from app.models.order import Order
from app.models.product import Product
from app.models.user import User


class AdminAuth(AuthenticationBackend):
    def __init__(self, secret_key: str):
        super().__init__(secret_key=secret_key)

    async def login(self, request: Request) -> bool:
        form = await request.form()
        email = form.get("username")
        password = form.get("password")

        if not email or not password:
            return False

        with SessionLocal() as db:
            user = db.query(User).filter(User.email == email).first()
            if not user or not user.is_admin or not verify_password(password, user.hashed_password):
                return False

        request.session.update(
            {
                "token": create_access_token(subject=email),
                "admin_email": email,
            }
        )
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool | RedirectResponse:
        token = request.session.get("token")
        if token:
            return True
        return RedirectResponse(url="/admin/login", status_code=302)


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.full_name, User.is_admin, User.created_at]
    form_excluded_columns = [User.hashed_password, User.orders, User.created_at]
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"


class ProductAdmin(ModelView, model=Product):
    column_list = [
        Product.id,
        Product.name,
        Product.price,
        Product.stock,
        Product.is_active,
        Product.created_at,
    ]
    name = "Product"
    name_plural = "Products"
    icon = "fa-solid fa-box"


class OrderAdmin(ModelView, model=Order):
    column_list = [Order.id, Order.user_id, Order.total_amount, Order.status, Order.created_at]
    name = "Order"
    name_plural = "Orders"
    icon = "fa-solid fa-cart-shopping"


def setup_admin(app) -> None:
    from app.core.config import settings

    authentication_backend = AdminAuth(secret_key=settings.secret_key)
    admin = Admin(app, engine, authentication_backend=authentication_backend)
    admin.add_view(UserAdmin)
    admin.add_view(ProductAdmin)
    admin.add_view(OrderAdmin)
