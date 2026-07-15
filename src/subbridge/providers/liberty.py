from __future__ import annotations

import json
from typing import Any

from subbridge.models import ProxyNode


class LibertyParseError(ValueError):
    pass


def parse_liberty_subscription(raw: str) -> list[ProxyNode]:
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise LibertyParseError(f"Subscription is not valid JSON: {exc}") from exc

    if not isinstance(payload, list):
        raise LibertyParseError("Expected a JSON array of Xray configurations")

    nodes: list[ProxyNode] = []
    seen: set[tuple[str, int, str]] = set()

    for config in payload:
        if not isinstance(config, dict):
            continue
        remarks = str(config.get("remarks") or "Liberty node")
        outbounds = config.get("outbounds")
        if not isinstance(outbounds, list):
            continue

        for outbound in outbounds:
            node = _parse_vless_outbound(outbound, remarks)
            if node is None:
                continue
            key = (node.server, node.port, node.uuid)
            if key not in seen:
                seen.add(key)
                nodes.append(node)

    if not nodes:
        raise LibertyParseError("No supported VLESS nodes were found")
    return nodes


def _parse_vless_outbound(outbound: Any, remarks: str) -> ProxyNode | None:
    if not isinstance(outbound, dict) or outbound.get("protocol") != "vless":
        return None

    vnext = outbound.get("settings", {}).get("vnext")
    if not isinstance(vnext, list) or not vnext:
        return None

    target = vnext[0]
    users = target.get("users")
    if not isinstance(users, list) or not users:
        return None

    user = users[0]
    server = target.get("address")
    port = target.get("port")
    uuid = user.get("id")
    if not server or not isinstance(port, int) or not uuid:
        return None

    stream = outbound.get("streamSettings", {})
    network = str(stream.get("network") or "tcp")
    security = stream.get("security")
    tls_enabled = security in {"tls", "reality"}

    servername = fingerprint = public_key = short_id = None
    if security == "reality":
        reality = stream.get("realitySettings", {})
        servername = reality.get("serverName")
        fingerprint = reality.get("fingerprint")
        public_key = reality.get("publicKey")
        short_id = reality.get("shortId")
    elif security == "tls":
        servername = stream.get("tlsSettings", {}).get("serverName")

    tag = str(outbound.get("tag") or "")
    name = remarks if not tag else f"{remarks} | {tag}"

    return ProxyNode(
        name=name,
        server=str(server),
        port=port,
        uuid=str(uuid),
        network=network,
        tls=tls_enabled,
        flow=user.get("flow") or None,
        servername=servername,
        fingerprint=fingerprint,
        public_key=public_key,
        short_id=short_id,
    )
