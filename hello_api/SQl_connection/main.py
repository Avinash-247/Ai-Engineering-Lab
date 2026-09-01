from expenses.database import engine,SessionLocal
from expenses.model import Base,Category

Base.metadata.create_all(engine)

print("Database created")

db=SessionLocal()

food=Category(name="Food")
salary=Category(name="Salary")
bills=Category(name="billing")
loans=Category(name="loan")
utilities=Category(name="utilities")
entertainment=Category(name="Entertainment")

db.add_all([food,salary,entertainment,
            loans,utilities,bills])
db.commit()
db.close()
print("This has Done")


