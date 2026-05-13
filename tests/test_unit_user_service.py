import pytest
from unittest.mock import Mock, AsyncMock, patch
from fastapi import HTTPException
from contextlib import asynccontextmanager

from app.services.user import UserService
from app.schemas.user import User, UserCreate, UserBase, UserAuth


class TestUserService:
    """Unit tests for UserService"""
    
    @pytest.fixture
    def mock_uow(self):
        """Create a mock unit of work"""
        mock = Mock()
        
        # Create an async context manager for the begin method
        @asynccontextmanager
        async def mock_begin():
            yield mock
        
        mock.begin = mock_begin
        return mock
    
    @pytest.fixture
    def mock_user_repo(self):
        """Create a mock user repository"""
        return Mock()
    
    @pytest.fixture
    def mock_collection_repo(self):
        """Create a mock collection repository"""
        return Mock()
    
    @pytest.fixture
    def mock_card_repo(self):
        """Create a mock card repository"""
        return Mock()
    
    @pytest.fixture
    def mock_file_repo(self):
        """Create a mock file repository"""
        return Mock()
    
    @pytest.fixture
    def user_service(self, mock_uow):
        """Create a UserService instance with mocked unit of work"""
        return UserService(mock_uow)
    
    @pytest.mark.asyncio
    async def test_register_user_success(self, user_service, mock_uow, mock_user_repo):
        """Test successful user registration"""
        # Setup
        user_data = UserCreate(
            email="test@example.com",
            nickname="testuser",
            password="testpassword123"
        )
        
        mock_uow.get_repository.return_value = mock_user_repo
        mock_user_repo.find_users_by_creds = AsyncMock(return_value=[])  # No existing users
        mock_user_repo.create_one = AsyncMock(return_value=User(
            id=1,
            email="test@example.com",
            nickname="testuser"
        ))
        
        # Execute
        result = await user_service.register_user(user_data)
        
        # Assert
        assert result.id == 1
        assert result.email == "test@example.com"
        assert result.nickname == "testuser"
        mock_user_repo.find_users_by_creds.assert_called_once()
        mock_user_repo.create_one.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_register_user_duplicate_email(self, user_service, mock_uow, mock_user_repo):
        """Test user registration with duplicate email"""
        # Setup
        user_data = UserCreate(
            email="test@example.com",
            nickname="testuser",
            password="testpassword123"
        )
        
        mock_uow.get_repository.return_value = mock_user_repo
        mock_user_repo.find_users_by_creds = AsyncMock(return_value=[1])  # Existing user
        
        # Execute & Assert
        with pytest.raises(HTTPException) as exc_info:
            await user_service.register_user(user_data)
        
        assert exc_info.value.status_code == 400
        mock_user_repo.find_users_by_creds.assert_called_once()
        mock_user_repo.create_one.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_get_user_success(self, user_service, mock_uow, mock_user_repo):
        """Test successful user retrieval"""
        # Setup
        mock_uow.get_repository.return_value = mock_user_repo
        mock_user_repo.get_user_by_id = AsyncMock(return_value=User(
            id=1,
            email="test@example.com",
            nickname="testuser"
        ))
        
        # Execute
        result = await user_service.get_user(1)
        
        # Assert
        assert result.id == 1
        assert result.email == "test@example.com"
        assert result.nickname == "testuser"
        mock_user_repo.get_user_by_id.assert_called_once_with(1, User)
    
    @pytest.mark.asyncio
    async def test_get_user_not_found(self, user_service, mock_uow, mock_user_repo):
        """Test user retrieval when user doesn't exist"""
        # Setup
        mock_uow.get_repository.return_value = mock_user_repo
        mock_user_repo.get_user_by_id = AsyncMock(return_value=None)
        
        # Execute & Assert
        with pytest.raises(HTTPException) as exc_info:
            await user_service.get_user(999)
        
        assert exc_info.value.status_code == 400
        mock_user_repo.get_user_by_id.assert_called_once_with(999, User)
    
    @pytest.mark.asyncio
    async def test_update_profile_success(self, user_service, mock_uow, mock_user_repo):
        """Test successful user profile update"""
        # Setup
        user_data = UserBase(
            email="updated@example.com",
            nickname="updateduser"
        )
        
        mock_uow.get_repository.return_value = mock_user_repo
        mock_user_repo.find_users_by_creds = AsyncMock(return_value=[])  # No conflicts
        mock_user_repo.update_user_by_id = AsyncMock(return_value=User(
            id=1,
            email="updated@example.com",
            nickname="updateduser"
        ))
        
        # Execute
        result = await user_service.update_profile(1, user_data)
        
        # Assert
        assert result.id == 1
        assert result.email == "updated@example.com"
        assert result.nickname == "updateduser"
        mock_user_repo.find_users_by_creds.assert_called_once()
        mock_user_repo.update_user_by_id.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_update_profile_conflict(self, user_service, mock_uow, mock_user_repo):
        """Test user profile update with conflicting data"""
        # Setup
        user_data = UserBase(
            email="conflict@example.com",
            nickname="conflictuser"
        )
        
        mock_uow.get_repository.return_value = mock_user_repo
        mock_user_repo.find_users_by_creds = AsyncMock(return_value=[2])  # Another user has this data
        
        # Execute & Assert
        with pytest.raises(HTTPException) as exc_info:
            await user_service.update_profile(1, user_data)
        
        assert exc_info.value.status_code == 400
        mock_user_repo.find_users_by_creds.assert_called_once()
        mock_user_repo.update_user_by_id.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_delete_profile_success(self, user_service, mock_uow, mock_user_repo):
        """Test successful user profile deletion"""
        # Setup
        mock_uow.get_repository.return_value = mock_user_repo
        mock_user_repo.exists_user_with_id = AsyncMock(return_value=True)
        mock_user_repo.delete_user_by_id = AsyncMock(return_value=None)
        
        # Execute
        await user_service.delete_profile(1)
        
        # Assert
        mock_user_repo.exists_user_with_id.assert_called_once_with(1)
        mock_user_repo.delete_user_by_id.assert_called_once_with(1)
    
    @pytest.mark.asyncio
    async def test_delete_profile_not_found(self, user_service, mock_uow, mock_user_repo):
        """Test user profile deletion when user doesn't exist"""
        # Setup
        mock_uow.get_repository.return_value = mock_user_repo
        mock_user_repo.exists_user_with_id = AsyncMock(return_value=False)
        
        # Execute & Assert
        with pytest.raises(HTTPException) as exc_info:
            await user_service.delete_profile(999)
        
        assert exc_info.value.status_code == 400
        mock_user_repo.exists_user_with_id.assert_called_once_with(999)
        mock_user_repo.delete_user_by_id.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_authenticate_user_success(self, user_service, mock_uow, mock_user_repo):
        """Test successful user authentication"""
        # Setup
        auth_data = UserAuth(
            email="test@example.com",
            password="testpassword123"
        )
        
        mock_uow.get_repository.return_value = mock_user_repo
        mock_user_repo.get_user_by_columns = AsyncMock(return_value=Mock(
            email="test@example.com",
            password="$2b$12$hashedpassword",  # Mocked hashed password
            model_dump=Mock(return_value={
                "email": "test@example.com",
                "nickname": "testuser",
                "password": "$2b$12$hashedpassword",
                "id": 1
            })
        ))
        
        # Mock password verification
        with patch('app.services.user.verify_password', return_value=True):
            # Execute
            result = await user_service.authenticate_user(auth_data)
            
            # Assert
            assert isinstance(result, User)
            assert result.email == "test@example.com"
            mock_user_repo.get_user_by_columns.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_authenticate_user_invalid_credentials(self, user_service, mock_uow, mock_user_repo):
        """Test user authentication with invalid credentials"""
        # Setup
        auth_data = UserAuth(
            email="test@example.com",
            password="wrongpassword"
        )
        
        mock_uow.get_repository.return_value = mock_user_repo
        mock_user_repo.get_user_by_columns = AsyncMock(return_value=None)
        
        # Execute & Assert
        with pytest.raises(HTTPException) as exc_info:
            await user_service.authenticate_user(auth_data)
        
        assert exc_info.value.status_code == 400
        mock_user_repo.get_user_by_columns.assert_called_once()