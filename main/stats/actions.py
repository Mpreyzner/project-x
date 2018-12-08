from events.actions import ImmediateAction
from .stats_calculator import StatsCalculator


class RecalculateStatsAction(ImmediateAction):
    def run(self, post):
        calculator = StatsCalculator()
        calculator.recalculate(post)
