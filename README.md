# SaferMaps

SaferMaps optimizes public transportation routes to help users travel safely across NYC. By analyzing crime data, population density, and real-time CCTV feeds, the application generates safer travel paths and visualizes them on an interactive map. Features include route summaries, transport service suggestions, and personalized route options based on user preferences.

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
- llama 3.37 and llama 3.2-11b-vision
- A* search

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
