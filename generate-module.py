import os
from datetime import datetime

def create_kmp_module(module_name, package_name, base_path="."):
    """
    Creates a KMP module structure with template files.
    
    Args:
        module_name (str): Name of the new module (e.g., "feature_login")
        package_name (str): Base package name (e.g., "com.yourpay")
        base_path (str): Base directory where module will be created
    """
    
    # Define module structure
    module_path = os.path.join(base_path, module_name)
    
    # Directory structure based on your requirements
    directories = [
        # Data layer
        "data/src/androidMain/kotlin/" + package_name.replace('.', '/') + "/data",
        "data/src/commonMain/kotlin/" + package_name.replace('.', '/') + "/data" + "/di",
        "data/src/commonMain/kotlin/" + package_name.replace('.', '/') + "/data" + "/model",
        "data/src/commonMain/kotlin/" + package_name.replace('.', '/') + "/data" + "/remote",
        "data/src/commonMain/kotlin/" + package_name.replace('.', '/') + "/data" + "/repository",
        "data/src/commonMain/kotlin/" + package_name.replace('.', '/') + "/data" + "/sources",
        "data/src/commonMain/kotlin/" + package_name.replace('.', '/') + "/data" + "/mapper",
        "data/src/iosMain/kotlin/" + package_name.replace('.', '/') + "/data",
        
        # Domain layer
        "domain/src/androidMain/kotlin/" + package_name.replace('.', '/') + "/domain",
        "domain/src/commonMain/kotlin/" + package_name.replace('.', '/') + "/domain" + "/model",
        "domain/src/commonMain/kotlin/" + package_name.replace('.', '/') + "/domain" + "/repository",
        "domain/src/iosMain/kotlin/" + package_name.replace('.', '/') + "/domain",
        
        # Presentation layer
        "presentation/androidMain/kotlin/" + package_name.replace('.', '/') + "/presentation",
        "presentation/commonMain/kotlin/" + package_name.replace('.', '/') + "/presentation" + "/di",
        "presentation/commonMain/kotlin/" + package_name.replace('.', '/') + "/presentation" + "/navigation",
        "presentation/commonMain/kotlin/" + package_name.replace('.', '/') + "/presentation" + "/utility",
        "presentation/commonMain/kotlin/" + package_name.replace('.', '/') + "/presentation" + "/components",
        "presentation/iosMain/kotlin/" + package_name.replace('.', '/') + "/presentation",
    ]
    
    # Files to create with their template content
    files = {
        # Data layer files
        "data/.gitignore": "/build",
        "data/build.gradle.kts": get_data_build_gradle_template(module_name),
        
        # Domain layer files
        "domain/.gitignore": "/build",
        "domain/build.gradle.kts": get_domain_build_gradle_template(module_name),
        
        # Presentation layer files
        "presentation/.gitignore": "/build",
        "presentation/build.gradle.kts": get_presentation_build_gradle_template(module_name),
        "presentation/androidMain/AndroidManifest.xml": get_manifest_template(),
    }
    
    # Create directories
    for directory in directories:
        full_path = os.path.join(module_path, directory)
        os.makedirs(full_path, exist_ok=True)
        print("Created directory:", full_path)
    
    # Create files
    for file_path, content in files.items():
        full_path = os.path.join(module_path, file_path)
        with open(full_path, 'w') as f:
            f.write(content)
        print("Created file:", full_path)
    
    print("\nKMP module '{}' created successfully at {}".format(
        module_name, os.path.abspath(module_path)))

def get_data_build_gradle_template(module_name):
    return f"""
plugins {{
    alias(libs.plugins.yourpay.kmp)
}}

kotlin {{
    sourceSets {{
        commonMain.dependencies {{
            implementation(libs.koin.core)
            implementation(libs.kotlin.serialization.json)
            implementation(libs.kotlin.coroutines.core)

            implementation(project(":core:network"))
            implementation(project(":core:utility"))
            implementation(project(":features:{module_name}:domain"))
        }}
    }}
}}
    """

def get_domain_build_gradle_template(module_name):
    return f"""
plugins {{
    alias(libs.plugins.yourpay.kmp)
}}

kotlin {{
    sourceSets {{
        commonMain.dependencies {{
            implementation(libs.kotlin.serialization.json)
            implementation(libs.kotlin.coroutines.core)
            implementation(project(":core:model"))
            implementation(project(":core:domain"))
        }}
    }}
}}
    """

def get_presentation_build_gradle_template(module_name):
    return f"""
plugins {{
    alias(libs.plugins.yourpay.cmp)
}}

kotlin {{
    sourceSets {{
        commonMain.dependencies {{
            implementation(libs.jetbrains.lifecycle.viewmodel.compose)
            implementation(libs.koin.core)
            implementation(libs.koin.composeViewModel)
            implementation(libs.navigation.compose)
            implementation(libs.kotlin.serialization.json)
            implementation(project(":core:presentation"))
            implementation(project(":core:utility"))
            implementation(project(":features:{module_name}:domain"))
            implementation(project(":core:monitoring"))
        }}
        androidMain.dependencies {{
            implementation(androidxLibs.fragment)
            implementation(project(":common:base"))
            implementation(project(":common:core"))
            implementation(project(":common:designsystem"))
            implementation(project(":common:utility"))
            implementation(project(":common:config"))
        }}
    }}
}}
    """

def get_manifest_template():
    return """
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">
</manifest>
    """

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Create a KMP module structure')
    parser.add_argument('module_name', help='Name of the module to create (e.g., feature_login)')
    parser.add_argument('package_name', help='Base package name (e.g., com.yourpay)')
    parser.add_argument('--path', default='.', help='Base path where module will be created (default: current directory)')
    
    args = parser.parse_args()
    
    create_kmp_module(args.module_name, args.package_name, args.path)