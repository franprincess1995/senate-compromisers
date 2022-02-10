import os
import requests


def main():
    api_key = os.environ["PROPUBLICA_API_KEY"]
    members = get_members_data(api_key)
    print("Senators most likely to break ranks:\n")
    dems, repubs = group_members_by_party(members)
    sorted_dems = sort_by_votes(dems)
    sorted_repubs = sort_by_votes(repubs)
    print_top_politicians(sorted_dems, "Democrat")
    print_top_politicians(sorted_repubs, "Republican")


def get_members_data(api_key):
    url = "https://api.propublica.org/congress/v1/117/senate/members.json"
    headers = {"X-API-Key": api_key}
    response = requests.get(url, headers=headers)
    full_dict = response.json()
    results = full_dict["results"]
    return results[0]["members"]


def group_members_by_party(members):
    members_by_party = {"D": [], "R": [], "ID": []}
    for member in members:
        party = member["party"]
        members_by_party[party].append(member)
    return members_by_party["D"], members_by_party["R"]


def sort_by_votes(grouped_members):
    return sorted(
        grouped_members,
        key=lambda grouped_member: grouped_member["votes_against_party_pct"],
        reverse=True,
    )[:5]


def print_top_politicians(sorted_politicians, party_name):
    hyphen_string = "-" * 8
    print(f"{party_name}\n{hyphen_string}")
    for politician in sorted_politicians:
        first_name = politician["first_name"]
        last_name = politician["last_name"]
        state = politician["state"]
        vote_against = politician["votes_against_party_pct"]
        print(
            f"* {first_name} {last_name} ({state}) votes against the party {vote_against}% of the time"
        )


main()
