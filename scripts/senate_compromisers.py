import os
import requests


def main():
    api_key = os.environ["PROPUBLICA_API_KEY"]
    members = get_members_data(api_key)
    print("Senators most likely to break ranks:\n")
    politicians_vote_against(members)


def get_members_data(api_key):
    url = "https://api.propublica.org/congress/v1/117/senate/members.json"
    headers = {"X-API-Key": api_key}
    response = requests.get(url, headers=headers)
    full_dict = response.json()
    results = full_dict["results"]
    data = results[0]["members"]
    return data


def politicians_vote_against(members):
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
            f"*{dem_first_name} {dem_last_name} ({dem_state}) votes against the party {dem_vote_against}% of the time\n"
        )
    print("Republican\n--------")
    for repub in repubs_sorted:
        repub_first_name = repub["first_name"]
        repub_last_name = repub["last_name"]
        repub_state = repub["state"]
        repub_vote_against = repub["votes_against_party_pct"]
        print(
            f"*{repub_first_name} {repub_last_name} ({repub_state}) votes against the party {repub_vote_against}% of the time"
        )


main()
