from api import create_app
from configs.config import settings

app = create_app(settings)

if __name__ == '__main__':
    app.run(host=settings.API.SERVER.HOST, port=settings.API.SERVER.PORT)
