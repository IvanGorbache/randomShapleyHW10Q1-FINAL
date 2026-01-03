import itertools, random, math


def subset_sum_dict(players):
    result = {}

    keys = list(players.keys())
    n = len(keys)

    for r in range(n + 1):
        for subset in itertools.combinations(keys, r):
            subset_key = frozenset(subset)
            subset_sum = sum(players[player] for player in subset)
            result[subset_key] = subset_sum

    return result

def exact_shapley(players, cost_fn):
    n = len(players)
    shap = dict.fromkeys(players, 0.0)
    perms = itertools.permutations(players)
    for perm in perms:
        prefix = []
        for p in perm:
            before = frozenset(prefix)
            after = frozenset(prefix + [p])
            marginal = cost_fn(after) - cost_fn(before)
            shap[p] += marginal
            prefix.append(p)
    # average over all permutations
    m = math.factorial(n)
    for p in shap:
        shap[p] /= m
    return shap


def random_shapley(players, cost_fn, m):
    shap = dict.fromkeys(players, 0.0)
    permutations = list(itertools.permutations(players))
    for i in range(m):
        prefix = []
        rng = random.randint(0, len(permutations)-1)
        perm = permutations[rng]

        for p in perm:
            before = frozenset(prefix)
            after = frozenset(prefix + [p])
            marginal = cost_fn(after) - cost_fn(before)
            shap[p] += marginal
            prefix.append(p)
    # average over all permutations
    for p in shap:
        shap[p] /= len(permutations)
    return shap


def random_airport_instance(n, seed=0, max_cost=100):
    random.seed(seed)
    # generate costs for each part of the runway
    runway_costs = [random.randint(1, max_cost) for _ in range(n)]
    players_costs = {}
    for i in range(n):
        player_name = chr(ord('A') + i)
        cost = 0
        for j in range(i + 1):  # player i uses parts 0..i
            users = n - j  # number of players using this part
            cost += runway_costs[j] / users
        players_costs[player_name] = cost

    return players_costs

players_costs = {'A': 30, 'B': 40, 'C': 50}
players = list(players_costs.keys())
costs = subset_sum_dict(players_costs)

def c(S):
    return costs.get(frozenset(S), float('inf'))

def main():

    # --- Fixed example ---
    print("=== Fixed example ===")
    fixed_players_costs = {'A': 30, 'B': 40, 'C': 50}
    fixed_players = list(fixed_players_costs.keys())
    fixed_costs = subset_sum_dict(fixed_players_costs)

    def fixed_c(S):
        return fixed_costs.get(frozenset(S), float('inf'))

    # Exact Shapley
    exact = exact_shapley(fixed_players, fixed_c)
    print("\nExact Shapley values:")
    for p in fixed_players:
        print(f"  {p}: {exact[p]}")

    # Random Shapley
    for m in range(1, math.factorial(len(fixed_players)) + 1):
        est = random_shapley(fixed_players, fixed_c, m)
        print(f"\nm={m}: estimates:", ', '.join(f"{p}:{est[p]}" for p in fixed_players))

    # --- Random Airport Instances ---
    for n in [3, 4, 5]:
        print(f"\n=== Random Airport Instance with {n} players ===")
        airport_players_costs = random_airport_instance(n, seed=42)
        print("Players' costs:", airport_players_costs)
        airport_players = list(airport_players_costs.keys())
        airport_costs = subset_sum_dict(airport_players_costs)

        def airport_c(S):
            return airport_costs.get(frozenset(S), float('inf'))

        # Exact Shapley
        exact = exact_shapley(airport_players, airport_c)
        print("Exact Shapley values:")
        for p in airport_players:
            print(f"  {p}: {exact[p]}")

        for i in range(1, math.factorial(n)+1):
            est = random_shapley(airport_players, airport_c, i)
            print(f"Random Shapley estimates (m={i}):")
            for p in airport_players:
                print(f"  {p}: {est[p]}")


if __name__ == "__main__":
    main()
