import pytest
from EasyForce.common.utils import questions
from EasyForce.data_mangement.data_structure.entities_classes import Team


def test_questions_team_define_returns_none():
    # Should not raise and should return None for unsupported action
    result = questions('Team', 'define')
    assert result is None


def test_get_column_values_nonexistent_column_returns_empty_list():
    values = Team.get_column_values('nonexistent_column')
    assert values == []
