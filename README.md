# Hotel Details Project
> This Django-based project manages hotel details, including locations, amenities, and property information. It includes an admin panel for data management and a custom data migration tool for importing data from a Scrapy database.

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/Speak2/Django_assignment/graphs/commit-activity)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/Speak2/Django_assignment/issues)


![Alt text](readme_img/Screenshot%20from%202024-08-16%2017-06-21.png)



## Table of Contents
1. [Requirements](#requirements)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Running the Project](#running-the-project)
5. [Database Creation guide ](#database-creation-guide )
6. [Admin Panel](#admin-panel)
7. [Data Migration](#data-migration)
8. [Key Features](#hotel-details-project---key-features)
9. [Project Structure](#project-structure) 
10. [Technologies Used](#technologies-used)
10. [Development Tools](#development-tools)
11. [Author](#authors)
12. [License](#license)

## Requirements 
Tools and packages required to successfully install this project.
For example:
- Python 3.x
- Django
- PostgreSQL

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Speak2/Django_assignment
   cd Django_assignment
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
4. before running this project run the updated **`scrapy_project`**

   github repository -  https://github.com/Speak2/web_crawler

   **Please Note:**

    **Due to recent changes in images file names in the scrapy project, running the Django project with the previous Scrapy project database will result in errors.Because it is functional with the updated scrapy project. To ensure proper functionality, please either:**

   - **Drop the Existing Scrapy Database & run the Scrapy project:**
    If you have run the project before kindly drop the existing database before proceeding.

   - **Use a Different Database Name & run the scrapy project:** Alternatively, you can use a new database name to avoid any conflicts with the previous database and run the scrapy project.


## Configuration

1. **Create a New `config.py` File**:

   Please create a new file named `config.py` in the `Django_assignment/config.py` directory. Include the following code in this file, ensuring that you replace the placeholders with your specific database configuration details:
   ```python
   DJANGO_DATABASE_CONFIG = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'database_name',
    'USER': 'user_name',
    'PASSWORD': 'password',
    'HOST': 'localhost',
    'PORT': 'port_number',
   }
   ```

   Make sure to adjust these settings according to your PostgreSQL configuration.


2. **Set the Base Directory Path for Scrapy Spider Images:**

   Define the base directory path for Scrapy spider images within the `config.py` file as follows for your pc-
   
   ```python
   WEB_CRAWLER_BASE_PATH = '/home/w3e02/last final check/web_crawler/dynamic_crawling/' 
   # your_pc_base_path/web_crawler/dynamic_crawling/
   ```
3. **Set the Scrapy Database Configuration:**

   Configure the Scrapy database settings in the `config.py` file using the following structure:
   ```python
   SCRAPY_DATABASE_CONFIG = {
    'NAME': 'database_name',
    'USER': 'user_name',
    'PASSWORD': 'password',
    'HOST': 'localhost',
    'PORT': 'port_number',
   }
   ```
4. For reference follow the `config-sample.txt` file in the root directory.
 

## Running the Project

1. **Database Creation:**

   Before running the project, it is essential to create the Django database. Additionally, ensure that the database name specified in the `config.py` file under the `django_database_config` value matches the created database. To create the database, execute the following SQL command:

   ```sql
   CREATE DATABASE database_name;
   ```
   Please note that for the Scrapy project, the logic for automatic database creation has already been implemented in that project. No need to worry about the scrapy project database.

2. **Database Setup**

   You have two options for setting up the database tables:

   - **Manual Creation:**
   You can manually create the database tables by executing the necessary SQL commands.
   - **Automatic Creation via Migrations:**
   Alternatively, you can use Django’s migration system to automatically create the database tables. This method is recommended as it ensures that the database schema matches the models defined in your project.

      ```bash
      python manage.py migrate
      ```

2. **Create a superuser(Admin user):**
   ```bash
   python manage.py createsuperuser
   ```
3. **Data Migration From scrapy database:**

   Use the following command to run the CLI application, which facilitates the migration of data from the Scrapy database to the Django database. Please ensure that an admin user is created beforehand, as this application requires admin authentication.

   ```bash
   python manage.py migrate_scrapy_data
   ```

4. Start the development server:
   ```bash
   python manage.py runserver
   ```

5. Access the application at `http://127.0.0.1:8000/`
6. Access the admin panel at `http://127.0.0.1:8000/admin`

## Database Creation guide 

In order to create the database use the following sql-

```sql
CREATE DATABASE database_name;
```

The schema for the `Location` table-
```sql
CREATE TABLE Location (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(20) CHECK (type IN ('country', 'state', 'city')) NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    create_date TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_date TIMESTAMPTZ
);
```

The schema for the `Amenity` table-
```sql
CREATE TABLE Amenity (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    create_date TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_date TIMESTAMPTZ
);
```

The schema for the `Property` table, along with the schema for the many-to-many relationship tables between the `Locations` table and the `Property` table, as well as the `Amenities` table and the `Property` table-
```sql
CREATE TABLE Property (
    id SERIAL PRIMARY KEY,
    property_id INTEGER NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    create_date TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_date TIMESTAMPTZ
);

CREATE TABLE Property_locations (
    id SERIAL PRIMARY KEY,
    property_id INTEGER NOT NULL REFERENCES Property(id) ON DELETE CASCADE,
    location_id INTEGER NOT NULL REFERENCES Location(id) ON DELETE CASCADE
);

CREATE TABLE Property_amenities (
    id SERIAL PRIMARY KEY,
    property_id INTEGER NOT NULL REFERENCES Property(id) ON DELETE CASCADE,
    amenity_id INTEGER NOT NULL REFERENCES Amenity(id) ON DELETE CASCADE
);
```

The schema for the `PropertyImage` table-
```sql
CREATE TABLE PropertyImage (
    id SERIAL PRIMARY KEY,
    property_id INTEGER NOT NULL REFERENCES Property(id) ON DELETE CASCADE,
    image VARCHAR(100) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ,
    caption VARCHAR(255) DEFAULT NULL,
    is_featured BOOLEAN NOT NULL DEFAULT FALSE
);
```
## Admin Panel

Access the admin panel at `http://127.0.0.1:8000/admin/` using the superuser credentials.

## Data Migration

To migrate data from the Scrapy database to Django, use the custom cli command:

```bash
python manage.py migrate_scrapy_data
```
this requires admin authentication, so ensure that you have created a superuser(admin user) before executing this
     
## Screenshots
This is the register information of the property details followed by upload images for each hotels

![Screenshots of projects](readme_img/hotel_details.png)

![Screenshots of the project](readme_img/hotel_images.png)


 
## Hotel Details Project - Key Features

- **Data Management**
  - Location (countries, states, cities) with geocoding
  - Amenities
  - Properties with multi-location and amenity associations
  - Property images with featured image functionality

- **Admin Panel**
  - Customized admin interface for all models
  - Image preview and management
  - List filters and search functionality

- **Data Migration Tool**
  - Custom command for Scrapy to Django data import
  - Dry-run option for testing

- **User Authentication**
  - Admin user management

- **File Management**
  - Static file serving (CSS, JavaScript, images)
  - Media file handling for uploaded images

- **Database**
  - PostgreSQL integration

- **Development Tools**
  - flake8 linter support
  - autopep8 integration for code formatting

- **Security Features**
  - CSRF protection
  - Configurable secret key

- **Internationalization**
  - Built-in i18n support

- **Time Zone Support**
  - Configured for Asia/Dhaka (customizable)



## Project Structure

- `admin_panel/`: Main application for the admin interface
- `data_migration_cli/`: Custom management command for data migration
- `hotel_details_project/`: Project settings and configuration
- `static/`: Static files (CSS, JavaScript)
- `property_images/`: Uploaded property images

   ```bash
   Django_assignment/
   │
   ├── admin_panel/   
   │   ├── migrations/
   │   ├── static/
   │   ├── __init__.py                   
   │   ├── admin.py 
   │   ├── apps.py
   │   ├── models.py
   │   └── views.py
   ├── data_migration_cli/                    
   │   └── management          
   │      └── commands    
   │          └── migrate_scrapy_data.py 
   ├── hotel_details_project/          
   │   ├── settings.py 
   │   ├── urls.py
   │   └── wsgi.py 
   ├── static/
   │   └── js/
   │       └── admin    
   │           ├── image_preview.js
   │           └── property_image_preview.js
   ├── readme_img/
   ├── manage.py
   ├── config.py
   ├── config-sample.py           
   ├── README.md   
   ├── requirements.txt      
   └── LICIENSE            
   ```

## Technologies used

- Django
- PostgreSQL
- Scrapy
- Django Admin
- HTML/CSS
- JavaScript
- Python
- Pillow
- Django ORM 
- CLI Application

## Development Tools

- Linter: flake8 (install from VS Code extension store)
- Code formatter: autopep8 (install from VS Code extension store)

Remember to run the linter and formatter regularly to maintain code quality.

## Authors
This project is for Django admin panel practice created by me for assignment purposes during my internship days at w3 egnineers ltd. 
 
Nahid Mahamud  – nahid.nm91@gmail.com
 
 You can find me here at:
[Github](https://github.com/Speak2) 





## License
A short snippet describing the license (MIT, Apache etc).

This project is licensed under the MIT License - see the LICENSE.md file for details

MIT © Nahid Mahamud