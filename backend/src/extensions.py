from flask_caching import Cache
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_smorest import Api
from imagekitio import ImageKit

jwt = JWTManager()
cors = CORS()
api = Api()
imagekit = ImageKit()
cache = Cache()
