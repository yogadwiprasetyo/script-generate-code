import yaml
import argparse
from datetime import datetime
import os
from typing import Dict, List, Any


class KotlinCodeGenerator:
    def __init__(self, yaml_content: str, feature_name: str):
        self.spec = yaml.safe_load(yaml_content)
        self.feature_name = feature_name
        self.base_package = "com.example.api"
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    def generate_all(self, output_dir: str):
        """Generate all Kotlin files"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate files in order of dependency
        endpoint_constants_file = self.generate_endpoint_constants(output_dir)
        dto_files = self.generate_dtos(output_dir)
        mapper_files = self.generate_mappers(output_dir)
        remote_datasource_files = self.generate_remote_datasources(output_dir)
        repository_files = self.generate_repositories(output_dir)
        
        return {
            "endpoint_constants": endpoint_constants_file,
            "dtos": dto_files,
            "mappers": mapper_files,
            "remote_datasources": remote_datasource_files,
            "repositories": repository_files
        }
    
    def generate_endpoint_constants(self, output_dir: str) -> str:
        """Generate API endpoint constants object"""
        constants = []
        
        for feature in self.spec.get("features", []):
            endpoint = feature["endpoint"].strip("/")
            method = feature["method"].upper()
            constant_name = f"{method}_{endpoint.replace('/', '_').replace('-', '_').replace('{', '').replace('}', '').upper()}"
            constants.append(f"    const val {constant_name} = \"{endpoint}\"")
        
        file_path = os.path.join(output_dir, f"{self.feature_name}ApiEndPoint.kt")
        newline = '\n'
        with open(file_path, "w") as f:
            f.write(f"""package {self.base_package}.endpoint

internal object {self.feature_name}ApiEndPoint {{
{newline.join(constants)}
}}
""")
        return file_path
    
    def generate_dtos(self, output_dir: str) -> List[str]:
        """Generate Data Transfer Objects"""
        generated_files = []
        dto_dir = os.path.join(output_dir, "dtos")
        os.makedirs(dto_dir, exist_ok=True)
        
        dto_specs = {}
        
        for feature in self.spec.get("features", []):
            # Response DTOs
            if "response" in feature:
                response = feature["response"]
                if response["type"] == "object":
                    dto_name = f"{self.feature_name}{feature['method'].capitalize()}Response"
                    dto_specs[dto_name] = response["properties"]
                elif response["type"] == "array" and "items" in response:
                    if isinstance(response["items"], list):
                        for i, item in enumerate(response["items"]):
                            if item["type"] == "object":
                                dto_name = f"{self.feature_name}{feature['method'].capitalize()}Item{i+1}"
                                dto_specs[dto_name] = item["properties"]
                    elif response["items"]["type"] == "object":
                        dto_name = f"{self.feature_name}{feature['method'].capitalize()}Item"
                        dto_specs[dto_name] = response["items"]["properties"]
            
            # Request DTOs
            if "request" in feature and feature["request"]["type"] == "object":
                dto_name = f"{self.feature_name}{feature['method'].capitalize()}Request"
                dto_specs[dto_name] = feature["request"]["properties"]
        
        for dto_name, properties in dto_specs.items():
            file_path = os.path.join(dto_dir, f"{dto_name}.kt")
            with open(file_path, "w") as f:
                f.write(self._generate_dto_class(dto_name, properties))
            generated_files.append(file_path)
        
        return generated_files
    
    def generate_mappers(self, output_dir: str) -> List[str]:
        """Generate mapper classes for DTO to Domain conversion"""
        generated_files = []
        mapper_dir = os.path.join(output_dir, "mappers")
        os.makedirs(mapper_dir, exist_ok=True)
        
        dto_classes = set()
        
        for feature in self.spec.get("features", []):
            if "response" in feature:
                response = feature["response"]
                if response["type"] == "object":
                    dto_classes.add(f"{self.feature_name}{feature['method'].capitalize()}Response")
                elif response["type"] == "array" and "items" in response:
                    if isinstance(response["items"], list):
                        for i in range(len(response["items"])):
                            dto_classes.add(f"{self.feature_name}{feature['method'].capitalize()}Item{i+1}")
                    else:
                        dto_classes.add(f"{self.feature_name}{feature['method'].capitalize()}Item")
        
        for dto_class in dto_classes:
            mapper_name = f"{dto_class}Mapper"
            file_path = os.path.join(mapper_dir, f"{mapper_name}.kt")
            with open(file_path, "w") as f:
                f.write(f"""package {self.base_package}.mappers

import {self.base_package}.dtos.{dto_class}
import {self.base_package}.domain.models.{self.feature_name}Model

