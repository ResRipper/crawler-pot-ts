#!/bin/python3
import json
import sys
from os import environ
from urllib.request import Request
from urllib.request import urlopen

if __name__ == '__main__':
    api_token = environ.get('API_TOKEN')
    zone_id = environ.get('TARGET_ZONE_ID')
    ruleset_id = environ.get('TARGET_RULESET_ID')
    rule_id = environ.get('TARGET_RULE_ID')

    if (zone_id and ruleset_id and api_token and rule_id) is None:
        raise ValueError('ENV not found')

    # Fetch current ruleset
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

            # Find target rule
            for rule in ruleset['result']['rules']:
                if rule['id'] == rule_id:
                    with open('./current_rule.txt', 'r') as f:
                        expression = f.read().strip()

                        # Update current expression
                        with urlopen(
                            Request(
                                url=f'https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets/{ruleset_id}/rules/{rule_id}',
                                method='PATCH',
                                headers={'Authorization': f'Bearer {api_token}'},
                                data=json.dumps(
                                    {
                                        'description': rule['description'],
                                        'action': rule['action'],
                                        'expression': expression,
                                    }
                                ).encode('utf-8'),
                            )
                        ) as req:
                            if req.status == 200:
                                print('Rule updated')
                                sys.exit()
                            else:
                                raise ValueError(f'{req.status}: {req.read().decode("utf-8")}')

            raise ValueError(f'Rule {rule_id} not found')
