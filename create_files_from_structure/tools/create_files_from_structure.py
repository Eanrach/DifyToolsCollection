from collections.abc import Generator
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
import os
import json
from typing import Any
from pathlib import Path
import os
import json
import tempfile
import zipfile
import io
from datetime import datetime

class CreateFilesFromStructureTool(Tool):

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        try:
            
            structure = tool_parameters.get("structure", "")
            # yield self.create_text_message(f"test")

            result = create_files_from_structure(structure)
            # yield self.create_text_message(f"test1")

            result_info = str(result)
            # yield self.create_text_message(f"test2")
            # 输出文件信息
            yield self.create_text_message(
                result_info
            )
            # yield self.create_text_message(f"test3")

            zip_name = result["file"]["filename"]
            zip_data = result["file"]["data"]
            # yield self.create_text_message(f"test4")
            # 输出压缩文件
            yield self.create_blob_message(
                blob=zip_data,
                meta={
                    "filename" : zip_name,
                    "mime_type": "application/zip"
                }
            )
        except Exception as e:
            yield self.create_text_message(f"Error exporting: {str(e)}")
            return




def create_files_from_structure(structure: str) -> dict:
    """
    根据提供的文件结构创建目录和文件，并返回zip压缩包
    
    Args:
        structure: 包含文件结构的数组对象
        
    Returns:
        dict: 包含zip文件数据的字典
    """
    try:
        # 解析输入参数
        if not structure or not isinstance(structure, str):
            return {
                "error": "Invalid input",
                "details": "Structure must be a string"
            }

        # 字符串转JSON
        structure = json.loads(structure)

        file_structure = []
        files_data = []
        
        for item in structure["files"]:
            files_data.append(item)
            file_structure.append(item["filename"])

        # 创建临时目录
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # 确保所有文件都存在于 file_structure 中
            for file_data in files_data:
                filename = file_data.get('filename')
                if filename and filename not in file_structure:
                    file_structure.append(filename)
            
            # 创建目录结构
            created_files = []
            for file_path in file_structure:
                full_path = temp_path / file_path
                
                # 创建父目录
                full_path.parent.mkdir(parents=True, exist_ok=True)
                
                # 查找文件内容
                content = None
                for file_data in files_data:
                    if file_data.get('filename') == file_path:
                        content = file_data.get('content', '')
                        break
                
                # 写入文件内容
                if content is not None:
                    full_path.write_text(content, encoding='utf-8')
                    created_files.append(str(full_path))
                else:
                    # 如果没有内容，创建空文件
                    full_path.touch()
                    created_files.append(str(full_path))
            
            # 创建zip文件
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, temp_dir)
                        zip_file.write(file_path, arcname)
            
            zip_buffer.seek(0)
            zip_data = zip_buffer.read()
            
            # 创建结果信息
            result_info = {
                "total_files": len(created_files),
                "created_files": created_files,
                "file_structure": file_structure,
                "timestamp": datetime.now().isoformat()
            }
            
            return {
                "result": result_info,
                "file": {
                    "data": zip_data,
                    "mime_type": "application/zip",
                    "filename": f"created_files_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
                }
            }
            
    except Exception as e:
        return {
            "error": "Failed to create files",
            "details": str(e)
        }
