from fastapi import FastAPI, HTTPException
import json
from pydantic import BaseModel
app = FastAPI()


class Employee(BaseModel):
    id: int
    name: str
    role: str 
    salary: int
    skills: list
    active: bool  



@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items")
def show(id: int = None):

    with open("data.json", "r") as f:
        data = json.load(f)
    if id == None:
        return data
    else:
        for employee in data["employees"]:
            if employee["id"] == id:
                return employee

        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

@app.post("/addEmp")
def addDetails(employee: Employee):
    with open("data.json", "r") as f:
        data = json.load(f)

    # Check if ID already exists
    for emp in data["employees"]:
        if emp["id"] == employee.id:
            raise HTTPException(409, "Employee already exists")

    # Add new employee
    data["employees"].append(employee.model_dump())

    # Save updated JSON
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)

    return {
        "message": "Employee created successfully",
        "employee": employee
    }

@app.post("/updateEmp")
def addDetails(employee: Employee):
    with open("data.json") as f:
        data = json.load(f)

    found = False

    for index, emp in enumerate(data["employees"]):
        if emp["id"] == employee.id:
            found = True
            data["employees"][index] = employee.model_dump()
            break
    if not found:
        raise HTTPException(404, "Employee not found")

    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)

    return {
        "message": "Employee updated successfully",
        "employee": employee.model_dump()
    }

@app.delete("/deleteEmp")

def deleteEmp(id: int):
    with open ("data.json") as f:
        data = json.load(f)
    employee_found = False

    for emp in data["employees"]:
        if emp["id"] == id:
            data["employees"].remove(emp)
            employee_found = True
            break

    if employee_found != True:
        raise HTTPException(404, "Employee not found")

    with open ("data.json", 'w') as f:
            json.dump(data, f, indent=4)

    return {
        "message": "Employee deleted successfully",
        "deleted_id": id
    }