internal class {mapper_name} {{
    fun {dto_class.lower()[0] + dto_class[1:]}.toDomain(): {self.feature_name}Model {{
        return {self.feature_name}Model(
            // TODO: Map DTO properties to domain model properties
        )
    }}
}}
""")
            generated_files.append(file_path)
        
        return generated_files
    
    def generate_remote_datasources(self, output_dir: str) -> List[str]:
        """Generate remote data source interface and implementation"""
        generated_files = []
        datasource_dir = os.path.join(output_dir, "datasources")
        os.makedirs(datasource_dir, exist_ok=True)
        
        # Generate interface
        interface_methods = []
        impl_methods = []
        
        for feature in self.spec.get("features", []):
            endpoint = feature["endpoint"].strip("/")
            method = feature["method"].lower()
            # method_name = f"{method}{endpoint.replace('/', '').replace('{', '').replace('}', '').capitalize()}"
            method_name = feature["action"]
            
            # Determine return type
            return_type = f"{self.feature_name}Dto"  # Default, can be adjusted based on your needs
            
            # Build parameters
            params = []
            call_params = []
            query_params = []
            map_query_params = ""
            
            if "{" in endpoint:
                path_parts = endpoint.split("/")
                for part in path_parts:
                    if part.startswith("{") and part.endswith("}"):
                        param_name = part[1:-1]
                        params.append(f"{param_name}: String")
                        call_params.append(param_name)
            
            if "queryParams" in feature:
                for param in feature["queryParams"]:
                    kotlin_type = self._kotlin_type(param["type"])
                    params.append(f"{param['name']}: {kotlin_type}? = null")
                    # call_params.append(f"{param['name']} = {param['name']}")
                    query_params.append(f"\"{param['name']}\" to {param['name']}")
            
            if "request" in feature:
                if feature["request"]["type"] == "object":
                    params.append(f"request: {self.feature_name}{feature['method'].capitalize()}Request")
                    call_params.append("body = request")
            
            if "queryParams" in feature and feature["method"] == "get":
                map_query_params = f"queryParams = mapOf({','.join(query_params)})"

            # Interface method
            interface_method = f"    suspend fun {method_name}({', '.join(params)}): ApiResponse<{return_type}>"
            interface_methods.append(interface_method)
            
            # Implementation method
            http_method = "get" if method.lower() == "get" else method.lower()
            endpoint_constant = f"{feature['method'].upper()}_{endpoint.replace('/', '_').replace('-', '_').replace('{', '').replace('}', '').upper()}"
            
            impl_method = f"""    override suspend fun {method_name}({', '.join(params)}): ApiResponse<{return_type}> {{
        return try {{
            httpService.{http_method}(
                path = {self.feature_name}ApiEndPoint.{endpoint_constant},
                {', '.join(call_params)},
                {map_query_params}
            ).transformResult {{ response ->
                val json = parseStringToJson(response)
                ApiResponse.Success(convertJsonObjectToModel(json))
            }}
        }} catch (e: HttpException) {{
            e.toApiResponse()
        }} catch (e: Exception) {{
            ApiResponse.Error(e)
        }}
    }}"""
            impl_methods.append(impl_method)
        
        # Generate interface file
        interface_file = os.path.join(datasource_dir, f"{self.feature_name}RemoteDataSource.kt")
        doubleNewLine = '\n\n'
        with open(interface_file, "w") as f:
            f.write(f"""package {self.base_package}.datasources

import {self.base_package}.dtos.*
import {self.base_package}.network.ApiResponse

internal interface {self.feature_name}RemoteDataSource {{
{doubleNewLine.join(interface_methods)}
}}
""")
        generated_files.append(interface_file)
        
        # Generate implementation file
        impl_file = os.path.join(datasource_dir, f"{self.feature_name}RemoteDataSourceImpl.kt")
        with open(impl_file, "w") as f:
            f.write(f"""package {self.base_package}.datasources

import {self.base_package}.dtos.*
import {self.base_package}.endpoint.{self.feature_name}ApiEndPoint
import {self.base_package}.network.ApiResponse
import {self.base_package}.network.HttpException
import {self.base_package}.network.HttpService

