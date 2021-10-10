from collections import defaultdict


# Compute number of players and suspects
def get_rooms_list(game_state: dict) -> dict:
    tmp = defaultdict(lambda: [0, 0])

    for ch in game_state['characters']:
        tmp[ch['position']][0] += 1
        if ch['suspect'] is True:
            tmp[ch['position']][1] += 1
    return tmp


# Get number of players per group
def get_groups_total(game_state):
    total = 0
    for room, nbs in get_rooms_list(game_state).items():
        if nbs[0] == 1 or room == game_state['shadow']:
            total -= nbs[1]
        else:
            total += nbs[1]
    return total


# Compute inspector score with a result value between 0 and 8
def inspector_gain(game_state):
    total = get_groups_total(game_state)
    return 8 - abs(total) if total < 0 else 8 - total + .1


# Trying to compute the fantom gain without knowing where the fantom is
def compute_fantom_gain(game_state):
    total = get_groups_total(game_state)
    return abs(total) + .1 if total < 0 else total


# Get the number of grouped and isolated people.
# Then, subtract the number including the fantom with the other one
def fantom_gain(game_state) -> int:
    if 'fantom' not in game_state:
        return compute_fantom_gain(game_state)
    fantom = next((item for item in game_state['characters'] if
                  item["color"] == game_state['fantom']), None)

    isolated = 0
    grouped = 0
    room_list = get_rooms_list(game_state)
    fantom_room = room_list[fantom['position']]
    is_fantom_isolated = fantom_room[0] == 1 or fantom['position'] == game_state[
        'shadow']

    for id, nbs in room_list.items():
        if nbs[0] == 1 or id == game_state['shadow']:
            isolated += nbs[1]
        else:
            grouped += nbs[1]

    if is_fantom_isolated is True:
        return (isolated - grouped) + 0.1
    else:
        return grouped - isolated
