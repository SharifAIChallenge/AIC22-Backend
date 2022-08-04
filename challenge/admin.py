from django.contrib import admin
from django.contrib.admin import ModelAdmin

#from import_export.admin import ImportExportModelAdmin

from challenge.models.match import Match
from challenge.models.league import League
from challenge.models.match_info import MatchInfo
from challenge.models.tournament import Tournament
from challenge.models.level_based_tournament import LevelBasedTournament
from challenge.models.map import Map
from .models import Submission

from .resources import MatchResource


@admin.register(League)
class LeagueAdmin(ModelAdmin):
    list_display = (
        'id', 'tournament_name', 'start_time', 'match_map', 'total_matches',
        'run')

    list_display_links = ('id',)


@admin.register(Match)
class MatchAdmin(ModelAdmin):
    list_display = ('id', 'team1', 'team2', 'status', 'winner', 'tournament',
                    'infra_token')
    list_display_links = ('id',)
    list_filter = ('tournament', 'status')
    search_fields = ('infra_token',)
    resource_class = MatchResource


@admin.register(MatchInfo)
class MatchInfoAdmin(ModelAdmin):
    pass


@admin.register(Tournament)
class TournamentAdmin(ModelAdmin):
    list_display = ('id', 'name', 'type', 'is_hidden', 'start_time',
                    'end_time')
    list_filter = ('type', 'is_hidden')
    search_fields = ('name',)
    list_editable = ('type', 'is_hidden', 'start_time', 'end_time')


@admin.register(LevelBasedTournament)
class LevelBasedTournamentAdmin(ModelAdmin):
    pass


@admin.register(Map)
class MapAdmin(ModelAdmin):
    list_display = ('id', 'name', 'file', 'active', 'infra_token')
    list_display_links = ('id', 'name')
    list_editable = ('file', 'active')
    list_filter = ('active',)
    search_fields = ('name', 'infra_token')


@admin.register(Submission)
class SubmissionAdmin(ModelAdmin):
    list_display = ('id', 'team', 'user', 'file', 'submit_time', 'is_final',
                    'status', 'infra_token', 'is_mini_game',
                    'is_mini_game_final')
    list_display_links = ('id',)

    list_filter = ('is_final', 'status', 'submit_time', 'is_mini_game',
                   'is_mini_game_final')
    search_fields = ('infra_token',)
