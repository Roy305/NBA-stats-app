from main.model import Player , Player_stats
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
from sqlalchemy import func
from datetime import datetime, timezone ,timedelta
from fastapi import HTTPException
from sqlalchemy.orm import Session
from main.database import get_db
import requests



def save_player(db:Session):
    all_players = players.get_players()
    count = db.query(Player).count()
    
    
    if count == 0:

        for all_nba in all_players:
            nba_all_player = Player( 

                id = all_nba["id"],
                full_name = all_nba["full_name"],
                is_active = all_nba["is_active"]
            
            )
        

            db.add(nba_all_player)
        db.commit()

def save_stats(player_name:str | None , db:Session):
    player = get_player_name(player_name,db)
    if player == None:
        raise HTTPException(status_code=404,detail="player not found")
    nba_time = db.query(Player_stats).filter(Player_stats.player_id == player.id).first()
    
    if nba_time is not None:
        now = datetime.now(timezone.utc)
        diff_time = (now - nba_time.updated_at)
        
        if diff_time < timedelta(days=1):
            return db.query(Player_stats).filter(Player_stats.player_id == player.id).all()

        db.query(Player_stats).filter(Player_stats.player_id == player.id).delete()
        db.commit()
    
    try:

        career = playercareerstats.PlayerCareerStats(
            player.id,
            per_mode36="PerGame",
            timeout=60
            
            )


        for row in career.get_data_frames()[0].to_dict(orient="records"):
        
            if int(row["SEASON_ID"][:4])>=1970:

                stat = Player_stats(
                    player_id = row["PLAYER_ID"],
                    season_id = row["SEASON_ID"],
                    team_name = row["TEAM_ABBREVIATION"],
                    player_age = row["PLAYER_AGE"],
                    play_game = row["GP"],
                    play_min = row["MIN"],
                    fg_pct = row["FG_PCT"],
                    fg3_pct = row["FG3_PCT"],
                    ft_pct = row["FT_PCT"],
                    PTS = row["PTS"],
                    REB = row["REB"],
                    AST = row["AST"],
                    STL = row["STL"],
                    BLK = row["BLK"],
                    TOV = row["TOV"],
                    updated_at = datetime.now(timezone.utc)
                    )
            
                db.add(stat)
        db.commit()
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=408,detail="NBA server timeout")
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=503,detail="NBA server unavailable")
    except Exception:
        raise HTTPException(status_code=500,detail="server error")
    
    return db.query(Player_stats).filter(Player_stats.player_id == player.id).all()
        
def get_player_name(name:str,db:Session):

    return db.query(Player).filter(func.lower(name)==func.lower(Player.full_name)).first()
