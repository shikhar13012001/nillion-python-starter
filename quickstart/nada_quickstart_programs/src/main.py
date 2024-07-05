from nada_dsl import *

def initialize_parties(nr_voters):
    return [Party(name=f"Voter{i}") for i in range(nr_voters)]

def inputs_initialization(nr_voters, nr_candidates, voters):
    votes = []
    for c in range(nr_candidates):
        candidate_votes = []
        for v in range(nr_voters):
            vote_input = SecretUnsignedInteger(Input(name=f"v{v}_c{c}", party=voters[v]))
            role_input = SecretUnsignedInteger(Input(name=f"role{v}_c{c}", party=voters[v]))
            candidate_votes.append(vote_input * role_input)
        votes.append(candidate_votes)
    return votes

def eligibility_check(voters):
    return [SecretUnsignedInteger(Input(name=f"eligibility{v}", party=voters[v]))
            for v in range(len(voters))]

def apply_multiplier(votes, multiplier):
    return [vote * multiplier for vote in votes]

def advanced_computation(votes, eligibility, multiplier):
    total = UnsignedInteger(0)
    for vote, eligible in zip(votes, eligibility):
        total += vote * eligible * multiplier
    return total

def weighted_vote_count(nr_voters, nr_candidates, weighted_votes, eligibility_results, outparty):
    results = []
    multiplier = UnsignedInteger(2)  # Example multiplier
    for c in range(nr_candidates):
        # Apply advanced computation with a multiplier
        total = advanced_computation(weighted_votes[c], eligibility_results, multiplier)
        results.append(Output(total, name=f"final_vote_count_c{c}", party=outparty))
    return results

def nada_main():
    nr_voters = 5
    nr_candidates = 3
    outparty = Party(name="OutParty")

    voters = initialize_parties(nr_voters)
    votes_per_candidate = inputs_initialization(nr_voters, nr_candidates, voters)
    eligibility_results = eligibility_check(voters)
    results = weighted_vote_count(nr_voters, nr_candidates, votes_per_candidate, eligibility_results, outparty)

    return results