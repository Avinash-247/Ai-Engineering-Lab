from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey


class Base(DeclarativeBase):
    pass


class Category(Base):
    __tablename__ = "Categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))

    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="category"
    )


class Transaction(Base):
    __tablename__ = "transaction"

    id: Mapped[int] = mapped_column(primary_key=True)

    amount: Mapped[float]

    description: Mapped[str] = mapped_column(String(500))

    type: Mapped[str] = mapped_column(String(500))

    category_id: Mapped[int] = mapped_column(
        ForeignKey("Categories.id")
    )

    category: Mapped["Category"] = relationship(
        back_populates="transactions"
    )