import subprocess
import sys
import os


def test_app_import():
    """Test that the app can be imported without errors"""
    # Set required environment variables for testing
    env = os.environ.copy()
    env['SECRET_KEY'] = 'test_secret_key'
    env['ACCESS_TOKEN_KEY'] = 'test_access_token'
    env['POSTGRES_USER'] = 'test_user'
    env['POSTGRES_PASSWORD'] = 'test_password'
    env['POSTGRES_HOST'] = 'localhost'
    env['POSTGRES_HOST_PORT'] = '5432'
    env['POSTGRES_DB'] = 'test_db'
    env['MINIO_BUCKET_NAME'] = 'test_bucket'
    env['MINIO_HOSTNAME'] = 'localhost'
    env['MINIO_PORT'] = '9000'
    env['MINIO_LOGIN'] = 'test_minio_user'
    env['MINIO_PASSWORD'] = 'test_minio_password'
    env['MINIO_MAX_FILE_MB_SIZE'] = '10'
    env['OLLAMA_MODEL'] = 'test_model'
    env['OLLAMA_HOSTNAME'] = 'localhost'
    env['OLLAMA_PORT'] = '11434'
    
    # Try to import the main module
    result = subprocess.run([
        sys.executable, "-c", 
        "import sys; sys.path.insert(0, '.'); import app.main; print('Import successful')"
    ], capture_output=True, text=True, cwd=".", env=env)
    
    # Check that the import was successful
    assert result.returncode == 0, f"Import failed with error: {result.stderr}"
    assert "Import successful" in result.stdout


def test_app_initialization():
    """Test that the app can be initialized"""
    # Set required environment variables for testing
    env = os.environ.copy()
    env['SECRET_KEY'] = 'test_secret_key'
    env['ACCESS_TOKEN_KEY'] = 'test_access_token'
    env['POSTGRES_USER'] = 'test_user'
    env['POSTGRES_PASSWORD'] = 'test_password'
    env['POSTGRES_HOST'] = 'localhost'
    env['POSTGRES_HOST_PORT'] = '5432'
    env['POSTGRES_DB'] = 'test_db'
    env['MINIO_BUCKET_NAME'] = 'test_bucket'
    env['MINIO_HOSTNAME'] = 'localhost'
    env['MINIO_PORT'] = '9000'
    env['MINIO_LOGIN'] = 'test_minio_user'
    env['MINIO_PASSWORD'] = 'test_minio_password'
    env['MINIO_MAX_FILE_MB_SIZE'] = '10'
    env['OLLAMA_MODEL'] = 'test_model'
    env['OLLAMA_HOSTNAME'] = 'localhost'
    env['OLLAMA_PORT'] = '11434'
    
    # Try to create an instance of the FastAPI app
    result = subprocess.run([
        sys.executable, "-c", 
        "import sys; sys.path.insert(0, '.'); from app.main import app; print('App created successfully')"
    ], capture_output=True, text=True, cwd=".", env=env)
    
    # Check that the app was created successfully
    assert result.returncode == 0, f"App creation failed with error: {result.stderr}"
    assert "App created successfully" in result.stdout