import yaml
from string import Template
from typing import Dict, List, Any
import os
from datetime import datetime

class KotlinCodeGenerator:
    def __init__(self, yaml_content: str):
        self.spec = yaml.safe_load(yaml_content)
        self.base_package = "com.example.api"
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    def generate_all(self, output_dir: str):
        """Generate all Kotlin files"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate DTOs first since other files depend on them
        dto_files = self.generate_dtos(output_dir)
        
        # Generate other components
        endpoint_files = self.generate_endpoints(output_dir)
        datasource_files = self.generate_remote_datasources(output_dir)
        repository_files = self.generate_repositories(output_dir)
        
        return {
            "dtos": dto_files,
            "endpoints": endpoint_files,
            "datasources": datasource_files,
            "repositories": repository_files
        }
    
    def generate_dtos(self, output_dir: str) -> List[str]:
        """Generate Data Transfer Objects"""
        generated_files = []
        dto_dir = os.path.join(output_dir, "dtos")
        os.makedirs(dto_dir, exist_ok=True)
        
        # Collect all unique response and request types
        dto_specs = {}
        
        for feature in self.spec.get("features", []):
            # Response DTOs
            if "response" in feature:
                response = feature["response"]
                if response["type"] == "object":
                    dto_name = self._get_dto_name(feature["endpoint"], feature["method"], "Response")
                    dto_specs[dto_name] = response["properties"]
                elif response["type"] == "array" and "items" in response:
                    if isinstance(response["items"], list):
                        # Handle case where items is a list of objects
                        for i, item in enumerate(response["items"]):
                            if item["type"] == "object":
                                dto_name = self._get_dto_name(feature["endpoint"], feature["method"], f"Item{i+1}")
                                dto_specs[dto_name] = item["properties"]
                    elif response["items"]["type"] == "object":
                        dto_name = self._get_dto_name(feature["endpoint"], feature["method"], "Item")
                        dto_specs[dto_name] = response["items"]["properties"]
            
            # Request DTOs
            if "request" in feature and feature["request"]["type"] == "object":
                dto_name = self._get_dto_name(feature["endpoint"], feature["method"], "Request")
                dto_specs[dto_name] = feature["request"]["properties"]
        
        # Generate DTO files
        for dto_name, properties in dto_specs.items():
            file_path = os.path.join(dto_dir, f"{dto_name}.kt")
            with open(file_path, "w") as f:
                f.write(self._generate_dto_class(dto_name, properties))
            generated_files.append(file_path)
        
        return generated_files
    
    def generate_endpoints(self, output_dir: str) -> List[str]:
        """Generate API endpoint interfaces"""
        generated_files = []
        endpoint_dir = os.path.join(output_dir, "endpoints")
        os.makedirs(endpoint_dir, exist_ok=True)
        
        # Group endpoints by resource
        endpoints_by_resource = {}
        for feature in self.spec.get("features", []):
            resource = feature["endpoint"].split("/")[1].capitalize() + "Endpoints"
            if resource not in endpoints_by_resource:
                endpoints_by_resource[resource] = []
            endpoints_by_resource[resource].append(feature)
        
        # Generate endpoint interfaces
        for resource, features in endpoints_by_resource.items():
            file_path = os.path.join(endpoint_dir, f"{resource}.kt")
            with open(file_path, "w") as f:
                f.write(self._generate_endpoint_interface(resource, features))
            generated_files.append(file_path)
        
        return generated_files
    
    def generate_remote_datasources(self, output_dir: str) -> List[str]:
        """Generate remote data source implementations"""
        generated_files = []
        datasource_dir = os.path.join(output_dir, "datasources")
        os.makedirs(datasource_dir, exist_ok=True)
        
        # Group endpoints by resource
        endpoints_by_resource = {}
        for feature in self.spec.get("features", []):
            resource = feature["endpoint"].split("/")[1].capitalize() + "RemoteDataSource"
            if resource not in endpoints_by_resource:
                endpoints_by_resource[resource] = []
            endpoints_by_resource[resource].append(feature)
        
        # Generate data source classes
        for resource, features in endpoints_by_resource.items():
            file_path = os.path.join(datasource_dir, f"{resource}.kt")
            with open(file_path, "w") as f:
                f.write(self._generate_remote_datasource(resource, features))
            generated_files.append(file_path)
        
        return generated_files
    
    def generate_repositories(self, output_dir: str) -> List[str]:
        """Generate repository implementations"""
        generated_files = []
        repo_dir = os.path.join(output_dir, "repositories")
        os.makedirs(repo_dir, exist_ok=True)
        
        # Group endpoints by resource
        endpoints_by_resource = {}
        for feature in self.spec.get("features", []):
            resource = feature["endpoint"].split("/")[1].capitalize() + "Repository"
            if resource not in endpoints_by_resource:
                endpoints_by_resource[resource] = []
            endpoints_by_resource[resource].append(feature)
        
        # Generate repository classes
        for resource, features in endpoints_by_resource.items():
            file_path = os.path.join(repo_dir, f"{resource}.kt")
            with open(file_path, "w") as f:
                f.write(self._generate_repository(resource, features))
            generated_files.append(file_path)
        
        return generated_files
    
    def _get_dto_name(self, endpoint: str, method: str, suffix: str) -> str:
        """Generate a DTO class name from endpoint and method"""
        resource = endpoint.split("/")[1].capitalize()
        return f"{resource}{method.capitalize()}{suffix}"
    
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
        for name, type_str in properties.items():
            kotlin_type = self._kotlin_type(type_str)
            properties_code.append(f"    val {name}: {kotlin_type}")
        
        return f"""
