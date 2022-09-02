from django.contrib import admin
from django.contrib.admin import ModelAdmin

# from import_export.admin import ImportExportModelAdmin
import csv

from challenge.models.match import Match, MatchStatusTypes
from challenge.models.league import League
from challenge.models.match_info import MatchInfo
from challenge.models.tournament import Tournament
from challenge.models.level_based_tournament import LevelBasedTournament
from challenge.models.level import Level
from challenge.models.level_match import LevelMatch
from challenge.models.map import Map
from django.http import HttpResponse
from .models import Submission
from .models.request import Request
from .models.scoreboard import Scoreboard, ScoreboardRow

from .resources import MatchResource


@admin.register(League)
class LeagueAdmin(ModelAdmin):
    list_display = (
        'id', 'tournament_name', 'start_time', 'match_map', 'total_matches',
        'run')

    list_display_links = ('id',)


class FailMatches:
    short_description = "Mark selected matches as failed"

    def __new__(cls, modeladmin, request, queryset):
        result = cls.make_matches_fail(modeladmin, request, queryset)
        return result

    @classmethod
    def make_matches_fail(cls, modeladmin, request, queryset):
        queryset.update(status=MatchStatusTypes.FAILED)


class RunMatches:
    short_description = "Run matches again!"

    def __new__(cls, modeladmin, request, queryset):
        result = cls.run_matches(modeladmin, request, queryset)
        return result

    @classmethod
    def run_matches(cls, modeladmin, request, queryset):
        for match in queryset.all():
            match.run_match(priority=0)


@admin.register(Match)
class MatchAdmin(ModelAdmin):
    list_display = ('id', 'team1', 'team2', 'status', 'winner', 'tournament',
                    'infra_token', 'created_at')
    list_display_links = ('id',)
    list_filter = ('tournament', 'status')
    search_fields = ('infra_token',)
    resource_class = MatchResource
    actions = [FailMatches, RunMatches]


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


@admin.register(Level)
class LevelAdmin(ModelAdmin):
    list_display = ('id', 'number', 'level_based_tournament')


@admin.register(LevelMatch)
class LevelMatchAdmin(ModelAdmin):
    list_display = ('id', 'match', 'level')


@admin.register(Scoreboard)
class ScoreboardAdmin(ModelAdmin):
    pass


@admin.register(ScoreboardRow)
class ScoreboardRowAdmin(ModelAdmin):
    pass


@admin.register(Map)
class MapAdmin(ModelAdmin):
    list_display = ('id', 'name', 'file', 'active', 'infra_token')
    list_display_links = ('id', 'name')
    list_editable = ('file', 'active')
    list_filter = ('active',)
    search_fields = ('name', 'infra_token')


@admin.register(Request)
class RequestAdmin(ModelAdmin):
    pass


@admin.register(Submission)
class SubmissionAdmin(ModelAdmin):
    actions = ["export_as_csv"]

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"

    list_display = ('id', 'team', 'user', 'file', 'submit_time', 'is_final',
                    'status', 'infra_token', 'is_mini_game',
                    'is_mini_game_final')
    list_display_links = ('id',)

    list_filter = ('is_final', 'status', 'submit_time', 'is_mini_game',
                   'is_mini_game_final')
    search_fields = ('infra_token',)
