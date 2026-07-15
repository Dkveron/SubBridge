
# SubBridge
SubBridge converts provider-specific proxy subscriptions into Mihomo-compatible YAML profiles.
The project was created because Liberty provides subscriptions as an array of Xray JSON configurations, which Nikki and Mihomo cannot import directly.
SubBridge downloads the subscription, extracts supported VLESS nodes and generates a valid Mihomo profile.
## Features
- Liberty JSON subscription support
- VLESS Reality node extraction
- Mihomo YAML generation
- Automatic proxy selection with `url-test`
- Routing rules for ChatGPT, YouTube, Instagram and Telegram
- Direct routing for Russian services and banks
- Automated profile generation with GitHub Actions
- OpenWrt and Nikki compatibility
- Safe validation before deployment
- Automatic rollback on the router
## Architecture
```text
Liberty subscription
        |
        v
GitHub Actions
        |
        v
SubBridge converter
        |
        v
Mihomo YAML profile
        |
        v
Private configuration repository
        |
        v
OpenWrt router
        |
        v
Nikki / Mihomo

Requirements

* Python 3.11 or newer
* A supported Liberty subscription
* Mihomo or Nikki for using the generated profile

Installation

git clone https://github.com/Dkveron/SubBridge.git
cd SubBridge
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e ".[dev]"

Usage

Set the subscription URL without saving it in the repository:

export LIBERTY_URL="https://example.com/connection/subs/TOKEN"

Generate a Mihomo profile:

subbridge convert \
  --provider liberty \
  --url "$LIBERTY_URL" \
  --output output/liberty.yaml

Example output:

Generated output/liberty.yaml with 28 nodes

Validate the generated profile with Mihomo:

mihomo -t -f output/liberty.yaml

Tests

ruff check .
pytest

GitHub Actions

The included workflow can:

1. Download a Liberty subscription using a GitHub Secret.
2. Convert it into Mihomo YAML.
3. Save the generated profile in a private repository.
4. Allow an OpenWrt router to download and validate updates automatically.

Required secrets in the public SubBridge repository:

* LIBERTY_URL
* CONFIG_REPO_TOKEN

Never commit a real subscription URL or generated profile containing credentials.

OpenWrt automation

A router-side update script can:

* download the latest profile;
* validate it with mihomo -t;
* create a backup;
* restart Nikki;
* restore the previous profile if startup fails.

Security

Generated profiles may contain UUIDs, server addresses and authentication parameters.

Keep the following private:

* subscription URLs;
* generated profiles;
* GitHub access tokens;
* router credentials.

Roadmap

* More Xray transport types
* Provider adapters
* Configurable routing rules
* Country filtering
* Improved CLI errors
* OpenWrt installer
* Docker image
* Web interface

License

MIT
EOF
