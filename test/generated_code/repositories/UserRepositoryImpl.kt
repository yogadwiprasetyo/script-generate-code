package com.example.api.repositories

import com.example.api.datasources.UserRemoteDataSource
import com.example.api.domain.models.UserModel
import com.example.api.network.ApiResponse
import com.example.core.State

internal class UserRepositoryImpl(
    private val remoteDataSource: UserRemoteDataSource,
    private val userDataStore: UserDataStore,
) : UserRepository {
    override suspend fun getUsers(page: Int? = null, pageSize: Int? = null, status: String? = null): State<UserModel, Nothing, Nothing> {
        return try {
            when (val result = remoteDataSource.getUsers(page = page, pageSize = pageSize, status = status)) {
                is ApiResponse.Error -> {
                    State.Error(message = result.exception.message.orEmpty())
                }
                is ApiResponse.Failed -> {
                    State.Error(
                        message = result.errorDetail.message,
                        messageTitle = result.errorDetail.messageTitle,
                        iconCode = result.errorDetail.iconCode
                    )
                }
                is ApiResponse.Success -> {
                    State.Success(data = result.data.toDomain())
                }
            }
        } catch (e: Exception) {
            State.Error(e.message.orEmpty())
        }
    }

    override suspend fun getUsersById(userId: String): State<UserModel, Nothing, Nothing> {
        return try {
            when (val result = remoteDataSource.getUsersById(userId)) {
                is ApiResponse.Error -> {
                    State.Error(message = result.exception.message.orEmpty())
                }
                is ApiResponse.Failed -> {
                    State.Error(
                        message = result.errorDetail.message,
                        messageTitle = result.errorDetail.messageTitle,
                        iconCode = result.errorDetail.iconCode
                    )
                }
                is ApiResponse.Success -> {
                    State.Success(data = result.data.toDomain())
                }
            }
        } catch (e: Exception) {
            State.Error(e.message.orEmpty())
        }
    }

    override suspend fun createUser(request: UserPostRequest): State<UserModel, Nothing, Nothing> {
        return try {
            when (val result = remoteDataSource.createUser(request = request)) {
                is ApiResponse.Error -> {
                    State.Error(message = result.exception.message.orEmpty())
                }
                is ApiResponse.Failed -> {
                    State.Error(
                        message = result.errorDetail.message,
                        messageTitle = result.errorDetail.messageTitle,
                        iconCode = result.errorDetail.iconCode
                    )
                }
                is ApiResponse.Success -> {
                    State.Success(data = result.data.toDomain())
                }
            }
        } catch (e: Exception) {
            State.Error(e.message.orEmpty())
        }
    }

    override suspend fun updateUserById(userId: String, request: UserPutRequest): State<UserModel, Nothing, Nothing> {
        return try {
            when (val result = remoteDataSource.updateUserById(userId, request = request)) {
                is ApiResponse.Error -> {
                    State.Error(message = result.exception.message.orEmpty())
                }
                is ApiResponse.Failed -> {
                    State.Error(
                        message = result.errorDetail.message,
                        messageTitle = result.errorDetail.messageTitle,
                        iconCode = result.errorDetail.iconCode
                    )
                }
                is ApiResponse.Success -> {
                    State.Success(data = result.data.toDomain())
                }
            }
        } catch (e: Exception) {
            State.Error(e.message.orEmpty())
        }
    }

    override suspend fun updateUserStatus(userId: String, request: UserPatchRequest): State<UserModel, Nothing, Nothing> {
        return try {
            when (val result = remoteDataSource.updateUserStatus(userId, request = request)) {
                is ApiResponse.Error -> {
                    State.Error(message = result.exception.message.orEmpty())
                }
                is ApiResponse.Failed -> {
                    State.Error(
                        message = result.errorDetail.message,
                        messageTitle = result.errorDetail.messageTitle,
                        iconCode = result.errorDetail.iconCode
                    )
                }
                is ApiResponse.Success -> {
                    State.Success(data = result.data.toDomain())
                }
            }
        } catch (e: Exception) {
            State.Error(e.message.orEmpty())
        }
    }

    override suspend fun searchUser(query: String? = null, field: String? = null): State<UserModel, Nothing, Nothing> {
        return try {
            when (val result = remoteDataSource.searchUser(query = query, field = field)) {
                is ApiResponse.Error -> {
                    State.Error(message = result.exception.message.orEmpty())
                }
                is ApiResponse.Failed -> {
                    State.Error(
                        message = result.errorDetail.message,
                        messageTitle = result.errorDetail.messageTitle,
                        iconCode = result.errorDetail.iconCode
                    )
                }
                is ApiResponse.Success -> {
                    State.Success(data = result.data.toDomain())
                }
            }
        } catch (e: Exception) {
            State.Error(e.message.orEmpty())
        }
    }

    override suspend fun validateUserEmail(request: UserPostRequest): State<UserModel, Nothing, Nothing> {
        return try {
            when (val result = remoteDataSource.validateUserEmail(request = request)) {
                is ApiResponse.Error -> {
                    State.Error(message = result.exception.message.orEmpty())
                }
                is ApiResponse.Failed -> {
                    State.Error(
                        message = result.errorDetail.message,
                        messageTitle = result.errorDetail.messageTitle,
                        iconCode = result.errorDetail.iconCode
                    )
                }
                is ApiResponse.Success -> {
                    State.Success(data = result.data.toDomain())
                }
            }
        } catch (e: Exception) {
            State.Error(e.message.orEmpty())
        }
    }
}
