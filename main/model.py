
from sqlalchemy import Column, Integer, String, Boolean , Float, DateTime
from main.database import Base

class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    is_active = Column(Boolean)

class Player_stats(Base):
    __tablename__ = "player_stats"
    id = Column(Integer,primary_key=True)
    player_id = Column(Float)
    season_id = Column(String)
    team_name = Column(String)
    player_age = Column(Float)
    play_game = Column(Float)
    play_min = Column(Float)
    fg_pct = Column(Float)
    fg3_pct = Column(Float)
    ft_pct = Column(Float)
    PTS = Column(Float)
    REB = Column(Float)
    AST = Column(Float)
    STL = Column(Float)
    BLK = Column(Float)
    TOV = Column(Float)
    FLS = Column(Float)
    updated_at = Column(DateTime(timezone=True))
    