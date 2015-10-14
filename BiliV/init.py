from BiliV.foundation import Base, engine

def create_db():
	#load_all_task()
	Base.metadata.create_all(bind=engine)

