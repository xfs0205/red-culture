import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# 导入模块路由
from routers.modules.test1 import router as test_router

# 静态文件类
class NoCacheStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        response = await super().get_response(path, scope)
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

# 路由类
class Route:
    def __init__(self, host, port,img_path,video_path,
                 allow_origins,
                 allow_credentials,
                 allow_methods,
                 allow_headers
                 ):
        self.app = FastAPI(title="红色文化")
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=allow_origins,
            allow_credentials=allow_credentials,
            allow_methods=allow_methods,
            allow_headers=allow_headers,
        )
        self.host = host
        self.port = port

        # ---------------------------添加静态文件路由---------------------------
        self.app.mount("/backend/static_video",
                       StaticFiles(directory=video_path),
                       name="static")

        self.app.mount("/backend/static_image",
                       NoCacheStaticFiles(directory=img_path),
                       name="static")

        # ---------------------------添加模块路由---------------------------
        self.app.include_router(test_router)

    def run(self):
        # 运行服务
        uvicorn.run(self.app, host=self.host, port=self.port)
