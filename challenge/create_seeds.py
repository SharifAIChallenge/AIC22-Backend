from django.utils import timezone

from .models.tournament import Tournament


def create_seeds(seeds_size, seeds_count, tournament_id):
    rows = Tournament.objects.get(id=tournament_id).scoreboard.rows.order_by(
        '-score')
    final_teams = []
    for row in rows:
        if row.team.final_submission():
            final_teams.append(row.team)

    if len(final_teams) != seeds_size * seeds_count:
        raise ValueError('seed_size * seeds_count != len(final_teams)')

    seeds = [final_teams[i: i + seeds_count] for i in
             range(0, seeds_size * seeds_count, seeds_count)]

    groups = [[] for _ in range(seeds_count)]

    for seed in seeds:
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
