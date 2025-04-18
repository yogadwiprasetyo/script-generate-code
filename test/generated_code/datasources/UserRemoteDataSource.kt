package com.example.api.datasources

import com.example.api.dtos.*
import com.example.api.network.ApiResponse

internal interface UserRemoteDataSource {
    suspend fun getUsers(page: Int? = null, pageSize: Int? = null, status: String? = null): ApiResponse<UserDto>

    suspend fun getUsersById(userId: String): ApiResponse<UserDto>

    suspend fun createUser(request: UserPostRequest): ApiResponse<UserDto>

    suspend fun updateUserById(userId: String, request: UserPutRequest): ApiResponse<UserDto>

    suspend fun updateUserStatus(userId: String, request: UserPatchRequest): ApiResponse<UserDto>

    suspend fun searchUser(query: String? = null, field: String? = null): ApiResponse<UserDto>

    suspend fun validateUserEmail(request: UserPostRequest): ApiResponse<UserDto>
}
