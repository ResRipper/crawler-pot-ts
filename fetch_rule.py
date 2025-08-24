#!/bin/python3
import json
from urllib.request import urlopen, Request
from os import environ

if __name__ == "__main__":
    zone_id = environ.get("ZONE_ID")
    ruleset_id = environ.get("RULESET_ID")
    api_token = environ.get("API_TOKEN")
    rule_id = environ.get("RULE_ID")

    if zone_id and ruleset_id and api_token and rule_id is None:
        exit('ENV not found')

    with urlopen(
        Request(
            url=f"https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets/{ruleset_id}",
            method="GET",
            headers={"Authorization": f"Bearer {api_token}"},
        )
    ) as req:
        ruleset = json.loads(req.read().decode("utf-8"))

        for item in ruleset["result"]["rules"]:
            if item["id"] == rule_id:
                rule = item["expression"]
                print(f'Current rule: {rule}')

                with open("./current_rule.txt", "w") as f:
                    f.truncate()
                    f.write(rule)
