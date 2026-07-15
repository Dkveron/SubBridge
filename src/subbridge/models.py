from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProxyNode:
    name: str
    server: str
    port: int
    uuid: str
    network: str = "tcp"
    tls: bool = True
    flow: str | None = None
    servername: str | None = None
    fingerprint: str | None = None
    public_key: str | None = None
    short_id: str | None = None
