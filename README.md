# FlixMix API in DRF

[Live link](https://agustin-cilli-flixmix-api.herokuapp.com/)

This code repository hosts the collection of APIs implemented with Django REST Framework, specifically designed to support the functionality of the FlixMix application's user interface. ([repository here](https://github.com/cilliagustin/flixmix) and [live website here](https://agustin-cilli-flixmix.herokuapp.com/))


## User Stories
The backend segment of the project primarily emphasizes its administrative aspect and encompasses two user stories:
- User story: Admin control of database
    - As an Admin, I can edit or delete any movie uploaded to the database as well as the lists reviews and comments created by the users to control the database posted and avoid inappropriate content
- User story: View and Delete reports:
    - As an Admin, I can view and delete reports created by users so that i can be aware of possible errors or innapropiate content and act accordingly

## Database
The subsequent models were designed to depict the structural layout of the application's database model:

<!-- ADD MODEL DIAGRAM -->

#### User Model
- The User model is a base model that comes by default with the django auth module

#### Profile Model
- Fk relation user model
- Stores the following information: created_at, updated_at, name, description (bio of the user) image and is_admin (Boolean only true for administrator profiles)

#### Movie Model
- Fk relation user model
- Stores the following information: created_at, updated_at, title, synopsis, poster, main_cast, directors genre and release_year

#### Rating Model
- Fk relation user model
- Fk relation movie model
- Stores the following information: created_at, updated_at, title, content, value

#### List Model
- Fk relation user model
- Many to many relation with movie model
- Stores the following information: created_at, updated_at, title, description


#### CommentBase Model
- Fk relation user model
- Stores the following information: created_at, updated_at, content

#### ListComment Model
- Inherits from CommentBase
- Fk relation List model

#### RatingComment Model
- Inherits from CommentBase
- Fk relation Rating model

#### Seen Model
- Fk relation user model
- Fk relation movie model
- Stores the following information: created_at

#### Watchlist Model
- Fk relation user model
- Fk relation movie model
- Stores the following information: created_at

#### Follower Model
- Fk relation between the owner field and the User model id field
- Fk relation between the followed field and the User model post field
- Stores the following information: created_at

#### Report Model
- Fk relation user model
- Fk relation movie model
- Stores the following information: created_at, content

