import json
from subbridge.providers.liberty import parse_liberty_subscription


def test_parse_vless_reality_node() -> None:
    raw = json.dumps([{
        "remarks": "England",
        "outbounds": [{
            "protocol": "vless",
            "tag": "proxy-1",
            "settings": {
                "vnext": [{
                    "address": "203.0.113.10",
                    "port": 443,
                    "users": [{
                        "id": "00000000-0000-0000-0000-000000000000",
                        "flow": "xtls-rprx-vision",
                    }],
                }]
            },
            "streamSettings": {
                "network": "tcp",
                "security": "reality",
                "realitySettings": {
                    "serverName": "example.com",
                    "fingerprint": "firefox",
                    "publicKey": "public-key",
                    "shortId": "abcd",
                },
            },
        }],
    }])

    nodes = parse_liberty_subscription(raw)
    assert len(nodes) == 1
    assert nodes[0].server == "203.0.113.10"
    assert nodes[0].public_key == "public-key"

def test_skip_unsupported_grpc_node() -> None:
    raw = json.dumps(
        [
            {
                "remarks": "Unsupported gRPC node",
                "outbounds": [
                    {
                        "protocol": "vless",
                        "settings": {
                            "vnext": [
                                {
                                    "address": "203.0.113.20",
                                    "port": 443,
                                    "users": [
                                        {
                                            "id": "00000000-0000-0000-0000-000000000001"
                                        }
                                    ],
                                }
                            ]
                        },
                        "streamSettings": {
                            "network": "grpc",
                            "security": "reality",
                            "realitySettings": {
                                "serverName": "example.com",
                                "publicKey": "public-key",
                                "shortId": "abcd",
                            },
                        },
                    }
                ],
            }
        ]
    )

    try:
        parse_liberty_subscription(raw)
    except Exception as exc:
        assert "No supported VLESS nodes" in str(exc)
    else:
        raise AssertionError("Unsupported gRPC node was not skipped")
