<h1 align='center'>FEPsino</h1> 

<p align='center'>
  <img src="https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python" alt="Python"/>
  <img src="https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray" alt="Django REST"/>
  <img src="https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB" alt="React"/>
  <img src="https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="TailwindCSS"/>
  <img src="https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL"/>
  <img src="https://img.shields.io/badge/Docker-blue?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />
  <img src="https://img.shields.io/badge/SonarQube-black?style=for-the-badge&logo=sonarqube&logoColor=4E9BCD" alt="Sonarqube"/>
</p>

---
## Overview

FEPsino is a group project that serves as an online casino that includes games such as BlackJack, Slots and Dice. Also, this project is a fully Dockerized web application designed for seamless deployment and scalability. It leverages modern technologies such as Django REST Framework, React, and PostgreSQL to provide a robust and efficient backend, paired with a sleek and responsive frontend. The project also integrates Sonarqube for code quality analysis, ensuring maintainability and high standards in development.  

---

## Getting Started  

The project is fully Dockerized and can be built with the following command:

```bash
docker-compose up --build
```

To run the project next time:

```bash
docker-compose up 
```

**Backend:** Runs on **`http://localhost:8000`**  
**Frontend:** Runs on **`http://localhost:5173`**  

---

## Sonarqube  

This project uses **Sonarqube** for easy code review and refactoring. Sonarqube and Sonar Scanner are run automatically with the whole project.  

**Manually launch the Sonarqube Scanner:**  

```bash
docker-compose up sonarscanner
```

---

## Example of `.env` file  

Create this file in the **root of the project**:

```bash
SECRET_KEY=your-secret-key

DB_HOST=db
DB_NAME=dbname
DB_USER=username
DB_PASS=userpass

SONAR_HOST_URL=sonar-host
SONAR_PROJECT_KEY=sonar-key
SONAR_PROJECT_NAME=sonar-name
SONAR_TOKEN=sonar-token

SONAR_JDBC_URL=sonar-url
SONAR_JDBC_USERNAME=sonar-username
SONAR_JDBC_PASSWORD=sonar-user-ass

VITE_API_URL=vite-api-url
```
