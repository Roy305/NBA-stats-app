from fastapi import FastAPI , HTTPException,Depends
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players
from main.model import Player , Player_stats
from main.database import engine , Base ,get_db
from main.crud import save_player , get_player_name ,save_stats
from sqlalchemy.orm import Session


app = FastAPI()

Base.metadata.create_all(engine)
db=next(get_db())
save_player(db)

players_db = [
    {"name":"jordan", "number":23},
    {"name":"lebron", "number":23},
    {"name":"curry","number":30}
]
@app.get("/nba")
def read_root():
    return {"stephen":"curry"}

@app.get("/players")
def players():
    return players_db

@app.get("/player_id/{player_id}")
def read_player(player_id: int , player:str | None = None):
    return {"player_id":player_id ,"player":players_db[player_id] }

@app.get("/player_name/{player_name}")
def read_name(player_name:str,db:Session=Depends(get_db)):

    player = get_player_name(player_name,db)
    
    if player == None:
        raise HTTPException(status_code=404 , detail="Not Found")
    return {"player_name":player_name,"player":player}

@app.get("/player_stats/{full_name}")
def read_stats(full_name: str,db:Session=Depends(get_db)):
    return save_stats(full_name,db)