package {self.base_package}.dtos

/**
 * Generated on {self.timestamp}
 */
data class {class_name}(
{','.join(properties_code)}
)
        """
    
    def _generate_endpoint_interface(self, interface_name: str, features: List[Dict[str, Any]]) -> str:
        """Generate a Retrofit interface for API endpoints"""
        methods = []
        
        for feature in features:
            endpoint = feature["endpoint"]
            method = feature["method"].lower()
            
            # Determine return type
            return_type = "Unit"
            if "response" in feature:
                response = feature["response"]
                if response["type"] == "object":
                    dto_name = self._get_dto_name(endpoint, feature["method"], "Response")
                    return_type = dto_name
                elif response["type"] == "array":
                    item_dto_name = self._get_dto_name(endpoint, feature["method"], "Item")
                    return_type = f"List<{item_dto_name}>"
            
            # Handle path parameters
            path_params = []
            if "{" in endpoint:
                path_parts = endpoint.split("/")
                for part in path_parts:
                    if part.startswith("{") and part.endswith("}"):
                        param_name = part[1:-1]
                        path_params.append(f'    @Path("{param_name}") {param_name}: String')
            
            # Handle query parameters
            query_params = []
            if "queryParams" in feature:
                for param in feature["queryParams"]:
                    kotlin_type = self._kotlin_type(param["type"])
                    query_params.append(f'    @Query("{param["name"]}") {param["name"]}: {kotlin_type}? = null')
            
            # Handle request body
            request_body = ""
            if "request" in feature:
                dto_name = self._get_dto_name(endpoint, feature["method"], "Request")
                request_body = f"\n    @Body request: {dto_name}"
            
            # Combine all parameters
            all_params = path_params + query_params
            if request_body:
                all_params.append(request_body.strip())
            
            # Build method annotation
            method_annotation = f'@{method.capitalize()}("{endpoint}")'
            
            # Build method signature
            method_signature = f"suspend fun {self._get_endpoint_method_name(endpoint, method)}("
            if all_params:
                method_signature += "\n" + ",\n".join(all_params) + "\n"
            method_signature += f"): {return_type}"
            
            methods.append(f"{method_annotation}\n{method_signature}")
        
        return f"""package {self.base_package}.endpoints

import retrofit2.http.*
import {self.base_package}.dtos.*

/**
 * Generated on {self.timestamp}
 */
interface {interface_name} {{
{''.join(methods)}
}}
"""
    
    def _generate_remote_datasource(self, class_name: str, features: List[Dict[str, Any]]) -> str:
        """Generate a remote data source implementation"""
        endpoint_interface = class_name.replace("RemoteDataSource", "Endpoints")
        methods = []
        
        for feature in features:
            endpoint = feature["endpoint"]
            method = feature["method"].lower()
            method_name = self._get_endpoint_method_name(endpoint, method)
            
            # Build method parameters
            params = []
            if "{" in endpoint:
                path_parts = endpoint.split("/")
                for part in path_parts:
                    if part.startswith("{") and part.endswith("}"):
                        param_name = part[1:-1]
                        params.append(f"{param_name}: String")
            
            if "queryParams" in feature:
                for param in feature["queryParams"]:
                    kotlin_type = self._kotlin_type(param["type"])
                    params.append(f"{param['name']}: {kotlin_type}? = null")
            
            if "request" in feature:
                dto_name = self._get_dto_name(endpoint, feature["method"], "Request")
                params.append(f"request: {dto_name}")
            
            # Build method call
            call_params = []
            if "{" in endpoint:
                path_parts = endpoint.split("/")
                for part in path_parts:
                    if part.startswith("{") and part.endswith("}"):
                        param_name = part[1:-1]
                        call_params.append(param_name)
            
            if "queryParams" in feature:
                for param in feature["queryParams"]:
                    call_params.append(param['name'])
            
            if "request" in feature:
                call_params.append("request")
            
            method_code = f"override suspend fun {method_name}({', '.join(params)}) = "
            method_code += f"api.{method_name}({', '.join(call_params)})"
            
            methods.append(method_code)
        
        return f"""package {self.base_package}.datasources

