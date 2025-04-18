package com.example.api.mappers

import com.example.api.dtos.UserPutResponse
import com.example.api.domain.models.UserModel

internal class UserPutResponseMapper {
    fun userPutResponse.toDomain(): UserModel {
        return UserModel(
            // TODO: Map DTO properties to domain model properties
        )
    }
}
