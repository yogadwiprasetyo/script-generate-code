package com.example.api.repositories

import com.example.api.domain.models.UserModel
import com.example.core.State

interface UserRepository {
    suspend fun getUsers(page: Int? = null, pageSize: Int? = null, status: String? = null): State<UserModel, Nothing, Nothing>

    suspend fun getUsersById(userId: String): State<UserModel, Nothing, Nothing>

    suspend fun createUser(request: UserPostRequest): State<UserModel, Nothing, Nothing>

    suspend fun updateUserById(userId: String, request: UserPutRequest): State<UserModel, Nothing, Nothing>

    suspend fun updateUserStatus(userId: String, request: UserPatchRequest): State<UserModel, Nothing, Nothing>

    suspend fun searchUser(query: String? = null, field: String? = null): State<UserModel, Nothing, Nothing>

    suspend fun validateUserEmail(request: UserPostRequest): State<UserModel, Nothing, Nothing>
}
