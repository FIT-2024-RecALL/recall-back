# Core Domain Models

This document describes the core business entities and data structures that form the foundation of the recall-back learning platform. These models represent the primary concepts users interact with: users, flashcards, collections, files, and training progress.

The domain models are implemented as Pydantic schemas for API serialization/validation and SQLAlchemy tables for database persistence. For detailed API endpoint usage of these models, see [API Reference](https://deepwiki.com/FIT-2024-RecALL/recall-back/5-api-reference). For the repository layer that manages data access, see [Repository and Data Access Layer](https://deepwiki.com/FIT-2024-RecALL/recall-back/3.3-repository-and-data-access-layer).

## Core Entity Overview

The recall-back platform is built around five primary domain entities that work together to enable spaced repetition learning:

```
Shared BehaviorsRelationship EntitiesCore Domain EntitiesUserUserBase, UserCreate, UserUserAuth, UserDTOCardCardCreate, Cardfront_side, back_sideCollectionCollectionCreate, CollectionCollectionShortFileFileCreate, FileMetaStreamingFileTrainRecordTrainRecordCreateUserAnswer, AIFeedbackCardCollectionMany-to-ManyCard ↔ CollectionFileCardMany-to-ManyFile ↔ CardPublicStatusMixinis_public fieldCamelCaseBaseModelBase Pydantic model
```

Sources: [app/schemas/user.py1-45](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/schemas/user.py#L1-L45) [app/schemas/card.py1-16](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/schemas/card.py#L1-L16) [app/schemas/collection.py1-21](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/schemas/collection.py#L1-L21) [app/schemas/storage.py1-49](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/schemas/storage.py#L1-L49) [app/schemas/train\_record.py1-31](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/schemas/train_record.py#L1-L31)

## User Domain Model

The `User` entity represents platform users and handles authentication, profiles, and ownership relationships. Users own all other content in the system.

### User Schema Hierarchy

| Schema Class | Purpose | Key Fields |
| --- | --- | --- |
| `UserBase` | Common user fields | `nickname`, `email` |
| `UserCreate` | User registration | Extends `UserBase` + `password` |
| `User` | Public user representation | Extends `UserBase` + `id` |
| `UserAuth` | Login credentials | `email`, `password` |
| `UserDTO` | Data transfer object | All fields optional, handles `hashed_password` alias |

### Key Implementation Details

-   Email validation using `EmailStr` from Pydantic
-   Nickname length constraints: 1-35 characters [app/schemas/user.py10](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/schemas/user.py#L10-L10)
-   Password length constraints: 8-40 characters [app/schemas/user.py15](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/schemas/user.py#L15-L15)
-   `UserDTO` provides flexible field mapping with `hashed_password` alias [app/schemas/user.py31](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/schemas/user.py#L31-L31)
-   Custom `table_dict()` method for database operations [app/schemas/user.py43-44](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/schemas/user.py#L43-L44)

Sources: [app/schemas/user.py9-45](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/schemas/user.py#L9-L45)

## Card Domain Model

The `Card` entity represents individual flashcards with front and back content. Cards are the primary learning unit in the spaced repetition system.

### Card Schema Structure

```
CardCreate+front_side: str+back_side: strCard+front_side: str+back_side: str+owner_id: int+is_public: boolPublicStatusMixin+is_public: boolCamelCaseBaseModel+model_config+fields()
```

### Card Business Rules

-   Both `front_side` and `back_side` require minimum length of 1 character [app/schemas/card.py10-11](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/schemas/card.py#L10-L11)
-   Cards inherit public/private visibility through `PublicStatusMixin` [app/schemas/card.py14](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/schemas/card.py#L14-L14)
-   Every card has an `owner_id` linking to the creating user [app/schemas/card.py15](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/schemas/card.py#L15-L15)
-   Cards can be associated with multiple collections through `CardCollection` relationship
-   Cards can have multiple file attachments through `FileCard` relationship

Sources: [app/schemas/card.py9-16](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/schemas/card.py#L9-L16)

## Collection Domain Model

The `Collection` entity groups related cards together and manages their collective visibility and organization.

### Collection Schema Variants

| Schema Class | Purpose | Fields |
| --- | --- | --- |
| `CollectionCreate` | Creating new collections | `title`, `description` |
| `Collection` | Full collection data | Extends `CollectionCreate` + `owner_id` + `is_public` |
| `CollectionShort` | Minimal collection info | `owner_id`, `title`, `is_public` |

### Collection Features

-   Title length constraints: 1-100 characters [app/schemas/collection.py10](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/schemas/collection.py#L10-L10)
-   Optional description field [app/schemas/collection.py11](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/schemas/collection.py#L11-L11)
-   Public/private visibility inheritance to contained cards
-   Owner-based access control through `owner_id` [app/schemas/collection.py15](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/schemas/collection.py#L15-L15)

Sources: [app/schemas/collection.py9-21](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/schemas/collection.py#L9-L21)

## File Storage Domain Model

The `File` entity manages multimedia attachments that can be associated with cards, supporting images, videos, and audio files.

### File Type System

The file system enforces strict type and extension validation:

```
Audio ExtensionsVideo ExtensionsImage ExtensionsAllowedTypesimagevideoaudiobmp, gif, jpg, jpeg, pngsvg, tif, tiff, webpavi, m4v, mkv, mov, mpgmp4, ogv, webm, wmvaac, flac, m4a, mp3mpeg, oga, ogg, wav
```

### File Schema Structure

-   `FileCreate`: Core file metadata with `owner_id`, `filename`, `type`, `ext`, `size` [app/schemas/storage.py31-37](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/schemas/storage.py#L31-L37)
-   `FileMeta`: Extends `FileCreate` with `PublicStatusMixin` for visibility control [app/schemas/storage.py39-40](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/schemas/storage.py#L39-L40)
-   `StreamingFile`: Special model for file transfer with metadata and `FileStream` [app/schemas/storage.py43-48](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/schemas/storage.py#L43-L48)

### File Business Rules

-   Supported types defined by `AllowedTypes` literal [app/schemas/storage.py11](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/schemas/storage.py#L11-L11)
-   Supported extensions defined by `AllowedExts` literal [app/schemas/storage.py12-16](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/schemas/storage.py#L12-L16)
-   File visibility cascades from associated cards' public status
-   Unique filename constraint in database [app/db/models/file.py19](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/db/models/file.py#L19-L19)
-   Size tracking optional [app/schemas/storage.py36](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/schemas/storage.py#L36-L36)

Sources: [app/schemas/storage.py11-49](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/schemas/storage.py#L11-L49) [app/db/models/file.py15-24](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/db/models/file.py#L15-L24)

## Training and Progress Domain Model

The `TrainRecord` entity implements the spaced repetition algorithm by tracking user progress on individual cards.

### Training Schema Components

```
TrainRecordCreate+mark: int [1-5]TrainRecord+id: int+card_id: int+user_id: int+mark: int [1-5]+repeat_date: datetime+next_repeat_date: datetime+progress: float [0.0-1.0]UserAnswer+answer: strAIFeedback+mark: int+comment: str
```

### Spaced Repetition Implementation

-   `mark`: User performance rating from 1-5 [app/schemas/train\_record.py12](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/schemas/train_record.py#L12-L12)
-   `progress`: Learning progress as float between 0.0-1.0 [app/schemas/train\_record.py21](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/schemas/train_record.py#L21-L21)
-   `repeat_date`: When the training session occurred [app/schemas/train\_record.py19](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/schemas/train_record.py#L19-L19)
-   `next_repeat_date`: When card should be reviewed next [app/schemas/train\_record.py20](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/schemas/train_record.py#L20-L20)
-   `UserAnswer`: Captures user's text response for AI evaluation [app/schemas/train\_record.py24-25](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/schemas/train_record.py#L24-L25)
-   `AIFeedback`: AI-generated score and feedback [app/schemas/train\_record.py28-30](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/schemas/train_record.py#L28-L30)

Sources: [app/schemas/train\_record.py11-31](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/schemas/train_record.py#L11-L31)

## Entity Relationships and Data Flow

The domain models form a cohesive system where users create and organize content for spaced repetition learning:

```
owns (owner_id)owns (owner_id)uploads (owner_id)practices (user_id)belongs_tocontainshas_attachmentsattached_topracticed_in (card_id)UserintidPKstringemailUKstringnicknamestringhashed_passwordCardintidPKintowner_idFKstringfront_sidestringback_sideboolis_publicCollectionintidPKintowner_idFKstringtitlestringdescriptionboolis_publicFileintidPKintowner_idFKstringfilenameUKenumtypeenumextintsizeboolis_publicTrainRecordintidPKintuser_idFKintcard_idFKintmarkdatetimerepeat_datedatetimenext_repeat_datefloatprogressCardCollectionFileCard
```

### Visibility and Access Control

The platform implements a sophisticated public/private visibility system:

1.  **User-owned content**: All entities (except `TrainRecord`) have an `owner_id` linking to the creating user
2.  **Public/private flag**: Cards, Collections, and Files inherit from `PublicStatusMixin` providing `is_public` boolean
3.  **Cascading visibility**: When a collection becomes public, its cards may also become visible; when cards become public, their attached files may also become visible
4.  **Training privacy**: `TrainRecord` entities are always private to the practicing user

Sources: [app/schemas/base.py](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/schemas/base.py) (PublicStatusMixin), [app/schemas/card.py14](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/schemas/card.py#L14-L14) [app/schemas/collection.py14](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/schemas/collection.py#L14-L14) [app/schemas/storage.py39](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/schemas/storage.py#L39-L39)