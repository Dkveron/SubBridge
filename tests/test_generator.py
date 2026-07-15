import yaml
from subbridge.generator import generate_mihomo_config
from subbridge.models import ProxyNode


def test_generate_mihomo_yaml() -> None:
    node = ProxyNode(
        name="England",
        server="203.0.113.10",
        port=443,
        uuid="00000000-0000-0000-0000-000000000000",
        flow="xtls-rprx-vision",
        servername="example.com",
        fingerprint="firefox",
        public_key="public-key",
        short_id="abcd",
    )
    result = yaml.safe_load(generate_mihomo_config([node]))
    assert result["proxies"][0]["type"] == "vless"
    assert result["proxy-groups"][0]["name"] == "PROXY"
    assert "DOMAIN-SUFFIX,chatgpt.com,PROXY" in result["rules"]
    assert result["rules"][-1] == "MATCH,DIRECT"
