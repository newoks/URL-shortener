from app.internal.pkg.models import Routes
from app.internal.routes import shortener

__all__ = ["__routes__"]


__routes__ = Routes(routers=(shortener.router,))
