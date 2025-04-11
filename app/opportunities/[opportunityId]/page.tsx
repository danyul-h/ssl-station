import { Opportunity } from "@/lib/types";

export default async function OpportunityDetails({
	params,
}: {
	params: {opportunityId:string}
}) {
	const res = await fetch(`http://localhost:5000/api/opportunities/${params.opportunityId}`);
	const opportunity: Opportunity = await res.json();
	return <p>{opportunity.title}</p>
}