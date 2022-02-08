import os
import requests


def main():
    api_key = os.environ["PROPUBLICA_API_KEY"]
    members = get_members_data(api_key)
    print("Senators most likely to break ranks:\n")
    sort_by_votes(members)
    top_dems_repubs_printed()


def get_members_data(api_key):
    url = "https://api.propublica.org/congress/v1/117/senate/members.json"
    headers = {"X-API-Key": api_key}
    response = requests.get(url, headers=headers)
    full_dict = response.json()
    results = full_dict["results"]
    data = results[0]["members"]
    return data


def sort_by_votes(members):
    sorted_members_party = {"dems": [], "repubs": []}
    for member in members:
        if member["party"] == "D":
            sorted_members_party["dems"].append(member)
            global against_party_dems
            against_party_dems = sorted(
                sorted_members_party["dems"],
                key=lambda sorted_members_party: sorted_members_party[
                    "votes_against_party_pct"
                ],
                reverse=True,
            )[:5]
        elif member["party"] == "R":
            sorted_members_party["repubs"].append(member)
            global against_party_repubs
            against_party_repubs = sorted(
                sorted_members_party["repubs"],
                key=lambda sorted_members_party: sorted_members_party[
                    "votes_against_party_pct"
                ],
                reverse=True,
            )[:5]
    return against_party_dems, against_party_repubs


def top_dems_repubs_printed():
    print("Democrat\n--------")
    for against_party_dem in against_party_dems:
        first_name = against_party_dem["first_name"]
        last_name = against_party_dem["last_name"]
        state = against_party_dem["state"]
        vote_against = against_party_dem["votes_against_party_pct"]
        print(
            f"* {first_name} {last_name} ({state}) votes against the party {vote_against}% of the time"
        )
    print("\nRepublican\n--------")
    for against_party_repub in against_party_repubs:
        first_name = against_party_repub["first_name"]
        last_name = against_party_repub["last_name"]
        state = against_party_repub["state"]
        vote_against = against_party_repub["votes_against_party_pct"]
        print(
            f"* {first_name} {last_name} ({state}) votes against the party {vote_against}% of the time"
        )


main()
