from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    favorite_characters: Mapped[list["FavoriteCharacter"]] = relationship(
        back_populates="user")
    favorite_planets: Mapped[list["FavoritePlanet"]] = relationship(
        back_populates="user")
    favorite_species: Mapped[list["FavoriteSpecies"]] = relationship(
        back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,

        }


class Characters(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    height: Mapped[int] = mapped_column(nullable=False)
    mass: Mapped[int] = mapped_column(nullable=False)
    hair_color: Mapped[str] = mapped_column(String(120))
    skin_color: Mapped[str] = mapped_column(String(120))
    eye_color: Mapped[str] = mapped_column(String(120))
    birth_year: Mapped[str] = mapped_column(String(120))
    gender: Mapped[str] = mapped_column(String(120))

    planets_id: Mapped[int] = mapped_column(
        ForeignKey("planets.id"), nullable=True)
    homeworld: Mapped["Planets"] = relationship(back_populates="characters")
    species_id: Mapped[int] = mapped_column(
        ForeignKey("species.id"), nullable=True)
    species: Mapped["Species"] = relationship(back_populates="characters")
    favorite_by_link: Mapped[list["FavoriteCharacter"]] = relationship(
        back_populates="character")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "homeworld": self.homeworld.name if self.homeworld else None,
            "species": self.species.name if self.species else None
        }


class Species(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    classification: Mapped[str] = mapped_column(String(120), nullable=False)
    designation: Mapped[str] = mapped_column(String(120), nullable=False)
    average_height: Mapped[str] = mapped_column(String(120), nullable=False)
    skin_colors: Mapped[str] = mapped_column(String(120), nullable=False)
    hair_colors: Mapped[str] = mapped_column(String(120), nullable=False)
    eye_colors: Mapped[str] = mapped_column(String(120), nullable=False)
    average_lifespan: Mapped[str] = mapped_column(String(120), nullable=False)
    language: Mapped[str] = mapped_column(String(120), nullable=False)

    planets_id: Mapped[int] = mapped_column(
        ForeignKey("planets.id"), nullable=True)
    homeworld: Mapped["Planets"] = relationship(back_populates="species")
    characters: Mapped[list["Characters"]] = relationship(
        back_populates="species")
    favorite_by_link: Mapped[list["FavoriteSpecies"]] = relationship(
        back_populates="specie")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "classification": self.classification,
            "designation": self.designation,
            "average_height": self.average_height,
            "skin_colors": self.skin_colors,
            "hair_colors": self.hair_colors,
            "eye_colors": self.eye_colors,
            "average_lifespan": self.average_lifespan,
            "language": self.language,
            "characters": [character.serialize() for character in self.characters],
            "homeworld": self.homeworld.name if self.homeworld else None,
        }


class Planets(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    rotation_period: Mapped[str] = mapped_column(String(120), nullable=False)
    orbital_period: Mapped[str] = mapped_column(String(120), nullable=False)
    diameter: Mapped[str] = mapped_column(String(120), nullable=False)
    climate: Mapped[str] = mapped_column(String(120), nullable=False)
    gravity: Mapped[str] = mapped_column(String(120), nullable=False)
    terrain: Mapped[str] = mapped_column(String(120), nullable=False)
    surface_water: Mapped[str] = mapped_column(String(120), nullable=False)
    population: Mapped[str] = mapped_column(String(120), nullable=False)

    characters: Mapped[list["Characters"]] = relationship(
        back_populates="homeworld")
    species: Mapped[list["Species"]] = relationship(back_populates="homeworld")
    favorite_by_link: Mapped[list["FavoritePlanet"]] = relationship(
        back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "diameter": self.diameter,
            "climate": self.climate,
            "gravity": self.gravity,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "population": self.population,
            "characters": [character.serialize() for character in self.characters],
            "species": [specie.serialize() for specie in self.species]
        }


class FavoriteCharacter(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="favorite_characters")
    character_id: Mapped[int] = mapped_column(
        ForeignKey("characters.id"))
    character: Mapped["Characters"] = relationship(
        back_populates="favorite_by_link")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
        }


class FavoritePlanet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="favorite_planets")
    planet_id: Mapped[int] = mapped_column(
        ForeignKey("planets.id"))
    planet: Mapped["Planets"] = relationship(back_populates="favorite_by_link")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
        }


class FavoriteSpecies(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="favorite_species")
    specie_id: Mapped[int] = mapped_column(
        ForeignKey("species.id"))
    specie: Mapped["Species"] = relationship(back_populates="favorite_by_link")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "specie_id": self.specie_id,
        }