internal class {self.feature_name}RemoteDataSourceImpl(
    private val httpService: HttpService,
) : {self.feature_name}RemoteDataSource {{
{doubleNewLine.join(impl_methods)}
}}
""")
        generated_files.append(impl_file)
        
        return generated_files
    
    def generate_repositories(self, output_dir: str) -> List[str]:
        """Generate repository interface and implementation"""
        generated_files = []
        repo_dir = os.path.join(output_dir, "repositories")
        os.makedirs(repo_dir, exist_ok=True)
        
        interface_methods = []
        impl_methods = []
        
        for feature in self.spec.get("features", []):
            endpoint = feature["endpoint"].strip("/")
            method = feature["method"].lower()
            # method_name = f"{method}{endpoint.replace('/', '').replace('{', '').replace('}', '').capitalize()}"
            method_name = feature["action"]
            
            # Build parameters
            params = []
            call_params = []
            
            if "{" in endpoint:
                path_parts = endpoint.split("/")
                for part in path_parts:
                    if part.startswith("{") and part.endswith("}"):
                        param_name = part[1:-1]
                        params.append(f"{param_name}: String")
                        call_params.append(param_name)
            
            if "queryParams" in feature:
                for param in feature["queryParams"]:
                    kotlin_type = self._kotlin_type(param["type"])
                    params.append(f"{param['name']}: {kotlin_type}? = null")
                    call_params.append(f"{param['name']} = {param['name']}")
            
            if "request" in feature:
                if feature["request"]["type"] == "object":
                    params.append(f"request: {self.feature_name}{feature['method'].capitalize()}Request")
                    call_params.append("request = request")
            
            # Interface method
            interface_method = f"    suspend fun {method_name}({', '.join(params)}): State<{self.feature_name}Model, Nothing, Nothing>"
            interface_methods.append(interface_method)
            
            # Implementation method
            impl_method = f"""    override suspend fun {method_name}({', '.join(params)}): State<{self.feature_name}Model, Nothing, Nothing> {{
        return try {{
            when (val result = remoteDataSource.{method_name}({', '.join(call_params)})) {{
                is ApiResponse.Error -> {{
                    State.Error(message = result.exception.message.orEmpty())
                }}
                is ApiResponse.Failed -> {{
                    State.Error(
                        message = result.errorDetail.message,
                        messageTitle = result.errorDetail.messageTitle,
                        iconCode = result.errorDetail.iconCode
                    )
                }}
                is ApiResponse.Success -> {{
                    State.Success(data = result.data.toDomain())
                }}
            }}
        }} catch (e: Exception) {{
            State.Error(e.message.orEmpty())
        }}
    }}"""
            impl_methods.append(impl_method)
        
        # Generate interface file
        interface_file = os.path.join(repo_dir, f"{self.feature_name}Repository.kt")
        doubleNewLine = '\n\n'
        with open(interface_file, "w") as f:
            f.write(f"""package {self.base_package}.repositories

import {self.base_package}.domain.models.{self.feature_name}Model
import com.example.core.State

interface {self.feature_name}Repository {{
{doubleNewLine.join(interface_methods)}
}}
""")
        generated_files.append(interface_file)
        
        # Generate implementation file
        impl_file = os.path.join(repo_dir, f"{self.feature_name}RepositoryImpl.kt")
        with open(impl_file, "w") as f:
            f.write(f"""package {self.base_package}.repositories

import {self.base_package}.datasources.{self.feature_name}RemoteDataSource
import {self.base_package}.domain.models.{self.feature_name}Model
import {self.base_package}.network.ApiResponse
import com.example.core.State

internal class {self.feature_name}RepositoryImpl(
    private val remoteDataSource: {self.feature_name}RemoteDataSource,
    private val userDataStore: UserDataStore,
) : {self.feature_name}Repository {{
{doubleNewLine.join(impl_methods)}
}}
""")
        generated_files.append(impl_file)
        
        return generated_files
    
    def _kotlin_type(self, type_str: str) -> str:
        """Map YAML types to Kotlin types"""
        type_mapping = {
            "string": "String",
            "integer": "Int",
            "boolean": "Boolean",
            "number": "Double"
        }
        return type_mapping.get(type_str.lower(), type_str.capitalize())
    
    def _generate_dto_class(self, class_name: str, properties: Dict[str, str]) -> str:
        """Generate a Kotlin data class for DTO"""
        properties_code = []
        newLine = ',\n'
        for name, type_str in properties.items():
            kotlin_type = self._kotlin_type(type_str)
            properties_code.append(f"    val {name}: {kotlin_type}")
        
        return f"""package {self.base_package}.dtos

/**
 * Generated on {self.timestamp}
 */
data class {class_name}(
{newLine.join(properties_code)}
)
"""


def main():
    parser = argparse.ArgumentParser(description='Generate Kotlin code from YAML API specification')
    parser.add_argument('--yaml', type=str, required=True, help='Path to YAML file')
    parser.add_argument('--feature', type=str, required=True, help='Feature name for generated code')
    parser.add_argument('--output', type=str, default='generated', help='Output directory')
    
    args = parser.parse_args()
    
    with open(args.yaml, 'r') as file:
        yaml_content = file.read()
    
    generator = KotlinCodeGenerator(yaml_content, args.feature)
    result = generator.generate_all(args.output)
    
    print("Generated files:")
    for category, files in result.items():
        print(f"\n{category}:")
        if isinstance(files, list):
            for file in files:
                print(f"  - {file}")
        else:
            print(f"  - {files}")


if __name__ == "__main__":
    main()