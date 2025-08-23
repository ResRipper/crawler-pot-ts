# Crawler pot - TS

A Cloudflare Worker that adds the ASN of incoming requests to a WAF rule.

## Prerequisites

- [API token](https://dash.cloudflare.com/profile/api-tokens) with `Zone > Zone WAF` permission
- A security rule with `AS Num` > `is in` > `Some ASN` as the configuration and its:

	> You can find these in the `Save with API call` tab at the bottom of the security rule edit window

  - Zone ID
  - Rule set ID
  - Rule ID

## Usage

1. Create a `.env` file:

    ```ini
    API_TOKEN=...
    ZONE_ID=...
    RULESET_ID=...
    RULE_ID=...
    ```

2. Deploy

    ```sh
    wrangler deploy
    ```

3. Upload secrets

    ```sh
    wrangler secret bulk .env
    ```

4. Go the the worker's setting tab, add some routes that only crawlers will access
