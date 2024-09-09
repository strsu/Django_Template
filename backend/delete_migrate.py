import os
import glob


def delete_migration_files(project_dir):
    # 프로젝트 폴더 내의 모든 앱을 찾음
    for root, dirs, files in os.walk(project_dir):
        if "migrations" in dirs:
            migration_dir = os.path.join(root, "migrations")
            # __init__.py를 제외한 모든 마이그레이션 파일 삭제
            files_to_delete = glob.glob(os.path.join(migration_dir, "*.py"))
            files_to_delete += glob.glob(os.path.join(migration_dir, "*.pyc"))

            for file_path in files_to_delete:
                if not file_path.endswith("__init__.py"):
                    print(f"Deleting: {file_path}")
                    os.remove(file_path)


if __name__ == "__main__":
    # 프로젝트의 루트 디렉토리 경로를 여기에 설정
    project_directory = os.getcwd()
    delete_migration_files(project_directory)
