from sqlalchemy.orm import Session

import models
from database import engine

models.Base.metadata.create_all(bind=engine)

# def init_db(db: Session):
#     pass
