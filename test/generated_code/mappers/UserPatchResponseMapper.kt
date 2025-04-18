package com.example.api.mappers

import com.example.api.dtos.UserPatchResponse
import com.example.api.domain.models.UserModel

internal class UserPatchResponseMapper {
    fun userPatchResponse.toDomain(): UserModel {
        return UserModel(
            // TODO: Map DTO properties to domain model properties
        )
    }
}
