# Application Architecture

This document explains the overall code organization, layered architecture patterns, and key design decisions used in the recall-back FastAPI application. It covers the structural foundation that supports the flashcard learning platform, including dependency injection, transaction management, and separation of concerns across different architectural layers.

For details about specific API endpoints, see [API Reference](https://deepwiki.com/FIT-2024-RecALL/recall-back/5-api-reference). For information about deployment infrastructure, see [Deployment and Infrastructure](https://deepwiki.com/FIT-2024-RecALL/recall-back/2-deployment-and-infrastructure).

## Architecture Overview

The recall-back application follows a clean layered architecture pattern with clear separation between API handling, business logic, and data access. The architecture is built around FastAPI and uses modern Python patterns including dependency injection, repository pattern, and unit of work for transaction management.

### High-Level Architecture Diagram

```
Data LayerRepository LayerService LayerAPI LayerFastAPI ApplicationAPI Routersusers, cards, collections,storage, train_recordsAPI DependenciesUserIdDep, ServiceDepsBaseServiceUserServiceCardServiceCollectionServiceStorageServiceTrainRecordServiceBaseSQLAlchemyRepositoryUserRepositoryCardRepositoryCollectionRepositoryFileRepositoryTrainRecordRepositoryUnitOfWorkDatabase TablesUserTable, CardTable, etc.
```

**Sources:** [app/main.py1-34](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/main.py#L1-L34) [app/repositories/base.py15-91](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/repositories/base.py#L15-L91) [app/services/base.py16-19](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/services/base.py#L16-L19) [app/db/unit\_of\_work.py17-48](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/db/unit_of_work.py#L17-L48)

## Application Initialization and Lifecycle

The FastAPI application uses a lifespan context manager to handle startup and shutdown operations. This includes database table creation, external service validation, and AI model management.

### Application Startup Flow

```
NoYesApplication Startlifespan() context managercreate_db_tables()is_bucket_available()Bucket Available?RuntimeError:Minio server's bucket isn't availableload_model()Router registration loopApplication ReadyApplication Shutdownunload_model()close_db_connections()Application End
```

The application initialization occurs in [app/main.py11-19](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/main.py#L11-L19) within the `lifespan` async context manager. The startup sequence ensures all required external dependencies are available before the application becomes ready to serve requests.

**Sources:** [app/main.py11-34](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/main.py#L11-L34)

## Layered Architecture Pattern

### API Layer

The API layer consists of FastAPI routers that handle HTTP requests and responses. Each domain area has its own router module:

| Router Module | Prefix | Purpose |
| --- | --- | --- |
| `users.py` | `/users` | User management operations |
| `cards.py` | `/cards` | Card CRUD operations |
| `collections.py` | `/collections` | Collection management |
| `storage.py` | `/storage` | File upload/download |
| `train_records.py` | `/train_records` | Training session tracking |

All routers are automatically registered through the `all_routers` list in [app/api/\_\_init\_\_.py8-14](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/api/__init__.py#L8-L14) and included in the FastAPI application via [app/main.py32-33](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/main.py#L32-L33)

**Sources:** [app/api/\_\_init\_\_.py1-14](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/api/__init__.py#L1-L14) [app/main.py32-33](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/main.py#L32-L33)

### Service Layer

The service layer encapsulates business logic and coordinates between the API and repository layers. All services inherit from `BaseService` which provides unit of work dependency injection.

The `@with_unit_of_work` decorator in [app/services/base.py9-13](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/services/base.py#L9-L13) ensures that service methods execute within database transactions managed by the Unit of Work pattern.

**Sources:** [app/services/base.py9-19](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/services/base.py#L9-L19) [app/services/train\_record.py13-55](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/services/train_record.py#L13-L55)

### Repository Layer

The repository layer provides data access abstraction through the repository pattern. `BaseSQLAlchemyRepository` implements common CRUD operations that are inherited by domain-specific repositories.

```
«abstract»BaseRepository+create_one(input_data, output_schema)+get_one_or_none(filter_expr, output_schema)+get_all(output_schema, limit, offset)+update_one(filter_expr, update_values, output_schema)+delete(filter_expr)+exists(filter_expr)BaseSQLAlchemyRepository+Table table+AsyncConnection connection+_item_id_filter(item_id)+create_one(input_data, output_schema)+get_one_or_none(filter_expr, output_schema)+update_one(filter_expr, update_values, output_schema)+delete(filter_expr)+exists(filter_expr)UserRepository+Table table = UserTable+get_user_by_id(user_id, output_schema)+get_user_by_columns(column_values, output_schema)+find_users_by_creds(filter_data)+update_user_by_id(user_id, update_values, output_schema)+delete_user_by_id(user_id)+exists_user_with_id(user_id)TrainRecordRepository+Table table = TrainRecordTable+create_train_record(train_data, interval_duration, output_schema)+get_user_card_last_train_record(user_id, card_id, output_schema)+get_collection_training_cards(user_id, collection_cards)
```

Each repository class sets a `table` class variable to specify which database table it operates on, as seen in [app/repositories/user.py13](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/repositories/user.py#L13-L13) and [app/repositories/train\_record.py13](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/repositories/train_record.py#L13-L13)

**Sources:** [app/repositories/base.py15-91](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/repositories/base.py#L15-L91) [app/repositories/user.py12-46](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/repositories/user.py#L12-L46) [app/repositories/train\_record.py12-46](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/repositories/train_record.py#L12-L46)

## Unit of Work Pattern

The `UnitOfWork` class implements transaction management using SQLAlchemy's async connection handling. It ensures that multiple repository operations can be executed within a single database transaction.

### Unit of Work Transaction Flow

```
"Repository""Database Engine""UnitOfWork""Service Method""Repository""Database Engine""UnitOfWork""Service Method"alt[Success][Exception]begin() context managerget_db_engine().begin()AsyncConnectionset connection in ContextVarget_repository(RepoClass)Create repository with connectionRepository instanceperform database operationsexecute SQL statementscommit transactionrollback transactionre-raise exceptionreset ContextVar token
```

The connection is stored in a `ContextVar` at [app/db/unit\_of\_work.py26](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/db/unit_of_work.py#L26-L26) to maintain transaction isolation across async operations. Repository instances are created on-demand through `get_repository()` at [app/db/unit\_of\_work.py40-44](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/db/unit_of_work.py#L40-L44)

**Sources:** [app/db/unit\_of\_work.py17-48](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/db/unit_of_work.py#L17-L48)

## Request Processing Flow

A typical API request flows through all architectural layers, with dependency injection managing the creation and coordination of components.

### Complete Request Flow Example

```
HTTP POST /train_records/{card_id}train_records.py routercreate_train_record() endpointUserIdDep dependencyTrainRecordServiceDepTrainRecordService.init()UnitOfWorkDep injectionservice.create_train_record()@with_unit_of_work decoratoruow.begin() contextuow.get_repository(UserRepository)uow.get_repository(CardRepository)uow.get_repository(TrainRecordRepository)exists_user_with_id()exists_card_with_id()create_train_record()INSERT SQL statementTransaction commitHTTP 200 + TrainRecord JSON
```

This flow demonstrates how a training record creation request at [app/api/train\_records.py21-26](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/api/train_records.py#L21-L26) flows through the service method at [app/services/train\_record.py14-30](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/services/train_record.py#L14-L30) and ultimately executes database operations through repositories.

**Sources:** [app/api/train\_records.py21-26](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/api/train_records.py#L21-L26) [app/services/train\_record.py14-30](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/services/train_record.py#L14-L30) [app/services/base.py9-13](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/services/base.py#L9-L13)

## Key Architectural Benefits

### Separation of Concerns

Each layer has a distinct responsibility:

-   **API Layer**: HTTP protocol handling, request validation, response formatting
-   **Service Layer**: Business logic, workflow orchestration, cross-cutting concerns
-   **Repository Layer**: Data access, query optimization, database abstraction
-   **Data Layer**: Transaction management, connection pooling

### Testability

The dependency injection pattern and interface-based design make the application highly testable. Services can be tested with mock repositories, and repositories can be tested with test databases.

### Maintainability

Clear architectural boundaries make it easy to modify individual components without affecting others. Adding new endpoints requires only implementing the corresponding service methods and repository operations.

**Sources:** [app/repositories/base.py15-39](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/repositories/base.py#L15-L39) [app/services/base.py16-19](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/services/base.py#L16-L19) [app/db/unit\_of\_work.py17-48](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/db/unit_of_work.py#L17-L48)