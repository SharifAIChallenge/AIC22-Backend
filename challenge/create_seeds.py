from django.utils import timezone
import random
from .models.tournament import Tournament


def create_seeds(seeds_size, seeds_count, tournament_id):
    rows = Tournament.objects.get(id=tournament_id).scoreboard.rows.order_by(
        '-score')
    final_teams = []
    for row in rows:
        if row.team.final_submission() and row.team.is_finalist:
            final_teams.append(row.team)

    if len(final_teams) != seeds_size * seeds_count:
        raise ValueError('seed_size * seeds_count != len(final_teams)')

    seeds = [final_teams[i: i + seeds_count] for i in
             range(0, seeds_size * seeds_count, seeds_count)]

    groups = [[] for _ in range(seeds_count)]

    for seed in seeds:
        random.shuffle(seed)
        for i, team in enumerate(seed):
            groups[i].append(team)

    for i, group in enumerate(groups):
        Tournament.create_tournament(
            name='گروه {}'.format(i + 1),
            start_time=timezone.now(),
            end_time=None,
            is_hidden=True,
            team_list=group
        )
    return groups


def run_tournament_groups(start_group_tournament_id, end_group_tournament_id, map_id, two_way):
    from .models.map import Map
    map_obj = Map.objects.get(id=map_id)
    for i in range(start_group_tournament_id, end_group_tournament_id + 1):
        Tournament.objects.get(id=i).make_league_for_tournament(
            match_map=map_obj,
            two_way=two_way
        )
