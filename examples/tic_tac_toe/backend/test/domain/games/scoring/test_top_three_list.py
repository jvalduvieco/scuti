import unittest

from domain.games.scoring.top_three_list import TopThreeList
from domain.games.scoring.user_score import UserScore
from domain.games.types import UserId


class TopThreeListTestCase(unittest.TestCase):
    def test_scores_below_last_item_in_the_list_should_not_be_on_the_list(self):
        top = TopThreeList(top_three=[UserScore(id=UserId(), score=100),
                                      UserScore(id=UserId(), score=300),
                                      UserScore(id=UserId(), score=200)])
        self.assertFalse(top.should_be_on_the_list(50))

    def test_if_a_score_equals_last_score_on_the_list_new_score_should_not_be_on_list(self):
        top = TopThreeList(top_three=[UserScore(id=UserId(), score=100),
                                      UserScore(id=UserId(), score=300),
                                      UserScore(id=UserId(), score=200)])
        self.assertFalse(top.should_be_on_the_list(100))

    def test_if_a_score_is_greater_than_last_score_new_score_should_be_on_the_list(self):
        top = TopThreeList() \
            .include(player_id=UserId(), score=100) \
            .include(player_id=UserId(), score=300) \
            .include(player_id=UserId(), score=200)
        self.assertTrue(top.should_be_on_the_list(200))

    def test_has_always_three_items(self):
        last_user_id = UserId()
        top = TopThreeList() \
            .include(player_id=UserId(), score=100) \
            .include(player_id=UserId(), score=300) \
            .include(player_id=last_user_id, score=200) \
            .include(player_id=UserId(), score=200)

        self.assertEqual(3, len(top.top_three))
        self.assertEqual(UserScore(id=last_user_id, score=200), top.top_three[-1])

    def test_items_are_sorted_by_score_descending(self):
        top = TopThreeList() \
            .include(player_id=UserId(), score=120) \
            .include(player_id=UserId(), score=345) \
            .include(player_id=UserId(), score=223)

        self.assertEqual([345, 223, 120], list(map(lambda e: e.score, top.top_three)))
