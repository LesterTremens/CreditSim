# CreditSim
Aplicacion que simula una tabla de amortizacion de creditos.

## Arquitectura 

### Backend
- Python 3.12
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- Pytest

### Frontend
- React
- Vite

### Infraestructura
- AWS Elastic Beanstalk (API)
- Amazon RDS (PostgreSQL)
- AWS Amplify (Frontend)

---

## Estructura del repositorio
```
CreditSim/
├── backend/
│ ├── app/
│ │ ├── api/
│ │ ├── core/
│ │ ├── db/
│ │ ├── models/
│ │ ├── schemas/
│ │ └── services/
│ ├── alembic/
│ ├── tests/
│ ├── Procfile
│ └── requirements.txt
│
├── frontend/
│ ├── src/
│ │ ├── components/
│ │ ├── hooks/
│ │ ├── lib/
│ │ ├── App.jsx
│ │ └── styles.css
│ └── package.json
│
└── README.md
```

## Backend

### Services
Se crearon dos servicios uno para calcular la tabla de amortizacion y el otro para simular un servicio externo. 

### Models
Dentro se encuentra el archivo donde se definio la tabla donde se guardan las peticiones.

### Api
Carpeta en donde se encuentraran las rutas de la api.

### Alembic
Se utiliza para hacer las migraciones de los modelos.

### Endpoint principal

**POST /simulate**

#### Request
```json
{
  "amount": 100000,
  "annual_rate": 12.5,
  "term_months": 24
}
```
### Response

```json
{
  "simulation_id": "uuid",
  "summary": {
    "monthly_payment": 4714.51,
    "total_interest": 13148.24,
    "total_payment": 113148.24
  },
  "schedule": [
    {
      "month": 1,
      "payment": 4714.51,
      "principal": 3676.51,
      "interest": 1038.00,
      "remaining_balance": 96323.49
    }
  ]
}
```

## Testing

Incluye:

- Tests unitarios de la lógica de amortización.

- Tests de integración del endpoint /simulate.

- Test de comportamiento asíncrono.

- Test de persistencia usando SQLite en memoria.

Ejecutar tests:

```bash
pytest
```

## Frontend

Se creo una vista con 3 inputs para calcular la tabla de amortizacion.

- Los valores del formulario persisten en localStorage.

- El último resultado se guarda como JSON local.

- Si cualquier campo cambia, la tabla se invalida y desaparece.

## Despliege local

### Requisitos

- Python 3.12 
- Node.js 18
- PostgreSQL local o SQLite

### 1. Backend (FastAPI)

#### 1.1 Entrar al backend y crear entorno virtual

```bash
cd backend
python virtualenv env --python=python3
source env/bin/activate
```
#### 1.2 Instalar dependencias

```bash
pip install -r requirements.txt
```
#### 1.3 Variables de entorno

Crea backend/.env:

```env
DATABASE_URL=sqlite:///./creditsim.db
CORS_ORIGINS=http://localhost:5173
```

#### 1.4 Migraciones
```bash
alembic upgrade head
```

#### 1.5 Levantar servidor

```bash
uvicorn app.main:app --reload
```
### 2. Frontend (React)

#### 2.1 Instalar dependencias

```bash
cd ../frontend
npm install
```

#### 2.2 Variables de entorno

Crea frontend/.env:
```bash
VITE_API_URL=http://localhost:8000
```

2.3 Levantar frontend
```bash
npm run dev
```

## Despliegue AWS

### Backend

- AWS Elastic Beanstalk (single instance).

- Variables de entorno:

    - DATABASE_URL

    - CORS_ORIGINS

- Migraciones ejecutadas con Alembic vía SSH.

### Frontend

- AWS Amplify Hosting.

- Variable de entorno:

    - VITE_API_URL


