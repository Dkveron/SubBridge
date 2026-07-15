# SubBridge

SubBridge converts provider-specific proxy subscriptions into Mihomo-compatible YAML.

The first supported input format is Liberty's JSON array of Xray configurations.

## MVP

- download a Liberty subscription;
- extract VLESS Reality nodes;
- generate a Mihomo YAML profile;
- keep Russian services direct;
- route selected blocked services through a proxy group.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

subbridge convert   --url "https://example.com/connection/subs/TOKEN"   --output output/mihomo.yaml
```

Never commit a real subscription URL or generated profile containing credentials.

## Tests

```bash
pytest
```
