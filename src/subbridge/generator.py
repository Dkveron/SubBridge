from __future__ import annotations

from typing import Iterable
import yaml

from subbridge.models import ProxyNode

DIRECT_DOMAINS = [
    "tbank.ru", "tinkoff.ru", "alfabank.ru", "sberbank.ru",
    "gosuslugi.ru", "yandex.ru", "vk.com", "mail.ru",
]

PROXY_DOMAINS = [
    "openai.com", "chatgpt.com", "oaistatic.com", "oaiusercontent.com",
    "youtube.com", "youtu.be", "googlevideo.com", "ytimg.com",
    "youtubei.googleapis.com", "youtube.googleapis.com", "ggpht.com",
    "instagram.com", "cdninstagram.com", "facebook.com", "fbcdn.net",
    "t.me", "telegram.org", "telesco.pe", "telegra.ph",
]

TELEGRAM_CIDRS = ["91.108.0.0/16", "149.154.160.0/20"]


def generate_mihomo_config(nodes: Iterable[ProxyNode]) -> str:
    node_list = list(nodes)
    if not node_list:
        raise ValueError("At least one proxy node is required")

    proxies = [_node_to_mihomo(node) for node in node_list]
    names = [node.name for node in node_list]

    rules = [f"DOMAIN-SUFFIX,{domain},DIRECT" for domain in DIRECT_DOMAINS]
    rules += [f"DOMAIN-SUFFIX,{domain},PROXY" for domain in PROXY_DOMAINS]
    rules += [f"IP-CIDR,{cidr},PROXY,no-resolve" for cidr in TELEGRAM_CIDRS]
    rules += ["GEOIP,RU,DIRECT", "MATCH,DIRECT"]

    config = {
        "mixed-port": 7890,
        "allow-lan": True,
        "mode": "rule",
        "log-level": "info",
        "ipv6": False,
        "proxies": proxies,
        "proxy-groups": [{
            "name": "PROXY",
            "type": "url-test",
            "url": "https://www.gstatic.com/generate_204",
            "interval": 300,
            "tolerance": 100,
            "proxies": names,
        }],
        "rules": rules,
    }
    return yaml.safe_dump(config, allow_unicode=True, sort_keys=False)


def _node_to_mihomo(node: ProxyNode) -> dict:
    result = {
        "name": node.name,
        "type": "vless",
        "server": node.server,
        "port": node.port,
        "uuid": node.uuid,
        "network": node.network,
        "tls": node.tls,
        "udp": True,
    }
    if node.flow:
        result["flow"] = node.flow
    if node.servername:
        result["servername"] = node.servername
    if node.fingerprint:
        result["client-fingerprint"] = node.fingerprint
    if node.public_key or node.short_id:
        result["reality-opts"] = {
            key: value for key, value in {
                "public-key": node.public_key,
                "short-id": node.short_id,
            }.items() if value
        }
    return result
