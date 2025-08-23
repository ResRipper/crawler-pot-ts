export default {
	async fetch(request: Request, env: Env): Promise<Response> {

		const asn = request.cf?.asn;

		const cf_asn = [13335, 132892]; // Cloudflare ASN list

		if (!cf_asn.includes(asn as number)) { // Prevent adding CF ASN

			if (asn == undefined) {
				console.log('ASN or cf object not found');
				return new Response('');
			}

			const rulesetResponse = await fetch(
				`https://api.cloudflare.com/client/v4/zones/${env.ZONE_ID}/rulesets/${env.RULESET_ID}`,
				{
					headers: { 'Authorization': `Bearer ${env.API_TOKEN}` }
				}
			);

			const ruleset = await rulesetResponse.json() as any;
			const rule = ruleset.result.rules.find((r: any) => r.id === env.RULE_ID);

			if (!rule) {
				console.log('Rule not found');
				return new Response('');
			}

			const asnList = rule.expression.split('{')[1].split('}')[0].split(' ');

			if (asnList.includes(String(asn))) {
				console.warn(`ASN ${asn} already exist`);
				return new Response('');
			}

			asnList.push(String(asn));

			await fetch(
				`https://api.cloudflare.com/client/v4/zones/${env.ZONE_ID}/rulesets/${env.RULESET_ID}/rules/${env.RULE_ID}`,
				{
					method: 'PATCH',
					headers: {
						'Authorization': `Bearer ${env.API_TOKEN}`,
						'Content-Type': 'application/json'
					},
					body: JSON.stringify({
						description: rule.description,
						action: rule.action,
						expression: `(ip.src.asnum in {${asnList.join(' ')}})`
					})
				}
			);

			console.log(`Added AS${asn}, from ${request.cf?.country}, ${request.cf?.city}, ${request.headers.get("CF-Connecting-IP")}`);
			return new Response('');
		} else {
			console.log('Cloudflare ASN');
			return new Response('');
		}
	},
} satisfies ExportedHandler<Env>;

interface Env {
	API_TOKEN: string;
	ZONE_ID: string;
	RULESET_ID: string;
	RULE_ID: string;
}
