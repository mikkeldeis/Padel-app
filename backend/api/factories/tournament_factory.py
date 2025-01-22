from ..models import Tournament, BracketTournament, AmericanoTournament, LeagueTournament

class TournamentFactory:
    @staticmethod
    def create_tournament(tournament_type, **kwargs):
        if tournament_type == 'BRACKET':
            return BracketTournament.objects.create(**kwargs)
        elif tournament_type == 'AMERICANO':
            return AmericanoTournament.objects.create(**kwargs)
        elif tournament_type == 'LEAGUE':
            return LeagueTournament.objects.create(**kwargs)
        else:
            raise ValueError(f"Unknown tournament type: {tournament_type}")