from core.api.kanoon import AcceptanceHistoryItem


class AnalyzeRank:

    definite = 800
    logical = 200

    rank: int = None
    history: list[AcceptanceHistoryItem] = None

    def __init__(
            self,
            history: list[AcceptanceHistoryItem],
            rank: int
    ) -> None:
        self.history = history
        self.rank = rank
    
    
    def check(self) -> str:
        ranks = [i.rank for i in self.history]
        if ranks:
            last_rank = sorted(ranks, reverse=True)[0]
            for r in [
                self._definite,
                self._logical,
                self._low
            ]:
                c = r(last_rank)
                if c:
                    return c + f'({str(last_rank - self.rank)})'
        
        return 'نامشخص'

    def _definite(self, rank:int):
        if (rank - self.rank) > self.definite:
            return f' قطعی '
        
        return False

    def _low(self, rank:int):
        if (self.rank - rank) > self.logical:
            return f' کم '
        
        return False

    def _logical(self, rank:int):
        if (self.rank - rank) < self.logical and (rank - self.rank) < self.logical:
            return f' منطقی '
        
        return False
    