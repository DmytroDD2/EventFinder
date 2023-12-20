from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.openapi.models import OAuthFlowAuthorizationCode

app = FastAPI()

class OAuth2AuthorizationCodeBearerWithGoogle(OAuth2AuthorizationCodeBearer):
    def __init__(self, tokenUrl: str, authorizationUrl: str, scopes: dict = None, name: str = None, auto_error: bool = True):
        flow = OAuthFlowAuthorizationCode(
            authorizationUrl=authorizationUrl,
            tokenUrl=tokenUrl,
        )
        flows = OAuthFlowsModel(authorizationCode=flow)
        super().__init__(tokenUrl=tokenUrl, flows=flows, scopes=scopes, name=name, auto_error=auto_error)

oauth2_scheme = OAuth2AuthorizationCodeBearerWithGoogle(
    tokenUrl="token",
    authorizationUrl="your_google_authorization_url",
    scopes={"openid": "OpenID Connect"}
)

@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}
