package com.example.api.mappers

import com.example.api.dtos.UserGetResponse
import com.example.api.domain.models.UserModel

internal class UserGetResponseMapper {
    fun userGetResponse.toDomain(): UserModel {
        return UserModel(
            // TODO: Map DTO properties to domain model properties
        )
    }
}
