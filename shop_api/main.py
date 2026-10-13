import uvicorn
from fastapi import FastAPI
from fastapi_swagger_ui_theme import setup_swagger_ui_theme
from web.exceptions import packaging_errors
from web.lifespan import lifespan
from web.routers import api_router

app = FastAPI(lifespan=lifespan, docs_url=None,
              version="1.0.0", title="ShopAPI", description="Интернет магазин бытовой техники")

setup_swagger_ui_theme(app, docs_path="/swagger/index.html",)
packaging_errors(app)
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)