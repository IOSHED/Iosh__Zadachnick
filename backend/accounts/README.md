# Django accounts

This is a Django packing that provides user management functionalities. The project includes views for creating, updating, and deleting users, as well as logging in and out. Additionally, it includes views for checking the validity of user input, such as email and password.

## Stack

| Name lib             | Version |
|----------------------|---------|
| Django               | 4.2.5   |
| Django-widget-tweaks | 1.5.0   |
| Htmx                 | 1.9.6   |
| Bootstrap            | 5.0.2   |
| Pillow               | 10.1.0  |


## Installation

To install the project, first clone the repository:
```commandline
git clone ...
```

Then, create a virtual environment and activate it:
```commandline
python -m venv env
source env/bin/activate
```

Install the dependencies:
```commandline
pip install -r requirements.txt
```

Finally, run the development server:
```commandline
python manage.py runserver
```

## Usage

The project includes the following URL patterns:

| Url                             | Name                    | available HTTP requests | description                                                                                                  |
|---------------------------------|-------------------------|-------------------------|--------------------------------------------------------------------------------------------------------------|
| ```create-user/```              | create-user             | GET, POST               | Creates a new user.                                                                                          |
| ```create-info-user/<int:pk>``` | create-info-user        | GET, POST               | Creates additional information for a user with the given primary key.                                        |
| ```login-user/```               | login-user              | GET, POST               | Logs in a user.                                                                                              |
| ```logout-user/```              | logout-user             | GET                     | Logs out the current user.                                                                                   |
| ```delete-user/```              | delete-user             | POST                    | Deletes the current user.                                                                                    |
| ```update-user/```              | update-user             | GET, POST               | Updates the current user's information.                                                                      |
| ```load-icon```                 | load-icon               | POST                    | Loads a image, and then saves two versions of it 64x64 and 32x32 in ```media/files/user_[login user]``` |
| ```check-email/```              | check-email             | POST                    | Checks if there is already such a registered email.                                                          |
| ```check-password/```           | check-password          | POST                    | Checks if a password meets the requirements.                                                                 |
| ```check-re-password/```        | check-check-re-password | POST                    | Checks if a password and its confirmation match.                                                             |
| ```check-have-email/```         | check-have-email        | POST                    | Checks if a user with such an email exists.                                                                  |
| ```check-login-user/```         | check-login-user        | POST                    | Checks whether such a user exists with such a email and password.                                            |

Additionally, the CustomUser model extends Django's AbstractBaseUser and includes fields for name, surname, birthday, creation date, update date, active status, staff status, superuser status, and email verification status.

## TODO

The project has several features that are yet to be implemented:

- Add forgot password functionality.
- Add view detail user functionality.
- Add email activation functionality.
- Use regex 're' in file ```views/check.py``` 

## Credits

This packed was developed by Valentin Ivenin.