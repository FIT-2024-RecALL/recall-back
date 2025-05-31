# API Reference

This document provides a complete reference for all REST API endpoints in the RecALL backend application. The API is built using FastAPI and provides endpoints for user management, flashcard operations, collections, file storage, and training functionality.

For detailed endpoint documentation, see the individual API sections: User API [5.1](https://deepwiki.com/FIT-2024-RecALL/recall-back/5.1-user-api-endpoints), Cards API [5.2](https://deepwiki.com/FIT-2024-RecALL/recall-back/5.2-cards-api), Collections API [5.3](https://deepwiki.com/FIT-2024-RecALL/recall-back/5.3-collections-api), Storage API [5.4](https://deepwiki.com/FIT-2024-RecALL/recall-back/5.4-storage-api), and Training API [5.5](https://deepwiki.com/FIT-2024-RecALL/recall-back/5.5-training-api). For information about the service layer implementation, see [Application Architecture](https://deepwiki.com/FIT-2024-RecALL/recall-back/3-application-architecture).

## API Architecture Overview

The API is organized into modular routers, each handling a specific domain of functionality. All routers use dependency injection for service access and authentication.

```
Business ServicesDependenciesAPI RoutersFastAPI ApplicationFastAPI AppMain ApplicationUser Router/userCards Router/cardsCollections Router/collectionsStorage Router/storageTrain Records Router/train_recordsUserIdDepRequired AuthUserIdSoftDepOptional AuthService DependenciesCardServiceDep, CollectionServiceDepStorageServiceDep, TrainRecordServiceDepUserServiceCardServiceCollectionServiceStorageServiceTrainRecordService
```

Sources: [app/api/dependencies.py1-25](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/api/dependencies.py#L1-L25) [app/api/cards.py8-11](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/api/cards.py#L8-L11) [app/api/collections.py8-11](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/api/collections.py#L8-L11) [app/api/storage.py10-13](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/api/storage.py#L10-L13)

The API uses a two-tier authentication system with required and optional authentication dependencies.

```
YesOptionalValidInvalidValidInvalid/MissingHTTP RequestAuthenticationRequired?UserIdDepget_profile_idUserIdSoftDepget_profile_id_softValidate JWT TokenSoft ValidateJWT Token401 Unauthorizeduser_id: NoneService Method CallBusiness LogicAuthorization ChecksAPI ResponseError Response
```

Sources: [app/api/dependencies.py16-17](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/api/dependencies.py#L16-L17)

## Common Request Patterns

### Dependency Injection Pattern

All API endpoints follow a consistent dependency injection pattern for services and authentication:

| Dependency | Type | Purpose | Usage |
| --- | --- | --- | --- |
| `UserIdDep` | `int` | Required authentication | Creates, updates, deletes |
| `UserIdSoftDep` | `int | None` | Optional authentication | Public reads with ownership context |
| `CardServiceDep` | `CardService` | Card business logic | Card-related operations |
| `CollectionServiceDep` | `CollectionService` | Collection business logic | Collection-related operations |
| `StorageServiceDep` | `StorageService` | File storage operations | File upload/download |
| `TrainRecordServiceDep` | `TrainRecordService` | Training progress | Learning analytics |

Sources: [app/api/dependencies.py8-24](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/api/dependencies.py#L8-L24)

### Request Body Patterns

#### Bulk Operations

For operations involving multiple IDs, the API uses `IntListBody` constraint:

```
IntListBody = Annotated[list[int], Body(min_length=1, max_length=100)]
```

This pattern is used in endpoints like card creation with collection assignments.

Sources: [app/api/dependencies.py24](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/api/dependencies.py#L24-L24) [app/api/cards.py33](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/api/cards.py#L33-L33)

## API Response Formats

### Standard Data Models

All API responses use Pydantic models for consistent data serialization:

| Model | Usage | Key Fields |
| --- | --- | --- |
| `Card` | Card data responses | `id`, `front_side`, `back_side`, `is_public`, `owner_id` |
| `Collection` | Collection data responses | `id`, `title`, `description`, `is_public`, `owner_id` |
| `CollectionShort` | Collection list responses | Excludes `description` field |
| `FileMeta` | File metadata responses | `id`, `filename`, `type`, `ext`, `is_public` |

### Special Response Types

#### File Downloads

File download endpoints return `StreamingResponse` with appropriate headers:

```
StreamingResponse(
    file.stream,
    media_type="application/octet-stream", 
    headers={
        "Content-Disposition": f"attachment; filename={quote(file.metadata.filename)}",
        "Content-Type": f"{file.metadata.type}/{file.metadata.ext}"
    }
)
```

Sources: [app/api/storage.py46-53](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/api/storage.py#L46-L53)

#### Deletion Operations

Delete operations return `Response` class with status code 204 (No Content).

Sources: [app/api/storage.py56-61](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/api/storage.py#L56-L61) [app/api/collections.py68-72](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/api/collections.py#L68-L72) [app/api/cards.py46-50](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/api/cards.py#L46-L50)

## Error Handling

The API follows FastAPI's standard error handling with HTTP status codes:

-   `401 Unauthorized` - Invalid or missing authentication
-   `403 Forbidden` - User lacks permission for the resource
-   `404 Not Found` - Resource does not exist
-   `422 Unprocessable Entity` - Invalid request data
-   `500 Internal Server Error` - Server-side errors

Authorization is handled at the service layer, allowing for consistent business logic across all endpoints.

## Endpoint Categories

### Core Resource Operations

| Router | Prefix | Primary Resources | Authentication |
| --- | --- | --- | --- |
| Cards | `/cards` | Flashcards, card-collection associations | Required for CUD, optional for reads |
| Collections | `/collections` | Collections, card organization | Required for CUD, optional for reads |
| Storage | `/storage` | File upload/download, metadata | Required for uploads/deletes, optional for downloads |
| User | `/user` | Registration, login, profiles | Mixed requirements |
| Train Records | `/train_records` | Learning progress, training sessions | Required |

### Cross-Resource Relationships

The API supports complex relationships between resources:

-   Cards can belong to multiple collections
-   Cards can have multiple file attachments
-   Collections have training modes for spaced repetition
-   Files inherit visibility from associated cards
-   Training records track progress across cards

Sources: [app/api/cards.py19-29](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/api/cards.py#L19-L29) [app/api/collections.py30-42](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/api/collections.py#L30-L42) [app/api/storage.py32-37](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/api/storage.py#L32-L37)

For complete endpoint documentation including request/response schemas, authentication requirements, and usage examples, refer to the individual API sections [5.1](https://deepwiki.com/FIT-2024-RecALL/recall-back/5.1-user-api-endpoints) through [5.5](https://deepwiki.com/FIT-2024-RecALL/recall-back/5.5-training-api).