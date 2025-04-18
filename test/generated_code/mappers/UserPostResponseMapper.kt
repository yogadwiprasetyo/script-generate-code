package com.example.api.mappers

import com.example.api.dtos.UserPostResponse
import com.example.api.domain.models.UserModel

internal class UserPostResponseMapper {
    fun userPostResponse.toDomain(): UserModel {
        return UserModel(
            // TODO: Map DTO properties to domain model properties
        )
    }
}
