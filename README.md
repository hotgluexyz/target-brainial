# target-brainial

`target-brainial` is a Singer target for [Brainial](https://app.brainial.com), a tender management platform. It writes Tender records to the Brainial API, supporting both create and update operations.

Built with the [Hotglue Singer SDK](https://github.com/hotgluexyz/HotglueSingerSDK) for Singer Targets.

## Installation

```bash
pip install target-brainial
```

Or install from source:

```bash
pip install git+https://github.com/hotgluexyz/target-brainial.git
```

## Configuration

| Field          | Required | Description                                                    |
|----------------|----------|----------------------------------------------------------------|
| `access_token` | Yes      | Bearer token obtained from the Brainial user session/cookies   |

Example `config.json`:

```json
{
    "access_token": "<your-jwt-bearer-token>"
}
```

## Source Authentication and Authorization

Brainial uses JWT Bearer tokens for authentication. The token is tied to a specific user and organisation and can be obtained from the browser's user session cookies after logging into [app.brainial.com](https://app.brainial.com).

Pass the token as the `access_token` field in your config. The token is sent via the `Authorization: Bearer <token>` header on every request.

## Supported Streams

| Stream    | Description                                                                   |
|-----------|-------------------------------------------------------------------------------|
| `tenders` | Creates or updates Tender records in Brainial via `POST /tenders/`. If `new_tender_id` is present in the record, the API upserts against that ID; otherwise a UUID is generated automatically. |

The target expects records that are already mapped to the Brainial Tender API field names (no additional field mapping is applied).

## Usage

Pipe a tap or a Singer file into the target:

```bash
cat sample_payload/data.singer | target-brainial --config config.json
```

Or with a tap:

```bash
tap-salesforce --config tap_config.json | target-brainial --config config.json
```

## Developer Resources

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install in editable mode with dev dependencies
pip install -e .
pip install ruff pytest

# Run linter
ruff check .

# Run tests (requires .secrets/config.json)
pytest target_brainial/tests/

# Verify CLI
target-brainial --version
target-brainial --about
```
