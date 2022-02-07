import os
import requests


def main():
    api_key = os.environ["PROPUBLICA_API_KEY"]
    members = get_members_data(api_key)
    print("Senators most likely to break ranks:\n")
    sorted_members = sort_by_votes(members)
    statements(sorted_members)

def get_members_data(api_key):
    url = "https://api.propublica.org/congress/v1/117/senate/members.json"
    headers = {"X-API-Key": api_key}
    response = requests.get(url, headers=headers)
    full_dict = response.json()
    results = full_dict["results"]
    data = results[0]["members"]
    return data

def sort_by_votes(members):
    against_party_score = sorted(
        members, key=lambda members: (members["party"], members["votes_against_party_pct"]), reverse=True
    )[:10]
    return against_party_score

def statements(sorted_members):
    first_name = sorted_members["first_name"]
    last_name = sorted_members["last_name"]
    state = sorted_members["state"]
    vote_against = sorted_members["votes_against_party_pct"]
    for sorted_member in sorted_members:
        if sorted_member['party'] == "D":
            print("Democrat\n--------")
            print(
            f"* {first_name} {last_name} ({state}) votes against the party {vote_against}% of the time"
        )
        elif sorted_member['party'] == "R":
            print("\nRepublican\n--------")
            print(
            f"* {first_name} {last_name} ({state}) votes against the party {vote_against}% of the time"
        )


def senators_split_sort(members):
    dems = []
    repubs = []
    for member in members:
        if member["party"] == "D":
            dems.append(member)
        elif member["party"] == "R":
            repubs.append(member)
    dems_sorted = sorted(
        dems, key=lambda dems: dems["votes_against_party_pct"], reverse=True
    )[:5]
    repubs_sorted = sorted(
        repubs, key=lambda repubs: repubs["votes_against_party_pct"], reverse=True
    )[:5]
    print("Democrat\n--------")
    for dem in dems_sorted:
        dem_first_name = dem["first_name"]
        dem_last_name = dem["last_name"]
        dem_state = dem["state"]
        dem_vote_against = dem["votes_against_party_pct"]
        print(
            f"* {dem_first_name} {dem_last_name} ({dem_state}) votes against the party {dem_vote_against}% of the time"
        )
    print("\nRepublican\n--------")
    for repub in repubs_sorted:
        repub_first_name = repub["first_name"]
        repub_last_name = repub["last_name"]
        repub_state = repub["state"]
        repub_vote_against = repub["votes_against_party_pct"]
        print(
            f"* {repub_first_name} {repub_last_name} ({repub_state}) votes against the party {repub_vote_against}% of the time"
        )


main()
