# SaferMaps

This is our project for DevFest 2025 at Columbia University. 

A full stack app for generating safe routes from departure location to the destination. 
---

## **Tech Stack**

### **Frontend**
- React
- Vite
- CSS

### **Backend**
- Flask
- MongoDB

### **AI Integration**
- **Groq AI**
---

## **Installation**

```
python -m venv env
source env/bin/activate
```

### **1. Clone the Repository**
```bash
git clone https://github.com/hibaa8/devfest.git
cd devfest
```

### **2. Backend Setup**

Navigate to the backend directory:
```bash
cd backend
```

Install the necessary requirements
```bash
pip install -r requirements.txt   
```

Run the Flask app:
```bash
flask run
```

### **3.Frontend Setup**

Open a new terminal window and navigate to the frontend directory:
```bash
cd ../frontend
```

Install dependencies:
```bash
npm install
```

Start the development server:
```bash
npm start
```

### **View the App**
Open your browser and navigate to: http://localhost:5173/
(flask server should be running on port 5000)
