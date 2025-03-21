# *Proyecto HBnB*


## 🧐 What is HBnB?
HBNB is a web application that allows users to register, search and reserve places to stay. This project was carried out by students of Holberton School Uruguay as part of the main project of the second quarter, which consists in creating a copy of the accommodation application; Airbnb.

## 📊 Content Table

- [Description](#descripción)
- [Project Structure](#estructura-del-proyecto)
- [Architecture and Layers](#arquitectura-y-capas)
- [Diagrams](#diagramas)
- [Models](#modelos)
- [Tests](#pruebas)
- [Use](#uso)
- [Details and Characteristics](#detalles-y-características)
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

## Diagrams
