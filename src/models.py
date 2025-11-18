from __future__ import annotations
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(80),  unique=True, nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime, server_default=func.now())
    updated_at:   Mapped[Optional[DateTime]] = mapped_column(
        DateTime, onupdate=func.now())

    favorites: Mapped[List["Favorite"]] = relationship(back_populates="user")

    def serialize(self) -> dict:
        return {
            "id":        self.id,
            "username":  self.username,
            "email":     self.email,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


class Planet(db.Model):
    __tablename__ = "planets"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    mass: Mapped[Optional[str]] = mapped_column(String(50))
    description: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime, server_default=func.now())
    updated_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime, onupdate=func.now())

    favorites: Mapped[List["Favorite"]] = relationship(back_populates="planet")

    def serialize(self):
        return {
            "id":        self.id,
            "name":  self.name,
            "mass":     self.mass,
            "is_active": self.is_active,
            "created_at": self.created_at,
        }


class Character(db.Model):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime, server_default=func.now())
    updated_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime, onupdate=func.now())
    
    favorites: Mapped[List["Favorite"]] = relationship(
        back_populates="character")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


class Starship(db.Model):
    __tablename__ = "starships"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    speed: Mapped[Optional[int]]
    faction: Mapped[Optional[str]] = mapped_column(String(50))
    status: Mapped[Optional[str]] = mapped_column(String(30))
    created_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime, server_default=func.now())
    updated_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime, onupdate=func.now())

    favorites: Mapped[List["Favorite"]] = relationship(
        back_populates="starship")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "speed": self.speed,
            "faction": self.faction,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

class Favorite(db.Model):
    __tablename__ = "favorites"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False)
    planet_id: Mapped[Optional[int]] = mapped_column(ForeignKey("planets.id"))
    character_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("characters.id"))
    starship_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("starships.id"))
    created_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime, server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="favorites")
    planet: Mapped[Optional["Planet"]] = relationship(
        back_populates="favorites")
    character: Mapped[Optional["Character"]] = relationship(
        back_populates="favorites")
    starship:  Mapped[Optional["Starship"]] = relationship(
        back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "character_id": self.character_id,
            "starship_id": self.starship_id,
            "created_at": self.created_at
        }