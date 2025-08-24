#!/bin/python3
import json
import sys
from os import environ
from urllib.request import Request
from urllib.request import urlopen

if __name__ == '__main__':
    zone_id = environ.get('ZONE_ID')
    ruleset_id = environ.get('RULESET_ID')
    api_token = environ.get('API_TOKEN')
    rule_id = environ.get('RULE_ID')

    if (zone_id and ruleset_id and api_token and rule_id) is None:
        raise ValueError('ENV not found')

    with urlopen(
        Request(
            url=f'https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets/{ruleset_id}',
            method='GET',
            headers={'Authorization': f'Bearer {api_token}'},
        )
    ) as req:
        if req.status != 200:
            raise ValueError(f'{req.status}: {req.read().decode("utf-8")}')
        else:
            ruleset: dict = json.loads(req.read().decode('utf-8'))

            for item in ruleset['result']['rules']:
                if item['id'] == rule_id:
                    rule = item['expression']
                    print(f'Current rule: {rule}')

                    # Overwrite currrent file
                    with open('./current_rule.txt', 'w') as f:
                        f.truncate()
                        f.write(rule)
                        sys.exit()

            raise ValueError(f'Rule {rule_id} not found')