import {self.base_package}.endpoints.{endpoint_interface}
import {self.base_package}.dtos.*
import javax.inject.Inject

/**
 * Generated on {self.timestamp}
 */
class {class_name} @Inject constructor(
    private val api: {endpoint_interface}
) : I{class_name} {{
{''.join(f'    {method}' for method in methods)}
}}
"""
    
    def _generate_repository(self, class_name: str, features: List[Dict[str, Any]]) -> str:
        """Generate a repository implementation"""
        datasource_interface = class_name.replace("Repository", "RemoteDataSource")
        methods = []
        
        for feature in features:
            endpoint = feature["endpoint"]
            method = feature["method"].lower()
            method_name = self._get_endpoint_method_name(endpoint, method)
            
            # Build method parameters
            params = []
            if "{" in endpoint:
                path_parts = endpoint.split("/")
                for part in path_parts:
                    if part.startswith("{") and part.endswith("}"):
                        param_name = part[1:-1]
                        params.append(f"{param_name}: String")
            
            if "queryParams" in feature:
                for param in feature["queryParams"]:
                    kotlin_type = self._kotlin_type(param["type"])
                    params.append(f"{param['name']}: {kotlin_type}? = null")
            
            if "request" in feature:
                dto_name = self._get_dto_name(endpoint, feature["method"], "Request")
                params.append(f"request: {dto_name}")
            
            # Build method call
            call_params = []
            if "{" in endpoint:
                path_parts = endpoint.split("/")
                for part in path_parts:
                    if part.startswith("{") and part.endswith("}"):
                        param_name = part[1:-1]
                        call_params.append(param_name)
            
            if "queryParams" in feature:
                for param in feature["queryParams"]:
                    call_params.append(param['name'])
            
            if "request" in feature:
                call_params.append("request")
            
            method_code = f"override suspend fun {method_name}({', '.join(params)}) = "
            method_code += f"remoteDataSource.{method_name}({', '.join(call_params)})"
            
            methods.append(method_code)
        
        return f"""package {self.base_package}.repositories

import {self.base_package}.datasources.{datasource_interface}
import {self.base_package}.dtos.*
import javax.inject.Inject

/**
 * Generated on {self.timestamp}
 */
class {class_name} @Inject constructor(
    private val remoteDataSource: I{datasource_interface}
) : I{class_name} {{
{''.join(f'    {method}' for method in methods)}
}}
"""
    
    def _get_endpoint_method_name(self, endpoint: str, method: str) -> str:
        """Generate a method name from endpoint and HTTP method"""
        # Remove leading/trailing slashes and split
        parts = endpoint.strip("/").split("/")
        
        # The first part is usually the resource name (e.g., "users")
        resource = parts[0]
        
        # Handle special cases for method names
        if method.lower() == "get":
            if len(parts) > 1 and "{" in parts[1]:
                # ID-based get (e.g., /users/{id})
                return f"get{resource.capitalize()}ById"
            else:
                return f"get{resource.capitalize()}s"
        elif method.lower() == "post":
            return f"create{resource.capitalize()}"
        elif method.lower() == "put":
            return f"update{resource.capitalize()}"
        elif method.lower() == "delete":
            return f"delete{resource.capitalize()}"
        else:
            # Fallback - combine method and resource
            return f"{method.lower()}{resource.capitalize()}"


def main():
    # Example usage
    yaml_content = """
features:
  - endpoint: /users
    method: GET
    queryParams:
      - name: limit
        type: integer
      - name: activeOnly
        type: boolean
    response:
      type: array
      items:
        - type: object
          properties:
            id: string
            name: string
            email: string
        - type: object
          properties:
            id: string
            name: string
            email: string
        
  - endpoint: /users/{id}
    method: GET
    response:
      type: object
      properties:
        id: string
        name: string
        email: string
        createdAt: string

  - endpoint: /users
    method: POST
    request:
      type: object
      properties:
        name: string
        email: string
        age: integer
    response:
      type: object
      properties:
        id: string
        status: string
"""
    
    generator = KotlinCodeGenerator(yaml_content)
    result = generator.generate_all("generated_code")
    print(f"Generated files: {result}")


if __name__ == "__main__":
    main()