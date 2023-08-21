from core.api.kanoon import AcceptanceHistoryItem


class AnalyzeRank:

    definite = 800
    logical = 200
    low = 800

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
            av_ranks = int(sum(ranks) / len(ranks))
            for r in [
                self._definite,
                self._logical,
                self._low
            ]:
                c = r(av_ranks)
                if c:
                    return c
        
        return 'نامشخص'

    def _definite(self, rank:int):
        if (self.rank + self.definite) < rank:
            return f' قطعی ({str(rank - self.rank)}) '
        
        return False

    def _low(self, rank:int):
        if (self.rank - self.low) > rank:
            return f' کم ({str(rank - self.rank)}) '
        
        return False

    def _logical(self, rank:int):
        if (self.rank - self.low) < rank or (self.rank + self.logical) < rank:
            return f' منطقی ({str(rank - self.rank)}) '
        
        return False