# client_lookup_tool.py

from typing import Optional
from ibm_watsonx_orchestrate.agent_builder.tools import tool

# In-memory data for 50 clients:
_CLIENTS = [
    {"FirstName": "Arianna",   "LastName": "Petrova",        "Email": "arianna.petrova@example.com",         "ContractType": "Gold",    "PaymentType": "card"},
    {"FirstName": "Dimitris",  "LastName": "Kotsios",        "Email": "dimitris.kotsios@example.com",        "ContractType": "Silver",  "PaymentType": "cash"},
    {"FirstName": "Eleni",     "LastName": "Nikolaou",       "Email": "eleni.nikolaou@example.com",          "ContractType": "Metal",   "PaymentType": "card"},
    {"FirstName": "Panagiotis","LastName": "Markos",         "Email": "panagiotis.markos@example.com",       "ContractType": "Diamond", "PaymentType": "cash"},
    {"FirstName": "Maria",     "LastName": "Ioannidou",      "Email": "maria.ioannidou@example.com",         "ContractType": "Gold",    "PaymentType": "card"},
    {"FirstName": "Georgios",  "LastName": "Vasilakis",      "Email": "georgios.vasilakis@example.com",      "ContractType": "Silver",  "PaymentType": "cash"},
    {"FirstName": "Anna",      "LastName": "Papadopoulou",   "Email": "anna.papadopoulou@example.com",       "ContractType": "Metal",   "PaymentType": "card"},
    {"FirstName": "Nikos",     "LastName": "Stavrou",        "Email": "nikos.stavrou@example.com",           "ContractType": "Diamond", "PaymentType": "cash"},
    {"FirstName": "Katerina",  "LastName": "Georgiou",       "Email": "katerina.georgiou@example.com",        "ContractType": "Gold",    "PaymentType": "card"},
    {"FirstName": "Leonidas",  "LastName": "Pappas",         "Email": "leonidas.pappas@example.com",         "ContractType": "Silver",  "PaymentType": "cash"},
    {"FirstName": "Zoe",       "LastName": "Karagianni",    "Email": "zoe.karagianni@example.com",           "ContractType": "Metal",   "PaymentType": "card"},
    {"FirstName": "Alexis",    "LastName": "Dimitriadis",    "Email": "alexis.dimitriadis@example.com",       "ContractType": "Diamond", "PaymentType": "cash"},
    {"FirstName": "Ioanna",    "LastName": "Christodoulou",  "Email": "ioanna.christodoulou@example.com",     "ContractType": "Gold",    "PaymentType": "card"},
    {"FirstName": "Thanos",    "LastName": "Economou",       "Email": "thanos.economou@example.com",           "ContractType": "Silver",  "PaymentType": "cash"},
    {"FirstName": "Sofia",     "LastName": "Konstantinou",  "Email": "sofia.konstantinou@example.com",       "ContractType": "Metal",   "PaymentType": "card"},
    {"FirstName": "Spyros",    "LastName": "Nikolaidis",     "Email": "spyros.nikolaidis@example.com",        "ContractType": "Diamond", "PaymentType": "cash"},
    {"FirstName": "Elpida",    "LastName": "Panou",          "Email": "elpida.panou@example.com",              "ContractType": "Gold",    "PaymentType": "card"},
    {"FirstName": "Marios",    "LastName": "Papageorgiou",   "Email": "marios.papageorgiou@example.com",       "ContractType": "Silver",  "PaymentType": "cash"},
    {"FirstName": "Olga",      "LastName": "Michailidou",    "Email": "olga.michailidou@example.com",          "ContractType": "Metal",   "PaymentType": "card"},
    {"FirstName": "Vasilis",   "LastName": "Karalis",        "Email": "vasilis.karalis@example.com",           "ContractType": "Diamond", "PaymentType": "cash"},
    {"FirstName": "Helen",     "LastName": "Pallis",         "Email": "helen.pallis@example.com",               "ContractType": "Gold",    "PaymentType": "card"},
    {"FirstName": "Andreas",   "LastName": "Mouzakis",       "Email": "andreas.mouzakis@example.com",           "ContractType": "Silver",  "PaymentType": "cash"},
    {"FirstName": "Kiki",      "LastName": "Vogiatzis",      "Email": "kiki.vogiatzis@example.com",             "ContractType": "Metal",   "PaymentType": "card"},
    {"FirstName": "Petros",    "LastName": "Sarris",         "Email": "petros.sarris@example.com",              "ContractType": "Diamond", "PaymentType": "cash"},
    {"FirstName": "Sophia",    "LastName": "Hadjichristos",  "Email": "sophia.hadjichristos@example.com",       "ContractType": "Gold",    "PaymentType": "card"},
    {"FirstName": "Kostas",    "LastName": "Arvanitis",      "Email": "kostas.arvanitis@example.com",            "ContractType": "Silver",  "PaymentType": "cash"},
    {"FirstName": "Despina",   "LastName": "Filippou",       "Email": "despina.filippou@example.com",            "ContractType": "Metal",   "PaymentType": "card"},
    {"FirstName": "Nikiforos", "LastName": "Xanthopoulos",   "Email": "nikiforos.xanthopoulos@example.com",       "ContractType": "Diamond", "PaymentType": "cash"},
    {"FirstName": "Vicky",     "LastName": "Papathanasiou",  "Email": "vicky.papathanasiou@example.com",          "ContractType": "Gold",    "PaymentType": "card"},
    {"FirstName": "Yiannis",   "LastName": "Kotzias",        "Email": "yiannis.kotzias@example.com",             "ContractType": "Silver",  "PaymentType": "cash"},
    {"FirstName": "Kalliopi",  "LastName": "Varoufaki",      "Email": "kalliopi.varoufaki@example.com",           "ContractType": "Metal",   "PaymentType": "card"},
    {"FirstName": "Dimitra",   "LastName": "Sideri",         "Email": "dimitra.sideri@example.com",               "ContractType": "Diamond", "PaymentType": "cash"},
    {"FirstName": "Kostis",    "LastName": "Galanis",        "Email": "kostis.galanis@example.com",                "ContractType": "Gold",    "PaymentType": "card"},
    {"FirstName": "Eleni2",    "LastName": "Douka",          "Email": "eleni.douka@example.com",                  "ContractType": "Silver",  "PaymentType": "cash"},
    {"FirstName": "Manolis",   "LastName": "Petrou",         "Email": "manolis.petrou@example.com",                "ContractType": "Metal",   "PaymentType": "card"},
    {"FirstName": "Athina",    "LastName": "Karadima",       "Email": "athina.karadima@example.com",                "ContractType": "Diamond", "PaymentType": "cash"},
    {"FirstName": "Christina", "LastName": "Laskaridou",     "Email": "christina.laskaridou@example.com",         "ContractType": "Gold",    "PaymentType": "card"},
    {"FirstName": "Panos",     "LastName": "Kotsialos",      "Email": "panos.kotsialos@example.com",                "ContractType": "Silver",  "PaymentType": "cash"},
    {"FirstName": "Maria2",    "LastName": "Vlachou",        "Email": "maria.vlachou@example.com",                   "ContractType": "Metal",   "PaymentType": "card"},
    {"FirstName": "Stavros",   "LastName": "Mavroudis",      "Email": "stavros.mavroudis@example.com",               "ContractType": "Diamond", "PaymentType": "cash"},
    {"FirstName": "Irene",     "LastName": "Theodorou",      "Email": "irene.theodorou@example.com",                 "ContractType": "Gold",    "PaymentType": "card"},
    {"FirstName": "Christos",  "LastName": "Panagiotou",     "Email": "christos.panagiotou@example.com",              "ContractType": "Silver",  "PaymentType": "cash"},
    {"FirstName": "Mary",      "LastName": "Karatzas",       "Email": "mary.karatzas@example.com",                    "ContractType": "Metal",   "PaymentType": "card"},
    {"FirstName": "George",    "LastName": "Kakouras",       "Email": "george.kakouras@example.com",                   "ContractType": "Diamond", "PaymentType": "cash"},
    {"FirstName": "Sofia2",    "LastName": "Katsaros",       "Email": "sofia.katsaros@example.com",                     "ContractType": "Gold",    "PaymentType": "card"},
    {"FirstName": "Nikos2",    "LastName": "Angelopoulos",  "Email": "nikos.angelopoulos@example.com",                 "ContractType": "Silver",  "PaymentType": "cash"},
    {"FirstName": "Melina",    "LastName": "Papagiannakis",  "Email": "melina.papagiannakis@example.com",               "ContractType": "Metal",   "PaymentType": "card"},
    {"FirstName": "Andreas2",  "LastName": "Tsiolis",        "Email": "andreas.tsiolis@example.com",                    "ContractType": "Diamond", "PaymentType": "cash"},
    {"FirstName": "Eleni3",    "LastName": "Lazarou",        "Email": "eleni.lazarou@example.com",                      "ContractType": "Gold",    "PaymentType": "card"},
    {"FirstName": "Antonis",   "LastName": "Giannakopoulos","Email":"antonis.giannakopoulos@example.com","ContractType":"Silver","PaymentType":"cash"},
    {"FirstName": "Helena",    "LastName": "Spiliotopoulou","Email":"helena.spiliotopoulou@example.com","ContractType":"Metal","PaymentType":"card"},
    {"FirstName": "Panagiota", "LastName": "Mylonaki",       "Email": "panagiota.mylonaki@example.com",                 "ContractType": "Diamond", "PaymentType": "cash"}
]

# Normalize for lookup
for c in _CLIENTS:
    c["FirstName_norm"] = c["FirstName"].strip().lower()
    c["LastName_norm"]  = c["LastName"].strip().lower()

@tool(
    name="lookup_client_contract",
    description="Given a client's first name and optionally last name, returns contract type & payment type."
)
def lookup_client_contract(
    first_name: str,
    last_name: Optional[str] = None
) -> str:
    fn = first_name.strip().lower()
    ln = last_name.strip().lower() if last_name else None

    # find matches
    matches = [c for c in _CLIENTS if c["FirstName_norm"] == fn and (ln is None or c["LastName_norm"] == ln)]

    if not matches:
        return f"No client found with name “{first_name} {last_name or ''}”."
    if len(matches) > 1:
        return f"Multiple clients found with the name “{first_name} {last_name or ''}” — please specify more details."

    client = matches[0]
    return (f"Client {client['FirstName']} {client['LastName']} (email: {client['Email']}) "
            f"has a {client['ContractType']} contract and pays by {client['PaymentType']}.")