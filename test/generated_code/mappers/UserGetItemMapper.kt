package com.example.api.mappers

import com.example.api.dtos.UserGetItem
import com.example.api.domain.models.UserModel

internal class UserGetItemMapper {
    fun userGetItem.toDomain(): UserModel {
        return UserModel(
            // TODO: Map DTO properties to domain model properties
        )
    }
}
