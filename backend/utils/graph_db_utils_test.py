from unittest.mock import ANY, MagicMock
from neo4j import Driver, Session
import pytest
# We assign an alias to "test_connection" to avoid pytest treating it as another test function
from utils.graph_db_utils import test_connection as verify_connection, create_goal

def test_database_connectivity_is_healthy(mocker):
    mock_driver = mocker.patch("utils.graph_db_utils.driver", return_value=MagicMock(spec=Driver))
    mock_driver.verify_connectivity.return_value = None

    connected = verify_connection()

    assert connected
    mock_driver.verify_connectivity.assert_called_once()
    mock_driver.close.assert_called_once()


def test_database_connectivity_is_unhealthy(mocker):
    mock_driver = mocker.patch("utils.graph_db_utils.driver", return_value=MagicMock(spec=Driver))
    mock_driver.verify_connectivity.side_effect = Exception

    connected = verify_connection()

    assert not connected
    mock_driver.verify_connectivity.assert_called_once()
    mock_driver.close.assert_called_once()


def test_create_goal_is_successful(mocker):
    mock_driver = mocker.patch("utils.graph_db_utils.driver", return_value=MagicMock(spec=Driver))
    mock_session = MagicMock(spec=Session)
    mock_driver.session.return_value = mock_session

    response = create_goal("Test Name", "Test Description")

    assert response is None
    mock_session.run.assert_called_once_with(ANY, name="Test Name", description="Test Description")
    mock_session.close.assert_called_once()
    mock_driver.close.assert_called_once()


def test_create_goal_throws_exception(mocker):
    mock_driver = mocker.patch("utils.graph_db_utils.driver", return_value=MagicMock(spec=Driver))
    mock_session = MagicMock(spec=Session)
    mock_driver.session.return_value = mock_session
    mock_session.run.side_effect = Exception

    with pytest.raises(Exception):
        create_goal("Test Name", "Test Description")

    mock_session.run.assert_called_once_with(ANY, name="Test Name", description="Test Description")
    mock_session.close.assert_called_once()
    mock_driver.close.assert_called_once()
