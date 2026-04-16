from fastapi import FastAPI, HTTPException

app = FastAPI()

users = []

def add_user(name: str):
    if name in users: 
        return False
    users.append(name)
    return True

@app.post("/users/")
async def create_user(name: str):
    if add_user(name):
        return {"message": f"Користувача {name} успішно додано."}
    else:
        raise HTTPException(status_code=400, detail="Користувач з таким іменем вже існує")

@app.get("/users")
async def get_all_users():
    return {"users": users}

@app.get("/users/{name}")
async def get_user(name: str):
    if name in users:
        return {"user": name}
    else:
        raise HTTPException(status_code=404, detail="Користувача з таким іменем не існує")

@app.delete("/users/{name}")
async def delete_user(name: str):
    if name in users:
        users.remove(name)
        return {"message": f"Користувача {name} успішно видалено."}
    else:
        raise HTTPException(status_code=404, detail="Користувача з таким іменем не існує")