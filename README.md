# *Proyecto HBnB*


## 🧐 What is HBnB?
HBNB is a web application that allows users to register, search and reserve places to stay. This project was carried out by students of Holberton School Uruguay as part of the main project of the second quarter, which consists in creating a copy of the accommodation application; Airbnb.

## 📊 Content Table

- [Description](#descripción)
- [Project Structure](#estructura-del-proyecto)
- [Architecture and Layers](#arquitectura-y-capas)
- [Diagrams](#diagramas)
- [Tests](#pruebas)
- [Use](#uso)
- [Authors](#autores)

## 📝 Description of the Project

The HBNB project is a web application that allows users:
- Register and authenticate.
- Create, update and delete places (Places).
- Create, update and delete reviews (reviews) of places.
- Look for available places.
- Manage amenities (amenities) associated with places.

## 🏗️ Project Structure

The project is divided into four parts: 

1. *UML and Technical Documentation*
2. *Business Logical and API Endpoints*
3. *Authentication and Database Integration*
4. *Simple Web Client (Coming Soon)*

### 1. *UML and Technical Documentation*

In this initial phase, we focus on creating comprehensive technical documentation that served as the basis for the development of the HBNB application. This documentation helped us to understand the general architecture, the detailed design of business logic and interactions within the system.

### 2. *Business Logical and API Endpoints*

In this part of the HBnB Project, we start the implementation phase of the application based on the design developed in the previous part. The objective of this phase was to build the Presentation and Business Logic layers of the application using Python and Flask. We implemented the core functionality by defining the necessary classes, methods and endpoints that served as the basis for the operation of the application.

### 3. *Authentication and Database Integration*

In this part of the project is where we extend the backend of the application by introducing user authentication, authorization and database integration using SQLAlchemy and SQLite for development. In this part, we secured the backend, introduced persistent storage, and prepared the application for scalable real-world deployment.

### 4. *Simple Web Client (Coming Soon)*

In this phase, we will focus on developing the frontend of the HBnB application. The goal will be to create a user-friendly web interface that interacts seamlessly with the backend API. This web client will allow users to explore, filter, and manage listings efficiently. More details will be provided as development progresses.

## 👷 Architecture and Layers

The HBnB project follows a layered architecture to ensure modularity, scalability, and maintainability. This architecture divides the system into multiple layers, each with a specific responsibility, ensuring a clean separation of concerns.

1. Presentation Layer (Frontend & API Endpoints)
The Presentation Layer is responsible for handling user interactions and displaying data from the backend. It consists of:

2. Business Logic Layer (BLL)
The Business Logic Layer (BLL) contains the core logic and rules governing the application. It acts as an intermediary between the Presentation Layer and the Persistence Layer, ensuring proper validation and processing of data.

3. Persistence Layer (Database & ORM)
The Persistence Layer is responsible for data storage and retrieval, ensuring data integrity and consistency.

4. Facade (Service)
The Facade Pattern is used to provide a unified interface to the underlying system components. It serves as a Service Layer that simplifies interactions between the Presentation Layer and the BLL.

5. APIs (Bridge Between Layers)
APIs act as the bridge between different layers, ensuring smooth communication.

## 👓 Diagrams

To better understand the architecture and interactions within the HBnB project, we provide three key diagrams:

- Class Diagram – Represents the structure of the system, including the main classes and their relationships.
- Sequence Diagram – Shows the flow of interactions between components during a specific process.
- Layer Diagram – Illustrates the architectural layers of the system and their dependencies.

These diagrams help visualize the design and functionality of the project, ensuring clarity in system development and maintenance.


### 1. *Class Diagram*

The Class Diagram provides an overview of the system's object-oriented structure, representing the main classes, their attributes, methods, and relationships (inheritance, associations, dependencies).

In the HBnB project, the class diagram includes key entities such as:

- User – Represents application users with authentication details.
- Place – Stores information about listings, including location and amenities.
- Review – Contains user-generated reviews linked to places.
- Amenity – Represents additional features available in a place.
- Base - Contains attributes and methods that will be shared by the other classes

This diagram helps in understanding how different parts of the system interact and how data flows between objects.

![Class Diagram](https://github.com/Ifabri31/holbertonschool-hbnb/blob/main/images/Diagrama%20de%20Clases.png)

---

### 2. *Sequence Diagram*

A Sequence Diagram illustrates the flow of interactions between different system components in a specific use case. It helps visualize how requests are processed and how different objects communicate over time.

For the HBnB project, a typical sequence diagram might illustrate:

### User Registration

![Class Diagram](https://github.com/Ifabri31/holbertonschool-hbnb/blob/main/images/Diagrama%20de%20Secuencias%20-%20User%20Registration.png)

### Description:

This flow represents the process of registering a new user. It involves data validation and verification of the user's existence in the database.

### Process Steps:

1. The user requests to register using the API.
2. The API sends the data to the business logic layer (BL).
3. BL validates the user's data:
    - If the data is invalid, an error is returned.
4. BL queries the database to see if the user already exists:
    - If the user exists, an error indicating “User exists” is returned.
    - If it does not exist, a new user is inserted in the database.
5. success message is returned if the user was successfully registered.

---

### Place Creation

![Class Diagram](https://github.com/Ifabri31/holbertonschool-hbnb/blob/main/images/Diagrama%20de%20Secuencias%20-%20Place%20Creation.png)

### Description:

This flow shows how the creation of a new site is handled, from data validation to insertion into the database.

### Process Steps:

1. The user requests to create a place via the API.
2. The API sends the place data to BL.
3. BL validates the place data:
    - If the data is invalid, an error is returned.
4. BL inserts the new place into the database.
    - If the place already exists, a “Place exists” error is returned.
5. A success message is returned if the place was created successfully.

---

### Review Submission

![Class Diagram](https://github.com/Ifabri31/holbertonschool-hbnb/blob/main/images/Diagrama%20de%20Secuencias%20-%20Review.png)

### Description:

This flow details how the submission of a review for a given location is processed.

### Process Steps:

1. The user submits a review via the API.
2. The API sends the review data to BL
3. BL validates the review data:
    - If the data is invalid, an error is returned.
4. BL checks if a user review already exists for that location:
    - If the review already exists, an error is returned stating “User Review Exist for Current Place”.
5. The new review is inserted into the database and a success message is returned.

---

### Fetching List of Places

![Class Diagram](https://github.com/Ifabri31/holbertonschool-hbnb/blob/main/images/Diagrama%20de%20Secuencias%20-Fetching%20List%20of%20Places.png)

### Description:

This flow shows the process of retrieving a list of places stored in the database.

### Process Steps:

1. The user requests the list of places via the API.
2. The API sends the request to BL.
3. BL queries the places in the database:
    - If no places are found, a message indicating “Places Not Found” is returned.
4. The list of found places is returned.

---

### 3. *Layer Diagram*

The Layer Diagram provides a high-level view of the system architecture, illustrating how different layers interact while maintaining a clean separation of concerns.

For HBnB, the main layers include:

- Presentation Layer – The UI (web client) and API endpoints that interact with users.
- Business Logic Layer (BLL) – Handles application logic, validation, and processing.
- Persistence Layer – Manages database storage using SQLAlchemy.
- Facade Layer – Serves as an intermediary between the API and core business logic.

![Class Diagram](https://github.com/Ifabri31/holbertonschool-hbnb/blob/main/images/Diagrama%20de%20Capas.png)

## 👨‍💻 Test and Use

### ~~Testing~~

To run the tests, navigate to the `part3/hbnb` directory and execute the `test.py` file:

```
python test.py
```

The tests are written using Python’s `unittest` module and cover the API endpoints for Users, Places, Reviews, and Amenities.

### Tested Endpoints

1. User Endpoints
  - POST /api/v1/users - Create a user
  - GET /api/v1/users - List all users
  - GET /api/v1/users/{id} - Retrieve a user by ID
  - PUT /api/v1/users/{id} - Update a user
    
Example Test - Creating a User

Input:

```
{
  "first_name": "Jane",
  "last_name": "Doe",
  "email": "jane.doe@example.com"
}
```
*Expected Result:* Status code 201 (Created)

2. Place Endpoints
  - POST /api/v1/places/ - Create a place
  - GET /api/v1/places/ - List all places
  - GET /api/v1/places/{id} - Retrieve a place by ID
  - PUT /api/v1/places/{id} - Update a place
    
Example Test - Creating a Place

Input:

```
{
  "title": "Cozy Apartment",
  "description": "A nice place to stay",
  "price": 100.0,
  "latitude": 37.7749,
  "longitude": -122.4194,
  "owner_id": "1"
}
```
*Expected Result:* Status code 201 (Created)

3. Review Endpoints
  - POST /api/v1/reviews/ - Create a review
  - GET /api/v1/reviews/ - List all reviews
  - GET /api/v1/reviews/{id} - Retrieve a review by ID
  - DELETE /api/v1/reviews/{id} - Delete a review
    
Example Test - Creating a Review

Input:

```
{
  "text": "Great place to stay!",
  "rating": 5,
  "user_id": "1",
  "place_id": "1"
}
```
*Expected Result:* Status code 201 (Created)

4. Amenity Endpoints
- POST /api/v1/amenities/ - Create an amenity
- GET /api/v1/amenities/ - List all amenities
- GET /api/v1/amenities/{id} - Retrieve an amenity by ID
- PUT /api/v1/amenities/{id} - Update an amenity
    
Example Test - Creating an Amenity

Input:

```
{
  "name": "WiFi"
}
```
*Expected Result:* Status code 201 (Created)

### ~~Use~~

#### Running the Application

To start the application, navigate to the `part3/hbnb` directory and execute the `run.py` file:

```
python run.py
```

## 😎 Authors

* **[Franco Reyes](https://github.com/Franco-byte)**
* **[Fabrizzio Oviedo](https://github.com/Ifabri31)**
* **[Jonathan Pérez](https://github.com/Jonatha32)**




