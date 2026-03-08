/*
    Pokémon neo
    ------------------------------

    file        : type.h
    author      : Philip Wellnitz
    description : Header file. Consult the corresponding source file for details.

    Copyright (C) 2012 - 2022
    Philip Wellnitz

    This file is part of Pokémon neo.

    Pokémon neo is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Pokémon neo is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Pokémon neo.  If not, see <http://www.gnu.org/licenses/>.
*/

#pragma once

namespace BATTLE {
    constexpr u8 NUM_TYPES = 19;

    enum type : u8 {
        TYPE_NORMAL    = 0,
        TYPE_FIGHTING  = 1,
        TYPE_FLYING    = 2,
        TYPE_POISON    = 3,
        TYPE_GROUND    = 4,
        TYPE_ROCK      = 5,
        TYPE_BUG       = 6,
        TYPE_GHOST     = 7,
        TYPE_STEEL     = 8,
        TYPE_UNKNOWN   = 9,
        TYPE_WATER     = 10,
        TYPE_FIRE      = 11,
        TYPE_GRASS     = 12,
        TYPE_LIGHTNING = 13,
        TYPE_PSYCHIC   = 14,
        TYPE_ICE       = 15,
        TYPE_DRAGON    = 16,
        TYPE_DARKNESS  = 17,
        TYPE_FAIRY     = 18,
    };

    enum contestType {
        CONTEST_TYPE_NONE      = 0,
        CONTEST_TYPE_TOUGH     = 1,
        CONTEST_TYPE_CLEVER    = 2,
        CONTEST_TYPE_BEAUTIFUL = 3,
        CONTEST_TYPE_COOL      = 4,
        CONTEST_TYPE_CUTE      = 5
    };

    constexpr u8 TypeEffectiveness[ NUM_TYPES ][ NUM_TYPES ] = {
        { 100, 100, 100, 100, 100, 75, 100, 0, 75, 75, 100, 100, 100, 100, 100, 100, 100, 100,
          100 }, // Normal
        { 150, 100, 75, 75, 100, 150, 75, 0, 150, 75, 100, 100, 100, 100, 75, 150, 100, 150,
          75 }, // Fight
        { 100, 150, 100, 100, 100, 75, 150, 100, 75, 75, 100, 100, 150, 75, 100, 100, 100, 100,
          100 }, // Flying
        { 100, 100, 100, 75, 75, 75, 100, 75, 0, 75, 100, 100, 150, 100, 100, 100, 100, 100,
          150 }, // Poison
        { 100, 100, 0, 150, 100, 150, 75, 100, 150, 75, 100, 150, 75, 150, 100, 100, 100, 100,
          100 }, // Ground
        { 100, 75, 150, 100, 75, 100, 150, 100, 75, 75, 100, 150, 100, 100, 100, 150, 100, 100,
          100 }, // Rock
        { 100, 75, 75, 75, 100, 100, 100, 75, 75, 75, 100, 75, 150, 100, 150, 100, 100, 150,
          75 }, // Bug
        { 0, 100, 100, 100, 100, 100, 100, 150, 75, 75, 100, 100, 100, 100, 150, 100, 100, 75,
          100 }, // Ghost
        { 100, 100, 100, 100, 100, 150, 100, 100, 75, 75, 75, 75, 100, 75, 100, 150, 100, 100,
          150 }, // Steel
        { 133, 133, 133, 133, 133, 133, 133, 133, 133, 100, 133, 133, 133, 133, 133, 133, 133, 133,
          133 }, //???
        { 100, 100, 100, 100, 150, 150, 100, 100, 100, 75, 75, 150, 75, 100, 100, 100, 75, 100,
          100 }, // Water
        { 100, 100, 100, 100, 100, 75, 150, 100, 150, 75, 75, 75, 150, 100, 100, 150, 75, 100,
          100 }, // Fire
        { 100, 100, 75, 75, 150, 150, 75, 100, 75, 75, 150, 75, 75, 100, 100, 100, 75, 100,
          100 }, // Grass
        { 100, 100, 150, 100, 0, 100, 100, 100, 100, 75, 150, 100, 75, 75, 100, 100, 75, 100,
          100 }, // Electric
        { 100, 150, 100, 150, 100, 100, 100, 100, 75, 75, 100, 100, 100, 100, 75, 100, 100, 0,
          100 }, // Psychic
        { 100, 100, 150, 100, 150, 100, 100, 100, 75, 75, 75, 75, 150, 100, 100, 75, 150, 100,
          100 }, // Ice
        { 100, 100, 100, 100, 100, 100, 100, 100, 75, 75, 100, 100, 100, 100, 100, 100, 150, 100,
          0 }, // Dragon
        { 100, 75, 100, 100, 100, 100, 100, 150, 75, 75, 100, 100, 100, 100, 150, 100, 100, 75,
          75 }, // Dark
        { 100, 150, 100, 75, 100, 100, 100, 100, 75, 75, 100, 75, 100, 100, 100, 100, 150, 150,
          100 } // Fairy
    };

    /*
     * @brief: Computes how effective a move of type p_t1 is on a pkmn of type p_t2
     */
    constexpr u8 getTypeEffectiveness( type p_t1, type p_t2 ) { // t1 is moving
        return TypeEffectiveness[ (u8) p_t1 ][ (u8) p_t2 ];
    }
} // namespace BATTLE
