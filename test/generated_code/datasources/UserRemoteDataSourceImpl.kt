package com.example.api.datasources

import com.example.api.dtos.*
import com.example.api.endpoint.UserApiEndPoint
import com.example.api.network.ApiResponse
import com.example.api.network.HttpException
import com.example.api.network.HttpService

internal class UserRemoteDataSourceImpl(
    private val httpService: HttpService,
) : UserRemoteDataSource {
    override suspend fun getUsers(page: Int? = null, pageSize: Int? = null, status: String? = null): ApiResponse<UserDto> {
        return try {
            httpService.get(
                path = UserApiEndPoint.GET_USERS,
                ,
                queryParams = mapOf("page" to page,"pageSize" to pageSize,"status" to status)
            ).transformResult { response ->
                val json = parseStringToJson(response)
                ApiResponse.Success(convertJsonObjectToModel(json))
            }
        } catch (e: HttpException) {
            e.toApiResponse()
        } catch (e: Exception) {
            ApiResponse.Error(e)
        }
    }

    override suspend fun getUsersById(userId: String): ApiResponse<UserDto> {
        return try {
            httpService.get(
                path = UserApiEndPoint.GET_USERS_USERID,
                userId,
                
            ).transformResult { response ->
                val json = parseStringToJson(response)
                ApiResponse.Success(convertJsonObjectToModel(json))
            }
        } catch (e: HttpException) {
            e.toApiResponse()
        } catch (e: Exception) {
            ApiResponse.Error(e)
        }
    }

    override suspend fun createUser(request: UserPostRequest): ApiResponse<UserDto> {
        return try {
            httpService.post(
                path = UserApiEndPoint.POST_USERS,
                body = request,
                
            ).transformResult { response ->
                val json = parseStringToJson(response)
                ApiResponse.Success(convertJsonObjectToModel(json))
            }
        } catch (e: HttpException) {
            e.toApiResponse()
        } catch (e: Exception) {
            ApiResponse.Error(e)
        }
    }

    override suspend fun updateUserById(userId: String, request: UserPutRequest): ApiResponse<UserDto> {
        return try {
            httpService.put(
                path = UserApiEndPoint.PUT_USERS_USERID,
                userId, body = request,
                
            ).transformResult { response ->
                val json = parseStringToJson(response)
                ApiResponse.Success(convertJsonObjectToModel(json))
            }
        } catch (e: HttpException) {
            e.toApiResponse()
        } catch (e: Exception) {
            ApiResponse.Error(e)
        }
    }

    override suspend fun updateUserStatus(userId: String, request: UserPatchRequest): ApiResponse<UserDto> {
        return try {
            httpService.patch(
                path = UserApiEndPoint.PATCH_USERS_USERID_STATUS,
                userId, body = request,
                
            ).transformResult { response ->
                val json = parseStringToJson(response)
                ApiResponse.Success(convertJsonObjectToModel(json))
            }
        } catch (e: HttpException) {
            e.toApiResponse()
        } catch (e: Exception) {
            ApiResponse.Error(e)
        }
    }

    override suspend fun searchUser(query: String? = null, field: String? = null): ApiResponse<UserDto> {
        return try {
            httpService.get(
                path = UserApiEndPoint.GET_USERS_SEARCH,
                ,
                queryParams = mapOf("query" to query,"field" to field)
            ).transformResult { response ->
                val json = parseStringToJson(response)
                ApiResponse.Success(convertJsonObjectToModel(json))
            }
        } catch (e: HttpException) {
            e.toApiResponse()
        } catch (e: Exception) {
            ApiResponse.Error(e)
        }
    }

    override suspend fun validateUserEmail(request: UserPostRequest): ApiResponse<UserDto> {
        return try {
            httpService.post(
                path = UserApiEndPoint.POST_USERS_VALIDATE_EMAIL,
                body = request,
                
            ).transformResult { response ->
                val json = parseStringToJson(response)
                ApiResponse.Success(convertJsonObjectToModel(json))
            }
        } catch (e: HttpException) {
            e.toApiResponse()
        } catch (e: Exception) {
            ApiResponse.Error(e)
        }
    }
}
