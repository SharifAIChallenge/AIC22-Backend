from challenge.models.lobby import LobbyTypes, LobbyQueue
from challenge.models.match import Match


class LobbyService:
    @staticmethod
    def run_tournament_after_team_join(lobby_q):
        if lobby_q.get_lobby_population() < lobby_q.get_lobby_size():
            return

        if lobby_q.game_type == LobbyTypes.FRIENDLY_MATCH:
            LobbyService.run_friendly_tournament(lobby_q)
        elif lobby_q.game_type == LobbyTypes.LEVEL_BASED_TOURNAMENT:
            LobbyService.run_mini_tournament(lobby_q)
        else:
            raise Exception("WTF?!")

    @staticmethod
    def run_friendly_tournament(lobby_q):
        # records = LobbyQueue.objects.filter(game_type=LobbyTypes.FRIENDLY_MATCH)[:2]
        # Match.create_friendly_match(records[0].team, records[1].team)
        #
        # for record in records:
        #     record.delete() # TODO: complete method
        pass

    @staticmethod
    def run_mini_tournament(lobby_q):
        # records = LobbyQueue.objects.filter(game_type=LobbyTypes.LEVEL_BASED_TOURNAMENT)[:8]
        # team_list = [record.team for record in records]
        #
        # LevelBasedTournament.create_level_based_tournament(
        #     name='Lobby Mini Tournament',
        #     start_time=datetime.now,
        #     end_time=None,
        #     is_hidden=True,
        #     team_list=team_list
        # )
        #
        # for record in records:
        #     record.delete() # TODO: complete method
        pass
