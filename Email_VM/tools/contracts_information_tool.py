# programm_details_tool.py

from typing import Optional
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

# Expanded contract tier data in-memory
_CONTRACT_TIERS = {
    "Silver": {
        "MonthlyCost": "€500",
        "AllowanceMax": "Up to 100 service-units/month",
        "Positioning": "Entry-level contract: basic service with core features",
        "Features": "Basic access, standard support, limited extras",
        "TargetClients": "Smaller clients, new customers",
        "Notes": "Good ‘foot-in-door’ tier; upsell potential"
    },
    "Gold": {
        "MonthlyCost": "€1,200",
        "AllowanceMax": "Up to 300 service-units/month",
        "Positioning": "Mid-tier: elevated level of service",
        "Features": "More features, faster support, moderate extras",
        "TargetClients": "Growing clients, committed users",
        "Notes": "Balanced value vs cost"
    },
    "Metal": {
        "MonthlyCost": "€2,500",
        "AllowanceMax": "Up to 700 service-units/month",
        "Positioning": "Premium tier: many features, high-service level",
        "Features": "Dedicated support, advanced features, higher limits",
        "TargetClients": "Larger clients, high demand",
        "Notes": "Name is non-typical — consider ‘Platinum’"
    },
    "Diamond": {
        "MonthlyCost": "€5,000",
        "AllowanceMax": "Up to 1,500 service-units/month",
        "Positioning": "Top-tier: highest service level",
        "Features": "All features, premium support, VIP perks",
        "TargetClients": "Key accounts, enterprise clients",
        "Notes": "Reserved-tier; highest price point"
    }
}

@tool(
    name="contracts_information",
    description="Used to retrieve information about the contract that a user has with the company. Input is one of the contract types.",
    permission=ToolPermission.READ_ONLY
)
def contracts_information(contract_type: Optional[str] = None) -> str:
    """
    If a tier is specified (e.g., 'Gold'), returns details for that tier.
    If no tier is specified, returns the full table of all tiers.
    """
    if contract_type:
        t = contract_type.strip().title()
        if t not in _CONTRACT_TIERS:
            return f"contract type '{contract_type}' not found. Available tiers: {', '.join(_CONTRACT_TIERS.keys())}."
        data = _CONTRACT_TIERS[t]
        return (
            f"**{t} Tier**\n"
            f"Monthly Cost: {data['MonthlyCost']}\n"
            f"Allowance Max: {data['AllowanceMax']}\n"
            f"Positioning: {data['Positioning']}\n"
            f"Features: {data['Features']}\n"
            f"Target Clients: {data['TargetClients']}\n"
            f"Notes: {data['Notes']}\n"
        )
    else:
        # Build full table header
        lines = []
        lines.append("| Tier     | Monthly Cost | Allowance Max               | Positioning                                    | Features                                       | Target Clients                          | Notes                                      |")
        lines.append("|----------|--------------|-----------------------------|------------------------------------------------|------------------------------------------------|------------------------------------------|---------------------------------------------|")
        for tier_name, data in _CONTRACT_TIERS.items():
            lines.append(
                f"| {tier_name:<8} | {data['MonthlyCost']:<12} | {data['AllowanceMax']:<27} | {data['Positioning']:<46} | {data['Features']:<44} | {data['TargetClients']:<40} | {data['Notes']:<41} |"
            )
        return "\n".join(lines)