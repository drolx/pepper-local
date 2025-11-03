from pydantic import BaseModel


class ResolverEndpointOption(BaseModel):
    auth: bool | None = False
    path: str | None = None
    timeout: float = 30
    headers: dict[str, str] | None = {}
    
    def get_auth(self):
        return self.auth

class ResolverEndpoint(BaseModel):
    login: ResolverEndpointOption | None = ResolverEndpointOption()
    device: ResolverEndpointOption | None = ResolverEndpointOption()
    position: ResolverEndpointOption | None = ResolverEndpointOption()
    geofence: ResolverEndpointOption | None = ResolverEndpointOption()
    forward: ResolverEndpointOption | None = ResolverEndpointOption()
    

